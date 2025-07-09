"""Task creation module."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

import openai
from board import TaskBoard


@dataclass
class Task:
    """Represents a single task."""

    id: int
    title: str
    description: str
    classification: str
    plan: str
    links: List[str] = field(default_factory=list)
    duplicates: List[int] = field(default_factory=list)


_board = TaskBoard()


def _classify(message: str) -> str:
    msg = message.lower()
    if "кп" in msg:
        return "КП / пресейл"
    return "Техническая"


def _default_title(classification: str, message: str) -> str:
    if classification == "КП / пресейл":
        # very naive extraction of company name
        words = [w for w in message.split() if w.istitle() and "@" not in w]
        name = words[-1] if words else "клиента"
        return f"Подготовить КП для {name}"
    if "google" in message.lower() and "500" in message:
        return "Исправить 500-ошибку при Google OAuth"
    return message[:30] + "..."


def _plan_for(classification: str) -> str:
    if classification == "КП / пресейл":
        return (
            "1. Скопировать FinTech_KP.pptx в новую папку /KP/<клиент>.\n"
            "2. Заполнить разделы 1–3 данными клиента.\n"
            "3. Добавить успешные кейсы из Notion.\n"
            "4. Согласовать цену.\n"
            "5. Отправить клиенту и отметить задачу готовой."
        )
    return (
        "1. Воспроизвести баг в staging.\n"
        "2. Изучить логи или sentry-трейс.\n"
        "3. Исправить причину.\n"
        "4. Добавить тест.\n"
        "5. Создать PR.\n"
        "6. После merge PR карточка перейдет в Done автоматически."
    )


def create_task_from_message(message: str) -> Task:
    """Create a task based on provided message using simple heuristics."""
    classification = _classify(message)
    title = _default_title(classification, message)
    plan = _plan_for(classification)
    description = plan
    task, duplicates = _board.add_task(title, description, classification, plan)
    dup_ids = [d.id for d in duplicates]
    return Task(
        id=task.id,
        title=task.title,
        description=description,
        classification=classification,
        plan=plan,
        links=task.links,
        duplicates=dup_ids,
    )
