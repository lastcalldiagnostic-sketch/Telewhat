from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from app.config import Config
from app.database import init_db
from app.logger import logger


def bootstrap() -> None:
    load_dotenv()
    if not Path(Config.DEFAULT_WORKSPACE).exists():
        Path(Config.DEFAULT_WORKSPACE).mkdir(parents=True, exist_ok=True)
    if not Path("logs").exists():
        Path("logs").mkdir(parents=True, exist_ok=True)
    init_db()
    logger.info("Bootstrap complete")


if __name__ == "__main__":
    bootstrap()
    from app.telegram.bot import main

    main()
