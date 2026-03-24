from __future__ import annotations

import math
import re
from pathlib import Path

from project.config import Settings


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))


def _score(query: str, text: str) -> float:
    query_terms = _tokenize(query)
    text_terms = _tokenize(text)
    if not query_terms or not text_terms:
        return 0.0
    overlap = sum(1 for token in query_terms if token in text_terms)
    return overlap / math.sqrt(len(query_terms) * len(text_terms))


def vector_search(query: str, settings: Settings) -> list[str]:
    matches: list[tuple[float, str]] = []
    for path in sorted(settings.docs_root.glob("*.md")):
        content = path.read_text(encoding="utf-8").strip()
        for chunk in [part.strip() for part in content.split("\n\n") if part.strip()]:
            score = _score(query, chunk)
            if score > 0:
                matches.append((score, f"{path.name}: {chunk}"))

    matches.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in matches[: settings.vector_top_k]]


def databricks_query(query: str, settings: Settings) -> str:
    if settings.databricks_enabled:
        return (
            "Databricks integration is configured. Replace this stub with a real "
            "SQL warehouse or Unity Catalog query implementation."
        )

    return (
        "Databricks credentials are not configured, so the analyst agent is using "
        "a stubbed response. Intended usage: structured analytics, warehouse queries, "
        "and enterprise data lookups."
    )


def load_skill_library(skills_root: Path) -> list[str]:
    return [path.read_text(encoding="utf-8").strip() for path in sorted(skills_root.glob("*.txt"))]
