from __future__ import annotations

from pprint import pprint
from uuid import uuid4

from project.graph import build_graph
from project.guardrails import sanitize_input, validate_input, validate_output


def main() -> None:
    user_id = input("Enter user id (example: user_001): ").strip() or "user_001"
    user_input = input("Enter your prompt: ").strip()

    input_errors = validate_input(user_input)
    if input_errors:
        print("Input validation failed:")
        for error in input_errors:
            print(f"- {error}")
        return

    graph = build_graph()
    initial_state = {
        "user_id": user_id,
        "session_id": f"session_{uuid4().hex[:8]}",
        "user_input": user_input,
        "sanitized_input": sanitize_input(user_input),
        "tool_calls": 0,
        "trace": [],
        "validation_errors": [],
    }
    result = graph.invoke(initial_state)

    output_errors = validate_output(result)
    if output_errors:
        print("Output validation warnings:")
        for error in output_errors:
            print(f"- {error}")

    print("\nFinal response:\n")
    print(result.get("final_answer", "No answer generated."))
    print("\nTrace:\n")
    pprint(result.get("trace", []))


if __name__ == "__main__":
    main()
