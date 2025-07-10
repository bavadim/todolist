"""Routes LLM function calls to MCP servers."""
from __future__ import annotations

from typing import Any, Dict

from modelcontextprotocol.client import Client


def route_call(clients: Dict[str, Client], tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tool against appropriate MCP server."""
    raise NotImplementedError
