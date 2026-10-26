from __future__ import annotations

import os
from typing import Any, Dict, List

from telegram import Update
from telegram.ext import ContextTypes

from app.config import Config
from app.utils import parse_chat_ids


async def require_allowed_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    allowed = parse_chat_ids(Config.ALLOWED_CHAT_IDS)
    if not allowed:
        return True
    chat_id = update.effective_chat.id
    if chat_id not in allowed:
        await update.message.reply_text("Your chat is not authorized to use this bot.")
        return False
    return True
