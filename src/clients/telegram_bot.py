"""Telegram client for Checklist Bot."""
from __future__ import annotations

from typing import NoReturn

from telegram.ext import Application

from ..host.config import Config


def run_bot(cfg: Config, app: Application) -> NoReturn:
    """Run the telegram bot using the provided config."""
    raise NotImplementedError
