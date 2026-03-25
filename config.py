from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    app_name: str = "production-ready-multi-agent-system"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    databricks_host: str = os.getenv("DATABRICKS_HOST", "")
    databricks_token: str = os.getenv("DATABRICKS_TOKEN", "")
    vector_top_k: int = int(os.getenv("VECTOR_TOP_K", "3"))
    tool_call_limit: int = int(os.getenv("TOOL_CALL_LIMIT", "6"))
    memory_root: Path = field(default_factory=lambda: Path("memory"))
    skills_root: Path = field(default_factory=lambda: Path("skills"))
    docs_root: Path = field(default_factory=lambda: Path("knowledge"))
    etl_root: Path = field(default_factory=lambda: Path("etl"))
    data_root: Path = field(default_factory=lambda: Path("data"))

    @property
    def llm_enabled(self) -> bool:
        return bool(self.openai_api_key.strip())

    @property
    def databricks_enabled(self) -> bool:
        return bool(self.databricks_host.strip() and self.databricks_token.strip())


def get_settings() -> Settings:
    return Settings()
