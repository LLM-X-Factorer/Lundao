"""Async SQLite connection management for the Lundao backend."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import aiosqlite

from src.core.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

_db: Optional[aiosqlite.Connection] = None
_schema_path = Path(__file__).parent / "schema.sql"


async def init_db() -> aiosqlite.Connection:
    """Open the SQLite connection, enable WAL mode, run schema.sql."""
    global _db
    if _db is not None:
        return _db

    settings = get_settings()
    db_path = settings.database_path
    db_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Opening SQLite database at {db_path}")
    _db = await aiosqlite.connect(db_path)
    _db.row_factory = aiosqlite.Row

    # Sensible defaults for a single-process API server.
    await _db.execute("PRAGMA journal_mode=WAL")
    await _db.execute("PRAGMA foreign_keys=ON")
    await _db.execute("PRAGMA synchronous=NORMAL")

    schema_sql = _schema_path.read_text(encoding="utf-8")
    await _db.executescript(schema_sql)
    await _db.commit()

    logger.info("Database initialized")
    return _db


def get_db() -> aiosqlite.Connection:
    """Return the active connection. Call init_db() during app startup first."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() during app startup.")
    return _db


async def close_db() -> None:
    """Close the connection. Called during app shutdown."""
    global _db
    if _db is not None:
        logger.info("Closing SQLite database")
        await _db.close()
        _db = None
