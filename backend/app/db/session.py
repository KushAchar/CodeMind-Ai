"""PostgreSQL engine, session factory, and connectivity checks."""

import logging
from collections.abc import Generator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class DatabaseConnectionError(RuntimeError):
    """Raised when PostgreSQL cannot be reached."""


def _database_url() -> str:
    """Return a SQLAlchemy URL using the installed psycopg driver."""
    url = get_settings().database_url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


engine: Engine = create_engine(
    _database_url(),
    pool_pre_ping=True,
)
"""Reusable SQLAlchemy engine for PostgreSQL."""

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
"""Request-scoped SQLAlchemy session factory."""


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and always close it after the request."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()


def check_database_connection() -> None:
    """Verify PostgreSQL connectivity with a lightweight query."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        logger.exception("PostgreSQL connectivity check failed")
        raise DatabaseConnectionError(
            "PostgreSQL is unavailable"
        ) from exc
