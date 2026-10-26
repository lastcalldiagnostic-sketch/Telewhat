from __future__ import annotations

import os
from typing import Any, Dict, List

from app.config import Config
from app.utils import ensure_directory


class Validator:
    def validate(self, task: str, workspace: str, repo_name: str | None = None, tool_results: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
        issues: List[str] = []
        output: Dict[str, Any] = {"success": True, "checks": [], "issues": issues}

        if workspace and not os.path.exists(workspace):
            issues.append(f"Workspace does not exist: {workspace}")
        output["checks"].append({"name": "workspace_exists", "passed": os.path.exists(workspace), "path": workspace})

        for result in tool_results or []:
            if isinstance(result, dict) and result.get("success") is False:
                issues.append(str(result.get("error") or result.get("stderr") or "Tool failed."))

        if repo_name and not repo_name.strip():
            issues.append("Repo name is blank.")

        output["success"] = not issues
        output["issues"] = issues
        return output
