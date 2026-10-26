import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


def sanitize_workspace_name(target: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", target.strip().lower())
    cleaned = cleaned.strip("-_.")
    return cleaned or "task"


def parse_chat_ids(raw: str) -> List[int]:
    values: List[int] = []
    if not raw:
        return values
    for part in raw.split(","):
        item = part.strip()
        if not item:
            continue
        try:
            values.append(int(item))
        except ValueError:
            continue
    return values


def ensure_directory(path: str) -> str:
    location = Path(path)
    location.mkdir(parents=True, exist_ok=True)
    return str(location)


def shell_execute(command: str, cwd: Optional[str] = None, timeout: int = 600) -> Dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ},
        )
        return {
            "success": completed.returncode == 0,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "command": command,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "success": False,
            "exit_code": 124,
            "stdout": exc.stdout or "",
            "stderr": str(exc),
            "command": command,
        }
    except Exception as exc:
        return {
            "success": False,
            "exit_code": 1,
            "stdout": "",
            "stderr": str(exc),
            "command": command,
        }


def execute_with_retry(operation: Callable[[], Any], max_retries: int = 3, delay: float = 1.0) -> Any:
    attempts = 0
    while attempts < max_retries:
        try:
            return operation()
        except Exception:
            attempts += 1
            if attempts >= max_retries:
                raise
            time.sleep(delay)
    raise RuntimeError("Retry loop exhausted")


def safe_json_loads(raw: str) -> Optional[Any]:
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None
