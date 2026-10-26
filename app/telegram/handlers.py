from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from app.config import Config
from app.logger import logger
from app.task_store import add_task_event, create_task, get_task, update_task
from app.telegram.middleware import require_allowed_chat
from app.utils import shell_execute


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_allowed_chat(update, context):
        return
    await update.message.reply_text(f"Welcome to {Config.APP_NAME}. Send /help to see available commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_allowed_chat(update, context):
        return
    help_text = (
        "/start - show welcome message\n"
        "/help - show help\n"
        "/status - show current task status\n"
        "/run <task> - start a new autonomous task\n"
        "/cancel <task_id> - cancel a task"
    )
    await update.message.reply_text(help_text)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_allowed_chat(update, context):
        return
    tasks = []
    for item in []:
        tasks.append(item)
    await update.message.reply_text("No active tasks found.")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_allowed_chat(update, context):
        return
    if not context.args:
        await update.message.reply_text("Usage: /cancel <task_id>")
        return
    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task ID must be an integer.")
        return
    task = get_task(task_id)
    if not task:
        await update.message.reply_text("Task not found.")
        return
    update_task(task_id, status="cancelled")
    add_task_event(task_id, "cancelled", f"Task cancelled by user {update.effective_user.full_name}.")
    await update.message.reply_text(f"Task {task_id} cancelled.")


async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_allowed_chat(update, context):
        return
    task_text = " ".join(context.args) if context.args else ""
    if not task_text:
        await update.message.reply_text("Usage: /run <task description>")
        return
    chat_id = update.effective_chat.id
    user_name = update.effective_user.full_name if update.effective_user else "unknown"
    task = create_task(chat_id=chat_id, user_name=user_name, task_text=task_text)
    add_task_event(task.id, "created", task_text)
    await update.message.reply_text(f"Task created with ID {task.id}.\n\n{task_text}")
    logger.info("Created task %s for %s", task.id, user_name)


async def fallback_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_allowed_chat(update, context):
        return
    await update.message.reply_text("Please use /help for commands or /run <task> to start a task.")


def build_application() -> Any:
    from telegram.ext import ApplicationBuilder

    app = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("run", run_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), fallback_message))
    return app
