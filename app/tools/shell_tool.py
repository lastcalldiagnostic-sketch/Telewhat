from __future__ import annotations

import os
import subprocess
from typing import Any, Dict, Optional

from app.tools.base_tool import BaseTool


class ShellTool(BaseTool):
    name = "shell"

    def execute(self, command: str, cwd: Optional[str] = None, timeout: int = 600, env: Optional[dict] = None) -> Dict[str, Any]:
        return self.run(command=command, cwd=cwd, timeout=timeout, env=env)

    def validate(self, *args, **kwargs) -> Dict[str, Any]:
        return {"valid": True, "tool": self.name}

    def run(self, command: str, cwd: Optional[str] = None, timeout: int = 600, env: Optional[dict] = None) -> Dict[str, Any]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        try:
            process = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                timeout=timeout,
                capture_output=True,
                text=True,
                env=merged_env,
            )
            return {
                "success": process.returncode == 0,
                "command": command,
                "return_code": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "success": False,
                "command": command,
                "return_code": 124,
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "Timed out",
            }
        except Exception as exc:
            return {
                "success": False,
                "command": command,
                "return_code": 1,
                "stdout": "",
                "stderr": str(exc),
            }

    def run_script(self, script_path: str, cwd: Optional[str] = None, timeout: int = 600, env: Optional[dict] = None) -> Dict[str, Any]:
        return self.run(command=f"bash {script_path}", cwd=cwd, timeout=timeout, env=env)

    def safe_command(self, command: str, cwd: Optional[str] = None, timeout: int = 600) -> Dict[str, Any]:
        return self.run(command=command, cwd=cwd, timeout=timeout)
