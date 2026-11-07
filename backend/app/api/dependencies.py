"""Shared FastAPI dependencies such as authentication and database sessions."""

from app.db.session import get_db

__all__ = ["get_db"]
