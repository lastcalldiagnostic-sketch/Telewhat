from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Task, TaskEvent, TaskStatus


def create_task(chat_id: int, user_name: str, task_text: str, workspace_path: Optional[str] = None, repo_name: Optional[str] = None) -> Task:
    session: Session = get_session()
    task = Task(
        chat_id=chat_id,
        user_name=user_name,
        task_text=task_text,
        status=TaskStatus.PENDING.value,
        workspace_path=workspace_path,
        repo_name=repo_name,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    session.close()
    return task


def get_task(task_id: int) -> Optional[Task]:
    session: Session = get_session()
    task = session.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    session.close()
    return task


def update_task(task_id: int, **kwargs: Any) -> Optional[Task]:
    session: Session = get_session()
    task = session.get(Task, task_id)
    if not task:
        session.close()
        return None
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(task)
    session.close()
    return task


def list_tasks(chat_id: Optional[int] = None) -> List[Task]:
    session: Session = get_session()
    query = select(Task)
    if chat_id is not None:
        query = query.where(Task.chat_id == chat_id)
    tasks = session.execute(query.order_by(Task.created_at.desc())).scalars().all()
    session.close()
    return tasks


def add_task_event(task_id: int, event_type: str, message: str) -> TaskEvent:
    session: Session = get_session()
    event = TaskEvent(task_id=task_id, event_type=event_type, message=message)
    session.add(event)
    session.commit()
    session.refresh(event)
    session.close()
    return event


def get_task_events(task_id: int) -> List[TaskEvent]:
    session: Session = get_session()
    events = session.execute(select(TaskEvent).where(TaskEvent.task_id == task_id).order_by(TaskEvent.created_at.asc())).scalars().all()
    session.close()
    return events
