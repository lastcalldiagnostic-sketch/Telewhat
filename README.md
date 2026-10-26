# Telewhat

A Telegram-first autonomous agent system for task decomposition, execution, repo/project generation, and progress reporting.

## Overview

Telewhat is a complete Python application that receives tasks through Telegram, decomposes them into practical subtasks, executes them with local tools, and reports progress back to Telegram. It supports:

- /start
- /help
- /status
- /run <task>
- /cancel <task_id>

It includes:

- Telegram bot integration
- OpenAI-assisted task planning
- SQLite task persistence
- Filesystem, shell, HTTP, GitHub, browser, and Docker tools
- Docker Compose deployment
- Safe defaults and environment configuration

## Quick start

1. Copy `.env.example` to `.env` and fill in your values.
2. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python -m playwright install
   ```
3. Run locally:
   ```bash
   python -m app.main
   ```
4. Or run with Docker:
   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```

## Environment

See `.env.example` for required variables.

## Telegram commands

- `/start` - show welcome message
- `/help` - show commands and usage
- `/status` - show task/state summary
- `/run create a Python CLI to fetch weather data` - run agent task
- `/cancel <task_id>` - cancel an active task

## Architecture

The app is organized into:

- `app/telegram` - Telegram bot and command handling
- `app/orchestration` - planning, execution, validation, reporting
- `app/tools` - shell, browser, GitHub, filesystem, HTTP, Docker integrations
- `app/database.py` - database setup and session creation
- `app/task_store.py` - SQLite task persistence

## License

This project is provided as a starter implementation for autonomous Telegram task execution. Configure credentials carefully and operate within your security policies.
