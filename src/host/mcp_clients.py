"""MCP client initialisation."""
from __future__ import annotations

from typing import Dict

from modelcontextprotocol.client import Client

from .config import Config


def create_clients(cfg: Config) -> Dict[str, Client]:
    """Create MCP clients for available servers."""
    raise NotImplementedError
