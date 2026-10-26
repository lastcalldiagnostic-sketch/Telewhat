from __future__ import annotations

from typing import Any, Dict, List


def build_progress_message(task: str, phase: str, status: str, details: str) -> str:
    return f"Task: {task}\nPhase: {phase}\nStatus: {status}\nDetails: {details}"


def build_final_report(task: str, results: List[Dict[str, Any]], validation: Dict[str, Any]) -> str:
    lines = [f"Task: {task}", "", "Execution Summary:"]
    for idx, item in enumerate(results, start=1):
        lines.append(f"{idx}. {item.get('summary', str(item))}")
    lines.append("")
    lines.append(f"Validation: {'passed' if validation.get('success') else 'failed'}")
    if validation.get("issues"):
        lines.append("Issues:")
        for issue in validation["issues"]:
            lines.append(f"- {issue}")
    return "\n".join(lines)
