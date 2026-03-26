from __future__ import annotations

import math
import re
from pathlib import Path
import csv


from config import Settings


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


def etl_search(query: str, settings: Settings) -> list[str]:
    matches: list[tuple[float, str]] = []

    for path in sorted(settings.etl_root.rglob("*.sql")):
        content = path.read_text(encoding="utf-8").strip()
        for chunk in [part.strip() for part in content.split("\n\n") if part.strip()]:
            score = _score(query, chunk)
            if score > 0:
                matches.append((score, f"{path.name}: {chunk}"))

    matches.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in matches[: settings.vector_top_k]]


def lineage_search(query: str, settings: Settings) -> list[str]:
    return etl_search(query, settings)


def combined_context_search(query: str, settings: Settings) -> list[str]:
    knowledge_results = vector_search(query, settings)
    etl_results = etl_search(query, settings)
    return (knowledge_results + etl_results)[: settings.vector_top_k * 2]


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


def csv_metric_query(query: str, settings: Settings) -> str:
    query_lower = query.lower()

    file_map = {
        "orders.csv": settings.data_root / "bronze" / "orders.csv",
        "customers.csv": settings.data_root / "bronze" / "customers.csv",
        "support_tickets.csv": settings.data_root / "bronze" / "support_tickets.csv",
        "backlog_items.csv": settings.data_root / "bronze" / "backlog_items.csv",
        "products.csv": settings.data_root / "bronze" / "products.csv",
    }

    target_file = None
    for name, path in file_map.items():
        if name in query_lower:
            target_file = path
            break

    if target_file is None:
        if "gross_amount" in query_lower or "order" in query_lower:
            target_file = settings.data_root / "bronze" / "orders.csv"
        elif "resolution_minutes" in query_lower or "ticket" in query_lower:
            target_file = settings.data_root / "bronze" / "support_tickets.csv"
        elif "story_points" in query_lower or "backlog" in query_lower:
            target_file = settings.data_root / "bronze" / "backlog_items.csv"

    if target_file is None or not target_file.exists():
        return "No matching CSV file found for the query."

    operation = None
    if any(word in query_lower for word in ["sum", "total"]):
        operation = "sum"
    elif any(word in query_lower for word in ["count", "how many"]):
        operation = "count"
    elif any(word in query_lower for word in ["average", "avg", "mean"]):
        operation = "avg"
    elif "max" in query_lower:
        operation = "max"
    elif "min" in query_lower:
        operation = "min"

    if operation is None:
        return "Could not identify the requested operation. Use sum, count, average, min, or max."

    candidate_columns = [
        "gross_amount",
        "discount_amount",
        "return_amount",
        "quantity",
        "resolution_minutes",
        "first_response_minutes",
        "story_points",
        "unit_price",
    ]

    column = None
    for candidate in candidate_columns:
        if candidate in query_lower:
            column = candidate
            break

    rows: list[dict[str, str]] = []
    with target_file.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if operation == "count":
        return f"Count from {target_file.name}: {len(rows)}"

    if column is None:
        return "Could not identify the target numeric column in the query."

    values: list[float] = []
    for row in rows:
        raw_value = row.get(column)
        if raw_value is None or raw_value == "":
            continue
        try:
            values.append(float(raw_value))
        except ValueError:
            continue

    if not values:
        return f"No numeric values found for column '{column}' in {target_file.name}."

    if operation == "sum":
        result = sum(values)
    elif operation == "avg":
        result = sum(values) / len(values)
    elif operation == "max":
        result = max(values)
    elif operation == "min":
        result = min(values)
    else:
        return "Unsupported operation."

    return f"{operation.upper()} of {column} from {target_file.name}: {result:.2f}"
