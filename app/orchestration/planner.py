from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from app.config import Config


class Planner:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None

    def plan(self, task: str) -> Dict[str, Any]:
        if not self.client:
            return self._fallback_plan(task)
        prompt = f"""
You are a planning engine. Break the following task into executable subtasks.
Return ONLY valid JSON with this schema:
{
  "objective": "string",
  "subtasks": ["string", "string"],
  "tools": ["github", "filesystem", "shell", "browser", "http", "docker"],
  "requires_repo": true,
  "repo_name": "string_or_null",
  "workspace": "/absolute/path"
}

Task:
{task}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                raise ValueError("Planner response is not a JSON object.")
            required = parsed.get("subtasks")
            if not isinstance(required, list):
                parsed["subtasks"] = [task]
            if not isinstance(parsed.get("tools"), list):
                parsed["tools"] = ["filesystem", "shell"]
            if not parsed.get("workspace"):
                parsed["workspace"] = os.path.join(Config.DEFAULT_WORKSPACE, "task")
            if not isinstance(parsed.get("repo_name"), str):
                parsed["repo_name"] = None
            return parsed
        except Exception:
            return self._fallback_plan(task)

    def _fallback_plan(self, task: str) -> Dict[str, Any]:
        subtasks = [
            f"Analyze task requirements for: {task}",
            f"Prepare working directory for: {task}",
            f"Execute the required work for: {task}",
            f"Validate the result for: {task}",
        ]
        lower = task.lower()
        tools = ["filesystem", "shell"]
        if "github" in lower or "repo" in lower or "repository" in lower:
            tools.append("github")
        if "browser" in lower or "website" in lower or "login" in lower or "account" in lower:
            tools.append("browser")
        if "docker" in lower or "container" in lower:
            tools.append("docker")
        if "api" in lower or "http" in lower or "request" in lower:
            tools.append("http")
        return {
            "objective": task,
            "subtasks": subtasks,
            "tools": list(dict.fromkeys(tools)),
            "requires_repo": "repo" in lower or "github" in lower,
            "repo_name": None,
            "workspace": os.path.join(Config.DEFAULT_WORKSPACE, "task"),
        }
