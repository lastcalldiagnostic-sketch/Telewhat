from __future__ import annotations

import os
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph


class ExecutionState(TypedDict):
    task: str
    objective: str
    subtasks: List[str]
    tools: List[str]
    workspace: str
    repo_name: str | None
    results: List[Dict[str, Any]]
    validation: Dict[str, Any]
    final_message: str


def build_graph() -> StateGraph:
    graph = StateGraph(ExecutionState)

    def plan_task(state: ExecutionState) -> ExecutionState:
        return state

    def prepare_workspace(state: ExecutionState) -> ExecutionState:
        os.makedirs(state["workspace"], exist_ok=True)
        return state

    def create_repo_if_needed(state: ExecutionState) -> ExecutionState:
        return state

    def execute_subtasks(state: ExecutionState) -> ExecutionState:
        return state

    def validate_results(state: ExecutionState) -> ExecutionState:
        return state

    def finalize_response(state: ExecutionState) -> ExecutionState:
        state["final_message"] = state.get("final_message", "Task completed.")
        return state

    graph.add_node("plan_task", plan_task)
    graph.add_node("prepare_workspace", prepare_workspace)
    graph.add_node("create_repo_if_needed", create_repo_if_needed)
    graph.add_node("execute_subtasks", execute_subtasks)
    graph.add_node("validate_results", validate_results)
    graph.add_node("finalize_response", finalize_response)

    graph.add_edge(START, "plan_task")
    graph.add_edge("plan_task", "prepare_workspace")
    graph.add_edge("prepare_workspace", "create_repo_if_needed")
    graph.add_edge("create_repo_if_needed", "execute_subtasks")
    graph.add_edge("execute_subtasks", "validate_results")
    graph.add_edge("validate_results", "finalize_response")
    graph.add_edge("finalize_response", END)

    return graph.compile()
