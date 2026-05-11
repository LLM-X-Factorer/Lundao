"""In-process async task queue.

Uses a single asyncio.Queue with N worker coroutines started during FastAPI
lifespan. Each worker pulls a taskId, looks up the row in SQLite, and runs the
PPT generation workflow. Progress is persisted back to SQLite so /task_status
can stream progress to the frontend.
"""

from __future__ import annotations

import asyncio
from typing import Optional

from src.core.config import get_settings
from src.db.repositories import get_task, update_task_status
from src.utils.logger import get_logger

logger = get_logger(__name__)

_queue: Optional[asyncio.Queue[str]] = None
_workers: list[asyncio.Task] = []
_stopping = False


def enqueue(task_id: str) -> None:
    """Push a task id onto the queue. Non-blocking (queue is unbounded)."""
    if _queue is None:
        raise RuntimeError("Task queue not started. Call start_workers() first.")
    _queue.put_nowait(task_id)
    logger.info(f"Enqueued task {task_id}")


async def start_workers() -> None:
    """Start N background workers based on settings.max_concurrent_tasks."""
    global _queue, _stopping
    if _queue is not None:
        return
    _queue = asyncio.Queue()
    _stopping = False

    settings = get_settings()
    n = settings.max_concurrent_tasks
    for i in range(n):
        worker = asyncio.create_task(_worker_loop(i))
        _workers.append(worker)
    logger.info(f"Started {n} task workers")


async def stop_workers() -> None:
    """Cancel all workers and wait for them to exit."""
    global _stopping
    _stopping = True
    for w in _workers:
        w.cancel()
    if _workers:
        await asyncio.gather(*_workers, return_exceptions=True)
    _workers.clear()
    logger.info("All task workers stopped")


async def _worker_loop(worker_id: int) -> None:
    """Per-worker coroutine. Pulls tasks off the queue until cancelled."""
    logger.info(f"Worker {worker_id} ready")
    while not _stopping:
        try:
            task_id = await _queue.get()  # type: ignore[union-attr]
        except asyncio.CancelledError:
            break

        try:
            await _run_task(task_id)
        except asyncio.CancelledError:
            # Mark the in-flight task as failed so it doesn't stay 'generating' forever.
            await update_task_status(
                task_id, "failed", error_message="Worker cancelled during shutdown"
            )
            break
        except Exception as exc:  # pragma: no cover — defensive
            logger.exception(f"Worker {worker_id} crashed handling {task_id}: {exc}")
            await update_task_status(task_id, "failed", error_message=str(exc))
        finally:
            if _queue is not None:
                _queue.task_done()


async def _run_task(task_id: str) -> None:
    """Execute a single PPT generation task end-to-end."""
    # Local import to avoid circular dependencies (workflow imports lots of things).
    from src.services.task_runner import run_ppt_task

    row = await get_task(task_id)
    if row is None:
        logger.warning(f"Task {task_id} disappeared before worker picked it up")
        return
    if row.status != "queued":
        logger.warning(f"Task {task_id} not in 'queued' state (got '{row.status}'); skipping")
        return

    logger.info(f"Worker picked up task {task_id} for paper {row.paper_id}")
    await update_task_status(task_id, "generating", progress=0)
    try:
        await run_ppt_task(row)
    except Exception as exc:
        logger.exception(f"Task {task_id} failed: {exc}")
        await update_task_status(task_id, "failed", error_message=str(exc))
