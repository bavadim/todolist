from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import List
import json
import os
from difflib import SequenceMatcher


@dataclass
class BoardTask:
    id: int
    title: str
    description: str
    classification: str
    plan: str
    links: List[str] = field(default_factory=list)


class TaskBoard:
    """Very small in-memory board persisted to JSON."""

    def __init__(self, path: str = "tasks.json") -> None:
        self.path = path
        self.tasks: List[BoardTask] = []
        self.next_id = 1
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.tasks = [BoardTask(**t) for t in data.get("tasks", [])]
                self.next_id = data.get("next_id", len(self.tasks) + 1)
            except Exception:
                self.tasks = []
                self.next_id = 1

    def _save(self) -> None:
        data = {"tasks": [asdict(t) for t in self.tasks], "next_id": self.next_id}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_task(self, title: str, description: str, classification: str, plan: str) -> tuple[BoardTask, List[BoardTask]]:
        duplicates = self.find_duplicates(title)
        task = BoardTask(
            id=self.next_id,
            title=title,
            description=description,
            classification=classification,
            plan=plan,
        )
        self.tasks.append(task)
        self.next_id += 1
        self._save()
        return task, duplicates

    def find_duplicates(self, title: str, threshold: float = 0.8) -> List[BoardTask]:
        title_lower = title.lower()
        dups = []
        for t in self.tasks:
            ratio = SequenceMatcher(None, t.title.lower(), title_lower).ratio()
            if ratio >= threshold:
                dups.append(t)
        return dups
