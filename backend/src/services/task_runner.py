"""Run a single PPT generation task end-to-end.

Loads paper materials (markdown + images) for the task's paper_id, invokes the
LangGraph workflow, persists outputs to settings.output_dir / task.id /, and
updates SQLite progress/status as it goes.

Progress model: workflow has 7 nodes; we tick progress at coarse milestones:
  10% — kicked off (state assembled)
  90% — workflow returned (writes follow)
 100% — outputs persisted, task completed
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.api.errors import APIError
from src.core.state import create_initial_state
from src.core.workflow import run_workflow
from src.db.repositories import TaskRow, get_upload, update_task_status
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def run_ppt_task(task: TaskRow) -> None:
    """Execute the LangGraph workflow for a single task."""
    output_dir = Path(task.output_dir) if task.output_dir else None
    if output_dir is None:
        raise APIError(500, "INTERNAL_ERROR", f"Task {task.id} missing output_dir")
    output_dir.mkdir(parents=True, exist_ok=True)

    await update_task_status(task.id, "generating", progress=10)

    paper_md, paper_meta, image_paths = await _load_paper_materials(task)

    initial_state = create_initial_state(
        paper_md=paper_md,
        paper_meta=paper_meta,
        image_paths=image_paths,
        paper_id=task.paper_id,
    )

    logger.info(f"Task {task.id}: starting workflow")
    final_state = await run_workflow(initial_state)
    logger.info(f"Task {task.id}: workflow returned")
    await update_task_status(task.id, "generating", progress=90)

    _persist_outputs(output_dir, final_state)

    # Pick the most informative downloadable artifact: PDF > PPTX > markdown
    download_url = _detect_download_url(task.id, output_dir, final_state)
    errors = final_state.get("errors") or []

    if errors and not final_state.get("p1_markdown"):
        # P1 is the keystone — without it nothing else is meaningful.
        await update_task_status(task.id, "failed", error_message="; ".join(errors)[:500])
        return

    await update_task_status(task.id, "completed", progress=100, download_url=download_url)
    logger.info(f"Task {task.id}: completed, download_url={download_url}")


async def _load_paper_materials(
    task: TaskRow,
) -> tuple[str, dict, list[str]]:
    """Return (paper_md, paper_meta, image_paths) for the workflow."""
    if task.source == "arxiv":
        # Short-term: use the abstract as paper body. Phase 2.7 will fetch full
        # text from arXiv (or whichever source supports it).
        from src.services.analysis_service import _fetch_arxiv_metadata

        title, abstract = await _fetch_arxiv_metadata(task.paper_id)
        paper_md = f"# {title}\n\n## Abstract\n\n{abstract}\n"
        return paper_md, {"arxivId": task.paper_id, "title": title}, []

    if task.source == "upload":
        upload = await get_upload(task.paper_id)
        if upload is None:
            raise APIError(404, "FILE_NOT_FOUND", f"Upload {task.paper_id} not found")
        # PDF text extraction is Phase 2.7. For now feed a placeholder so the
        # workflow can at least dry-run end to end with the filename context.
        paper_md = (
            f"# {upload.file_name}\n\n"
            f"[PDF text extraction pending — placeholder content for {upload.file_name}.]\n"
        )
        return paper_md, {"fileName": upload.file_name}, []

    raise APIError(500, "INTERNAL_ERROR", f"Unknown task source: {task.source}")


def _persist_outputs(output_dir: Path, final_state: dict) -> None:
    """Write each agent's text artifact to disk if present."""
    mapping = {
        "p1_markdown": "p1_gamma_markdown.md",
        "p2_document": "p2_deep_analysis.md",
        "p3_article": "p3_tech_article.md",
        "p4_script": "p4_speech_script.md",
    }
    for key, filename in mapping.items():
        text = final_state.get(key)
        if text:
            (output_dir / filename).write_text(text, encoding="utf-8")


def _detect_download_url(task_id: str, output_dir: Path, final_state: dict) -> Optional[str]:
    """Prefer the Gamma export if downloaded; otherwise return None."""
    for ext in ("pdf", "pptx"):
        if (output_dir / f"gamma_presentation.{ext}").exists():
            return f"/api/ppt_download?taskId={task_id}"
    if final_state.get("gamma_ppt_url"):
        return final_state["gamma_ppt_url"]
    return None
