# Architecture Components

Core components:

- Orchestrator Agent: main coordinator that delegates to sub-agents
- Databricks Analyst Agent: handles structured data queries
- Vector Search Agent: handles semantic search and retrieval
- Middleware Stack: cross-cutting workflow logic
- Memory Manager: user-scoped, thread-safe persistence
- Skills System: reusable procedure library
- Guardrails Engine: pre and post validation
- LangGraph Workflow: state-machine orchestration
- MLflow: optional tracing for future extension

Suggested technology stack:

- LangChain for agents and middleware-ready patterns
- LangGraph for stateful orchestration
- OpenAI GPT-4 class model as base LLM
- Databricks for structured analytics
- Vector database or semantic retrieval layer for search
