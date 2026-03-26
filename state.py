from __future__ import annotations

from typing import Literal, TypedDict


AgentName = Literal["orchestrator", "databricks_analyst", "vector_search", "done"]


class WorkflowState(TypedDict, total=False):
    user_id: str
    session_id: str
    user_input: str
    sanitized_input: str
    next_agent: AgentName
    vector_search_done: bool
    databricks_done: bool
    retrieved_context: list[str]
    databricks_result: str
    csv_analysis_result: str
    skill_matches: list[str]
    summary: str
    final_answer: str
    tool_calls: int
    validation_errors: list[str]
    trace: list[str]
    retrieved_context: list[str]
    etl_context: list[str]
