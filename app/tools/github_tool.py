from __future__ import annotations

from typing import Any, Dict, List, Optional

from github import Github

from app.config import Config
from app.tools.base_tool import BaseTool


class GitHubTool(BaseTool):
    name = "github"

    def __init__(self, token: Optional[str] = None):
        self.token = token or Config.GITHUB_TOKEN
        self.client = Github(self.token) if self.token else None

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        return {"status": "ok", "tool": self.name, "args": args, "kwargs": kwargs}

    def validate(self, *args, **kwargs) -> Dict[str, Any]:
        return {"valid": bool(self.client), "tool": self.name}

    def repo_exists(self, owner: str, repo: str) -> bool:
        if not self.client:
            return False
        try:
            self.client.get_repo(f"{owner}/{repo}")
            return True
        except Exception:
            return False

    def create_repo(self, repo_name: str, description: str = "", private: bool = False) -> Dict[str, Any]:
        if not self.client:
            return {"success": False, "error": "GitHub token not configured."}
        try:
            user = self.client.get_user()
            repo = user.create_repo(name=repo_name, description=description, private=private, auto_init=True)
            return {"success": True, "repo": repo.full_name, "html_url": repo.html_url}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def list_repos(self) -> List[str]:
        if not self.client:
            return []
        try:
            return [repo.full_name for repo in self.client.get_user().get_repos()]
        except Exception:
            return []

    def get_repo_summary(self, repo_name: str) -> Dict[str, Any]:
        if not self.client:
            return {"success": False, "error": "GitHub token not configured."}
        try:
            repo = self.client.get_repo(repo_name)
            return {
                "success": True,
                "full_name": repo.full_name,
                "private": repo.private,
                "description": repo.description,
                "default_branch": repo.default_branch,
                "html_url": repo.html_url,
            }
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def create_or_update_file(self, repo_owner: str, repo_name: str, branch: str, path: str, content: str, commit_message: str) -> Dict[str, Any]:
        if not self.client:
            return {"success": False, "error": "GitHub token not configured."}
        try:
            repo = self.client.get_repo(f"{repo_owner}/{repo_name}")
            try:
                existing = repo.get_contents(path, ref=branch)
                if isinstance(existing, list):
                    return {"success": False, "error": "Path is a directory."}
                repo.update_file(path=path, message=commit_message, content=content, sha=existing.sha, branch=branch)
            except Exception:
                repo.create_file(path=path, message=commit_message, content=content, branch=branch)
            return {"success": True, "path": path, "branch": branch}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def clone_repo(self, repo_url: str, destination: str) -> Dict[str, Any]:
        from app.utils import shell_execute

        result = shell_execute(f"git clone {repo_url} {destination}")
        return result

    def add_file_or_update(self, repo_owner: str, repo_name: str, branch: str, path: str, content: str, commit_message: str) -> Dict[str, Any]:
        return self.create_or_update_file(repo_owner, repo_name, branch, path, content, commit_message)
