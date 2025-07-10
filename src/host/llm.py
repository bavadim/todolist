"""LLM integration."""
from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from .config import Config


def run_llm(cfg: Config, messages: List[Dict[str, str]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Send messages to OpenAI and return the response."""
    raise NotImplementedError
