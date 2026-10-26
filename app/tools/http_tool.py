from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from app.tools.base_tool import BaseTool


class HTTPTool(BaseTool):
    name = "http"

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        return {"status": "ok", "tool": self.name, "args": args, "kwargs": kwargs}

    def validate(self, *args, **kwargs) -> Dict[str, Any]:
        return {"valid": True, "tool": self.name}

    def get_json(self, url: str, headers: Optional[dict] = None) -> Dict[str, Any]:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def post_json(self, url: str, payload: dict, headers: Optional[dict] = None) -> Dict[str, Any]:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def download_file(self, url: str, destination: str) -> Dict[str, Any]:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        with open(destination, "wb") as handle:
            handle.write(response.content)
        return {"success": True, "destination": destination, "bytes": len(response.content)}
