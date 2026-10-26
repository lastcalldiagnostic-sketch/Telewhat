from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from app.config import Config
from app.tools.browser_tool import BrowserTool
from app.tools.docker_tool import DockerTool
from app.tools.filesystem_tool import FilesystemTool
from app.tools.github_tool import GitHubTool
from app.tools.http_tool import HTTPTool
from app.tools.shell_tool import ShellTool
from app.orchestration.reporter import build_final_report, build_progress_message
from app.orchestration.validator import Validator
from app.utils import ensure_directory


class Executor:
    def __init__(self):
        self.filesystem_tool = FilesystemTool()
        self.shell_tool = ShellTool()
        self.github_tool = GitHubTool()
        self.browser_tool = BrowserTool()
        self.http_tool = HTTPTool()
        self.docker_tool = DockerTool()
        self.validator = Validator()

    def execute(self, task: str, plan: Dict[str, Any], progress_callback=None) -> Dict[str, Any]:
        workspace = plan.get("workspace") or os.path.join(Config.DEFAULT_WORKSPACE, "task")
        ensure_directory(workspace)
        results: List[Dict[str, Any]] = []

        for index, subtask in enumerate(plan.get("subtasks", []), start=1):
            if progress_callback:
                progress_callback(build_progress_message(task, "execution", "running", f"Executing task step {index}: {subtask}"))
            result = self._dispatch_subtask(subtask, workspace, plan.get("tools", []))
            results.append({"summary": f"Step {index}: {subtask}", **result})
            if result.get("success") is False:
                break

        validation = self.validator.validate(task, workspace, plan.get("repo_name"), results)
        final_report = build_final_report(task, results, validation)
        return {
            "workspace": workspace,
            "results": results,
            "validation": validation,
            "final_report": final_report,
        }

    def _dispatch_subtask(self, subtask: str, workspace: str, tools: List[str]) -> Dict[str, Any]:
        lower = subtask.lower()
        if any(item in lower for item in ["create", "write", "file", "project", "app", "code"]):
            file_name = os.path.join(workspace, "generated_task.txt")
            result = self.filesystem_tool.write_text_file(file_name, f"Task: {subtask}\n")
            return {"success": True, "output": result}
        if any(item in lower for item in ["repo", "github", "repository"]):
            if Config.GITHUB_TOKEN and Config.GITHUB_USERNAME:
                created = self.github_tool.create_repo(repo_name=f"task-{abs(hash(subtask))}", description=subtask)
                return {"success": created.get("success", False), "output": created}
            return {"success": False, "error": "GitHub credentials not configured."}
        if any(item in lower for item in ["browser", "login", "website", "webpage", "page"]):
            if not Config.ALLOW_BROWSER:
                return {"success": False, "error": "Browser tool disabled in configuration."}
            return {"success": True, "output": {"tool": "browser", "message": "Browser task registered."}}
        if any(item in lower for item in ["docker", "container", "image"]):
            return {"success": True, "output": {"tool": "docker", "message": "Docker task registered."}}
        if any(item in lower for item in ["http", "api", "request", "fetch", "curl"]):
            try:
                response = self.http_tool.get_json("https://api.github.com/repos/github/gitignore")
                return {"success": True, "output": response}
            except Exception as exc:
                return {"success": False, "error": str(exc)}
        result = self.shell_tool.run(f"python -c \"print({subtask!r})\"", cwd=workspace)
        return {"success": result["success"], "output": result}
