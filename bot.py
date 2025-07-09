"""Telegram bot for creating tasks from user messages."""
from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from task import create_task_from_message

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Отправьте мне сообщение, и я создам задачу.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    message = update.message.text
    task = create_task_from_message(message)

    reply_lines = [
        f"✅ #{task.id} {task.title}",
        f"Тип: {task.classification}",
        "План:",
        task.plan,
    ]
    if task.duplicates:
        dup_line = ", ".join(f"#{d}" for d in task.duplicates)
        reply_lines.append(f"Возможные дубли: {dup_line}")
    if task.links:
        reply_lines.extend(task.links)
    reply = "\n".join(reply_lines)

    await update.message.reply_text(reply)


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN not set")

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
