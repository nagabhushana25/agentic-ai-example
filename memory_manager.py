from __future__ import annotations

from datetime import datetime
from pathlib import Path

from config import Settings


class MemoryManager:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def ensure_user_space(self, user_id: str) -> Path:
        user_root = self.settings.memory_root / user_id
        (user_root / "sessions").mkdir(parents=True, exist_ok=True)
        memory_file = user_root / "memory.md"
        if not memory_file.exists():
            memory_file.write_text(
                f"# Memory for {user_id}\n\n## User Preferences\n\n- Not captured yet.\n",
                encoding="utf-8",
            )
        return user_root

    def read_user_memory(self, user_id: str) -> str:
        user_root = self.ensure_user_space(user_id)
        return (user_root / "memory.md").read_text(encoding="utf-8")

    def append_session_turn(self, user_id: str, session_id: str, user_input: str, final_answer: str) -> Path:
        user_root = self.ensure_user_space(user_id)
        session_path = user_root / "sessions" / f"{session_id}.md"
        timestamp = datetime.now().isoformat(timespec="seconds")
        entry = (
            f"## {timestamp}\n\n"
            f"### User\n{user_input}\n\n"
            f"### Assistant\n{final_answer}\n\n"
        )
        with session_path.open("a", encoding="utf-8") as handle:
            handle.write(entry)
        return session_path

    def append_user_memory(self, user_id: str, note: str) -> None:
        user_root = self.ensure_user_space(user_id)
        memory_path = user_root / "memory.md"
        with memory_path.open("a", encoding="utf-8") as handle:
            handle.write(f"\n- {note}\n")
