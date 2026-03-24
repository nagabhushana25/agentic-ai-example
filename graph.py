from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from project.agents import (
    MiddlewareManager,
    databricks_analyst_agent,
    finalize_response,
    orchestrator_agent,
    vector_search_agent,
)
from project.config import get_settings
from project.memory_manager import MemoryManager
from project.state import WorkflowState


def build_graph():
    settings = get_settings()
    memory = MemoryManager(settings)
    middleware = MiddlewareManager(settings)

    def orchestrator_node(state: WorkflowState) -> WorkflowState:
        trace = list(state.get("trace", []))
        middleware.apply_todo_tracking(state, trace)
        middleware.apply_retry_note(trace)
        state["trace"] = trace
        return orchestrator_agent(state, memory, settings)

    def vector_node(state: WorkflowState) -> WorkflowState:
        result = vector_search_agent(state, settings)
        merged = {**state, **result}
        middleware.enforce_tool_limit(merged)
        middleware.apply_summarization(merged, merged.setdefault("trace", []))
        return result

    def databricks_node(state: WorkflowState) -> WorkflowState:
        result = databricks_analyst_agent(state, settings)
        merged = {**state, **result}
        middleware.enforce_tool_limit(merged)
        return result

    def final_node(state: WorkflowState) -> WorkflowState:
        return finalize_response(state, memory)

    graph = StateGraph(WorkflowState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("vector_search", vector_node)
    graph.add_node("databricks_analyst", databricks_node)
    graph.add_node("finalize", final_node)

    graph.add_edge(START, "orchestrator")
    graph.add_conditional_edges(
        "orchestrator",
        lambda state: state["next_agent"],
        {
            "vector_search": "vector_search",
            "databricks_analyst": "databricks_analyst",
            "done": "finalize",
        },
    )
    graph.add_edge("vector_search", "orchestrator")
    graph.add_edge("databricks_analyst", "orchestrator")
    graph.add_edge("finalize", END)
    return graph.compile()
