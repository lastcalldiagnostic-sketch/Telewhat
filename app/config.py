from __future__ import annotations

import os
from typing import List, Optional


def _get_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
    DEFAULT_WORKSPACE = os.getenv("DEFAULT_WORKSPACE", "/workspace")
    DB_PATH = os.getenv("DB_PATH", "/app/app.db")
    ALLOWED_CHAT_IDS = os.getenv("ALLOWED_CHAT_IDS", "")
    APP_NAME = os.getenv("APP_NAME", "Telewhat")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ALLOW_GITHUB_REPO_CREATION = _get_bool(os.getenv("ALLOW_GITHUB_REPO_CREATION"), True)
    ALLOW_SHELL = _get_bool(os.getenv("ALLOW_SHELL"), True)
    ALLOW_BROWSER = _get_bool(os.getenv("ALLOW_BROWSER"), True)
    USER_EMAIL = os.getenv("USER_EMAIL", "")
    USER_PASSWORD = os.getenv("USER_PASSWORD", "")
    MAX_TASK_RUNTIME_MINUTES = int(os.getenv("MAX_TASK_RUNTIME_MINUTES", "60"))

    @classmethod
    def allowed_chat_ids(cls) -> List[int]:
        raw = cls.ALLOWED_CHAT_IDS.strip()
        if not raw:
            return []
        ids: List[int] = []
        for item in raw.split(","):
            val = item.strip()
            if val:
                try:
                    ids.append(int(val))
                except ValueError:
                    continue
        return ids
