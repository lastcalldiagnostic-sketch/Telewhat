from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    name = "base_tool"

    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def validate(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError
