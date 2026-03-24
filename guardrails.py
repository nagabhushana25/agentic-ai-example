from __future__ import annotations

import re

from project.state import WorkflowState


EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d[\d -]{8,}\d)\b")


def sanitize_input(user_input: str) -> str:
    redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", user_input)
    redacted = PHONE_PATTERN.sub("[REDACTED_PHONE]", redacted)
    return redacted.strip()


def validate_input(user_input: str) -> list[str]:
    errors: list[str] = []
    if not user_input.strip():
        errors.append("Input cannot be empty.")
    if len(user_input.strip()) < 10:
        errors.append("Input should be descriptive enough for agent routing.")
    return errors


def validate_output(state: WorkflowState) -> list[str]:
    errors: list[str] = []
    final_answer = state.get("final_answer", "")
    if not final_answer:
        errors.append("Final answer was not generated.")
    if "[REDACTED_" in final_answer:
        errors.append("Output still contains redaction markers that may need review.")
    return errors
