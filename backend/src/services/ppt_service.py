"""PPT task lifecycle service.

Bridges the API layer and the task queue / runner / SQLite store.
- create_ppt_task: validate paper exists, create task row + enqueue
- get_task_status: read SQLite task row → camelCase dict
- get_ppt_content: read outputs/{taskId}/p1_gamma_markdown.md → markdown payload
- resolve_ppt_download_path / resolve_ppt_image_path: route file downloads
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Optional

from src.api.errors import APIError
from src.api.schemas import CreateTaskResponse
from src.core.config import get_settings
from src.db.repositories import create_task, get_task, get_upload
from src.services.task_queue import enqueue
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def create_ppt_task(
    arxiv_id: Optional[str] = None, file_id: Optional[str] = None
) -> CreateTaskResponse:
    settings = get_settings()
    if arxiv_id:
        source = "arxiv"
        paper_id = arxiv_id
        paper_title = await _resolve_arxiv_title(arxiv_id)
    elif file_id:
        upload = await get_upload(file_id)
        if upload is None:
            raise APIError(404, "FILE_NOT_FOUND", f"Upload {file_id} not found")
        source = "upload"
        paper_id = file_id
        paper_title = upload.file_name
    else:
        raise APIError(400, "BAD_REQUEST_INVALID_PARAM", "Provide arxivId or fileId")

    task_id = str(uuid.uuid4())
    output_dir = settings.output_dir / task_id
    output_dir.mkdir(parents=True, exist_ok=True)

    await create_task(
        task_id=task_id,
        paper_id=paper_id,
        paper_title=paper_title,
        source=source,
        output_dir=str(output_dir),
    )
    enqueue(task_id)

    row = await get_task(task_id)
    assert row is not None
    return CreateTaskResponse(task_id=row.id, status="queued", created_at=row.created_at)


async def get_task_status(task_id: str) -> dict[str, Any]:
    row = await get_task(task_id)
    if row is None:
        raise APIError(404, "TASK_NOT_FOUND", f"Task {task_id} not found")
    return row.to_camel()


async def get_ppt_content(task_id: str) -> dict[str, Any]:
    row = await get_task(task_id)
    if row is None:
        raise APIError(404, "TASK_NOT_FOUND", f"Task {task_id} not found")
    if row.status != "completed":
        raise APIError(
            409,
            "TASK_NOT_COMPLETED",
            f"Task is in '{row.status}' state, not 'completed'",
        )

    output_dir = Path(row.output_dir) if row.output_dir else None
    md_path = output_dir / "p1_gamma_markdown.md" if output_dir else None
    if not md_path or not md_path.exists():
        raise APIError(410, "CONTENT_GONE", "Generated content is no longer available")

    markdown = md_path.read_text(encoding="utf-8")
    total_slides = max(1, markdown.count("\n---\n") + (0 if markdown.startswith("---") else 1))

    return {
        "taskId": row.id,
        "paperId": row.paper_id,
        "type": "markdown",
        "markdown": markdown,
        "totalSlides": total_slides,
        "metadata": {
            "paperTitle": row.paper_title,
            "generatedAt": row.completed_at,
            "source": row.source,
        },
    }


async def resolve_ppt_download_path(task_id: str) -> tuple[Path, str]:
    row = await get_task(task_id)
    if row is None:
        raise APIError(404, "TASK_NOT_FOUND", f"Task {task_id} not found")
    if row.status != "completed":
        raise APIError(409, "TASK_NOT_COMPLETED", "Task not completed yet")
    if not row.output_dir:
        raise APIError(410, "CONTENT_GONE", "Output directory missing")

    output_dir = Path(row.output_dir)
    for ext in ("pdf", "pptx"):
        candidate = output_dir / f"gamma_presentation.{ext}"
        if candidate.exists():
            safe_title = "".join(c if c.isalnum() else "_" for c in row.paper_title)[:80]
            return candidate, f"{safe_title}.{ext}"

    raise APIError(410, "CONTENT_GONE", "Presentation file not found")


async def resolve_ppt_image_path(task_id: str, slide: int) -> Path:
    """images mode placeholder. Phase 2.7 adds pdf2image rendering."""
    raise APIError(
        501,
        "NOT_IMPLEMENTED",
        "Image-mode PPT preview requires Phase 2.7 (pdf2image slicing)",
    )


async def _resolve_arxiv_title(arxiv_id: str) -> str:
    """Pull title from arXiv to populate paper_title nicely. Best-effort."""
    try:
        from src.services.analysis_service import _fetch_arxiv_metadata  # type: ignore

        title, _ = await _fetch_arxiv_metadata(arxiv_id)
        return title
    except APIError:
        raise
    except Exception as exc:  # network blip, fall back to id
        logger.warning(f"Failed to fetch arXiv title for {arxiv_id}: {exc}")
        return f"arXiv:{arxiv_id}"
