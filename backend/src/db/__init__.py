"""SQLite persistence layer for tasks, papers cache, and uploads."""

from src.db.connection import get_db, init_db, close_db

__all__ = ["get_db", "init_db", "close_db"]
