from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import Config


class Base(DeclarativeBase):
    pass


engine = create_engine(f"sqlite:///{Config.DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    from app.models import Task, TaskEvent  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return SessionLocal()
