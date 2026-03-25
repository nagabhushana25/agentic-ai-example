from __future__ import annotations

from dataclasses import dataclass

from config import Settings
from memory_manager import MemoryManager
from state import WorkflowState
from tools import (databricks_query, load_skill_library,
                    vector_search,combined_context_search)


@dataclass(slots=True)
class MiddlewareManager:
    settings: Settings

    def apply_todo_tracking(self, state: WorkflowState, trace: list[str]) -> None:
        trace.append("middleware: todo tracking attached to workflow state")

    def apply_summarization(self, state: WorkflowState, trace: list[str]) -> None:
        if state.get("retrieved_context") and not state.get("summary"):
            state["summary"] = " | ".join(state["retrieved_context"][:2])
            trace.append("middleware: summarized retrieved context")

    def enforce_tool_limit(self, state: WorkflowState) -> None:
        used = state.get("tool_calls", 0)
        if used > self.settings.tool_call_limit:
            raise RuntimeError("Tool call limit exceeded.")

    def apply_retry_note(self, trace: list[str]) -> None:
        trace.append("middleware: retry policy available for transient tool failures")


def orchestrator_agent(state: WorkflowState, memory: MemoryManager, settings: Settings) -> WorkflowState:
    trace = list(state.get("trace", []))
    user_memory = memory.read_user_memory(state["user_id"])
    trace.append("orchestrator: loaded user-scoped memory")

    if not state.get("vector_search_done", False):
        next_agent = "vector_search"
    elif not state.get("databricks_done", False):
        next_agent = "databricks_analyst"
    else:
        next_agent = "done"

    skill_library = load_skill_library(settings.skills_root)
    matched_skills = [item.splitlines()[0] for item in skill_library if any(token in item.lower() for token in state["sanitized_input"].lower().split())]
    if not matched_skills:
        matched_skills = ["General orchestration and retrieval workflow"]

    trace.append(f"orchestrator: selected next agent {next_agent}")
    trace.append("orchestrator: reviewed skills library")

    return {
        "next_agent": next_agent,
        "skill_matches": matched_skills[:3],
        "summary": user_memory.splitlines()[0],
        "trace": trace,
    }


def vector_search_agent(state: WorkflowState, settings: Settings) -> WorkflowState:
    trace = list(state.get("trace", []))
    context = combined_context_search(state["sanitized_input"], settings)

    if context:
        trace.append(f"vector_search_agent: retrieved {len(context)} knowledge chunks")
    else:
        trace.append("vector_search_agent: no matching knowledge chunks found")

    return {
        "vector_search_done": True,
        "retrieved_context": context,
        "tool_calls": state.get("tool_calls", 0) + 1,
        "trace": trace,
    }



def databricks_analyst_agent(state: WorkflowState, settings: Settings) -> WorkflowState:
    trace = list(state.get("trace", []))
    result = databricks_query(state["sanitized_input"], settings)
    trace.append("databricks_analyst_agent: produced structured-data analysis")
    return {
        "databricks_done": True,
        "databricks_result": result,
        "tool_calls": state.get("tool_calls", 0) + 1,
        "trace": trace,
    }



def finalize_response(state: WorkflowState, memory: MemoryManager) -> WorkflowState:
    trace = list(state.get("trace", []))
    retrieved = "\n".join(f"- {item}" for item in state.get("retrieved_context", []))
    skills = "\n".join(f"- {item}" for item in state.get("skill_matches", []))

    final_answer = (
        f"User request: {state['sanitized_input']}\n\n"
        "System design:\n"
        "- Orchestrator agent delegates work to specialized sub-agents.\n"
        "- User-scoped memory stores persistent notes and session history.\n"
        "- Guardrails validate input and output while masking sensitive values.\n"
        "- Vector search grounds responses with project knowledge and RAG-style retrieval.\n"
        "- Databricks analyst agent is ready for structured enterprise data integration.\n\n"
        f"Relevant skills:\n{skills or '- No matching skills found.'}\n\n"
        f"Retrieved context:\n{retrieved or '- No matching knowledge found.'}\n\n"
        f"Databricks analysis:\n{state.get('databricks_result', 'Not generated.')}\n"
    )

    trace.append("finalizer: built final response")
    memory.append_user_memory(state["user_id"], "Most recent request involved the multi-agent assignment scaffold.")
    memory.append_session_turn(
        user_id=state["user_id"],
        session_id=state["session_id"],
        user_input=state["user_input"],
        final_answer=final_answer,
    )
    trace.append("finalizer: persisted user memory and session history")
    return {"final_answer": final_answer, "trace": trace}
