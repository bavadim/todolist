"""Task creation module."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

import openai


@dataclass
class Task:
    """Represents a single task."""

    title: str
    description: str
    links: List[str] = field(default_factory=list)


def create_task_from_message(message: str) -> Task:
    """Create a task using ChatGPT based on provided message."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        "Сформулируй краткое описание задачи на основе сообщения пользователя. "
        "Ответь в формате: <title>\n<description>"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{prompt}\n{message}"}],
    )
    text = response.choices[0].message.content.strip()
    title, _, description = text.partition("\n")
    return Task(title=title or "Задача", description=description)
