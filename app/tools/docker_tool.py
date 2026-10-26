from __future__ import annotations

import json
import subprocess
from typing import Any, Dict, List, Optional

from app.tools.base_tool import BaseTool


class DockerTool(BaseTool):
    name = "docker"

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        return {"status": "ok", "tool": self.name, "args": args, "kwargs": kwargs}

    def validate(self, *args, **kwargs) -> Dict[str, Any]:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        return {"valid": result.returncode == 0, "tool": self.name, "output": result.stdout.strip()}

    def build_image(self, context_dir: str, image_name: str) -> Dict[str, Any]:
        result = subprocess.run(["docker", "build", "-t", image_name, context_dir], capture_output=True, text=True)
        return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr, "image": image_name}

    def run_container(self, image_name: str, command: Optional[str] = None, ports: Optional[List[str]] = None, environment: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        cmd = ["docker", "run", "-d", image_name]
        if command:
            cmd.extend(["bash", "-lc", command])
        if ports:
            for port in ports:
                cmd.extend(["-p", port])
        if environment:
            for key, value in environment.items():
                cmd.extend(["-e", f"{key}={value}"])
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}

    def ps(self) -> Dict[str, Any]:
        result = subprocess.run(["docker", "ps", "--format", "json"], capture_output=True, text=True)
        return {"success": result.returncode == 0, "output": result.stdout}

    def logs(self, container_id: str) -> Dict[str, Any]:
        result = subprocess.run(["docker", "logs", container_id], capture_output=True, text=True)
        return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
