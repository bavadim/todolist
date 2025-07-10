"""Configuration utilities for Checklist Bot."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class Config:
    """Application configuration loaded from environment."""

    openai_api_key: str
    github_pat: str
    notion_token: str
    google_credentials: Path
    telegram_token: str
    gdrive_uri: str
    notion_uri: str
    github_uri: str


def load_config(env_file: Optional[Path] = None) -> Config:
    """Load configuration from ``.env`` file and environment variables."""
    raise NotImplementedError
