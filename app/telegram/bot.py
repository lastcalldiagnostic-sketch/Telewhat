from __future__ import annotations

from telegram.ext import Application

from app.config import Config
from app.logger import logger


def main() -> None:
    if not Config.TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is missing. Set it in your environment or .env file.")
    from app.telegram.handlers import build_application

    app: Application = build_application()
    logger.info("Starting Telegram bot")
    app.run_polling()
