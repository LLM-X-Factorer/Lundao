"""Repository functions for the four SQLite tables.

All functions are async and use the global aiosqlite connection from
`src.db.connection.get_db()`. JSON columns are serialized with the stdlib
`json` module — no schemas are inferred, callers pass dicts.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from src.db.connection import get_db


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# =============================================================================
# tasks
# =============================================================================


@dataclass
class TaskRow:
    id: str
    paper_id: str
    paper_title: str
    source: str
    status: str
    progress: Optional[int]
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    download_url: Optional[str]
    error_message: Optional[str]
    retry_count: int
    output_dir: Optional[str]

    def to_camel(self) -> dict[str, Any]:
        """Convert to camelCase dict for API responses."""
        return {
            "id": self.id,
            "paperId": self.paper_id,
            "paperTitle": self.paper_title,
            "source": self.source,
            "status": self.status,
            "progress": self.progress,
            "createdAt": self.created_at,
            "startedAt": self.started_at,
            "completedAt": self.completed_at,
            "downloadUrl": self.download_url,
            "errorMessage": self.error_message,
            "retryCount": self.retry_count,
        }


async def create_task(
    task_id: str, paper_id: str, paper_title: str, source: str, output_dir: str
) -> None:
    """Insert a new task in `queued` status."""
    db = get_db()
    await db.execute(
        """
        INSERT INTO tasks (id, paper_id, paper_title, source, status, progress,
                           created_at, retry_count, output_dir)
        VALUES (?, ?, ?, ?, 'queued', NULL, ?, 0, ?)
        """,
        (task_id, paper_id, paper_title, source, _now_iso(), output_dir),
    )
    await db.commit()


async def get_task(task_id: str) -> Optional[TaskRow]:
    db = get_db()
    cursor = await db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = await cursor.fetchone()
    return TaskRow(**dict(row)) if row else None


async def update_task_status(
    task_id: str,
    status: str,
    progress: Optional[int] = None,
    download_url: Optional[str] = None,
    error_message: Optional[str] = None,
) -> None:
    """Update task status, progress, and lifecycle timestamps as needed."""
    db = get_db()
    now = _now_iso()
    fields = ["status = ?"]
    values: list[Any] = [status]

    if progress is not None:
        fields.append("progress = ?")
        values.append(progress)
    if download_url is not None:
        fields.append("download_url = ?")
        values.append(download_url)
    if error_message is not None:
        fields.append("error_message = ?")
        values.append(error_message)
    if status == "generating":
        fields.append("started_at = COALESCE(started_at, ?)")
        values.append(now)
    elif status in ("completed", "failed"):
        fields.append("completed_at = ?")
        values.append(now)

    values.append(task_id)
    await db.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", values)
    await db.commit()


# =============================================================================
# papers_cache  (arXiv list cache)
# =============================================================================


async def get_papers_cache(period: str, page: int, limit: int) -> Optional[dict[str, Any]]:
    """Return cached arXiv list payload if not expired, else None."""
    db = get_db()
    key = f"{period}:{page}:{limit}"
    cursor = await db.execute(
        "SELECT payload, expires_at FROM papers_cache WHERE cache_key = ?", (key,)
    )
    row = await cursor.fetchone()
    if not row:
        return None
    if row["expires_at"] < _now_iso():
        return None
    return json.loads(row["payload"])


async def set_papers_cache(
    period: str, page: int, limit: int, payload: dict[str, Any], ttl_hours: int
) -> None:
    db = get_db()
    key = f"{period}:{page}:{limit}"
    now = datetime.now(timezone.utc)
    expires = now + timedelta(hours=ttl_hours)
    await db.execute(
        """
        INSERT INTO papers_cache (cache_key, period, page, payload, cached_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(cache_key) DO UPDATE SET
            payload = excluded.payload,
            cached_at = excluded.cached_at,
            expires_at = excluded.expires_at
        """,
        (
            key,
            period,
            page,
            json.dumps(payload, ensure_ascii=False),
            now.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            expires.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        ),
    )
    await db.commit()


# =============================================================================
# analysis_cache  (paper AI analysis)
# =============================================================================


async def get_analysis(paper_key: str) -> Optional[dict[str, Any]]:
    db = get_db()
    cursor = await db.execute(
        "SELECT status, payload, error_message FROM analysis_cache WHERE paper_key = ?",
        (paper_key,),
    )
    row = await cursor.fetchone()
    if not row:
        return None
    return {
        "status": row["status"],
        "payload": json.loads(row["payload"]) if row["payload"] else None,
        "errorMessage": row["error_message"],
    }


async def upsert_analysis(
    paper_key: str,
    source: str,
    status: str,
    payload: Optional[dict[str, Any]] = None,
    error_message: Optional[str] = None,
) -> None:
    db = get_db()
    now = _now_iso()
    payload_json = json.dumps(payload, ensure_ascii=False) if payload else None
    completed_at = now if status in ("completed", "failed") else None
    await db.execute(
        """
        INSERT INTO analysis_cache (paper_key, source, status, payload, error_message,
                                    started_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(paper_key) DO UPDATE SET
            status = excluded.status,
            payload = COALESCE(excluded.payload, analysis_cache.payload),
            error_message = excluded.error_message,
            completed_at = excluded.completed_at
        """,
        (paper_key, source, status, payload_json, error_message, now, completed_at),
    )
    await db.commit()


# =============================================================================
# uploads
# =============================================================================


@dataclass
class UploadRow:
    id: str
    file_name: str
    file_size: int
    md5: Optional[str]
    storage_path: str
    uploaded_at: str
    expires_at: str


async def create_upload(
    file_id: str,
    file_name: str,
    file_size: int,
    storage_path: str,
    ttl_hours: int,
    md5: Optional[str] = None,
) -> UploadRow:
    db = get_db()
    now = datetime.now(timezone.utc)
    expires = now + timedelta(hours=ttl_hours)
    row = UploadRow(
        id=file_id,
        file_name=file_name,
        file_size=file_size,
        md5=md5,
        storage_path=storage_path,
        uploaded_at=now.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        expires_at=expires.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    )
    await db.execute(
        """
        INSERT INTO uploads (id, file_name, file_size, md5, storage_path, uploaded_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row.id,
            row.file_name,
            row.file_size,
            row.md5,
            row.storage_path,
            row.uploaded_at,
            row.expires_at,
        ),
    )
    await db.commit()
    return row


async def get_upload(file_id: str) -> Optional[UploadRow]:
    db = get_db()
    cursor = await db.execute("SELECT * FROM uploads WHERE id = ?", (file_id,))
    row = await cursor.fetchone()
    return UploadRow(**dict(row)) if row else None
