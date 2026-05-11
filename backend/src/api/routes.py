"""API routes for the Lundao backend.

All endpoints are mounted at /api (set by main.py). See docs/api-design.md for
the contract this implements. Endpoint bodies marked with NotImplementedError
are filled in by later Phase 2 sub-phases (2.3 arXiv, 2.4 upload+analyze, 2.5 PPT).
"""

from __future__ import annotations

from fastapi import APIRouter, File, Query, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from src.api.errors import APIError
from src.api.schemas import (
    CreateTaskResponse,
    GeneratePPTRequest,
    HealthResponse,
    PapersListResponse,
    UploadResponse,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


# =============================================================================
# Health
# =============================================================================


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version="0.2.0")


# =============================================================================
# arXiv paper discovery — Phase 2.3
# =============================================================================


@router.get("/arxiv_papers", response_model=PapersListResponse)
async def arxiv_papers(
    period: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
) -> PapersListResponse:
    from src.services.arxiv_service import fetch_trending_papers

    return await fetch_trending_papers(period=period, page=page, limit=limit)


# =============================================================================
# PDF upload — Phase 2.4
# =============================================================================


@router.post("/upload_pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    from src.services.upload_service import save_uploaded_pdf

    return await save_uploaded_pdf(file)


# =============================================================================
# Paper AI analysis — Phase 2.4
# =============================================================================


@router.get("/analyze_paper")
async def analyze_paper(
    arxiv_id: str | None = Query(None, alias="arxivId"),
    file_id: str | None = Query(None, alias="fileId"),
) -> JSONResponse:
    """Returns 200 with full Analysis, or 202 with retryAfter if still pending."""
    from src.services.analysis_service import get_or_start_analysis

    if (arxiv_id is None) == (file_id is None):
        raise APIError(
            400,
            "BAD_REQUEST_INVALID_PARAM",
            "Provide exactly one of arxivId or fileId",
        )

    result = await get_or_start_analysis(arxiv_id=arxiv_id, file_id=file_id)
    if result["analysisStatus"] == "pending":
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=result,
            headers={"Retry-After": "5"},
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


# =============================================================================
# PPT task creation — Phase 2.5
# =============================================================================


@router.post("/generate_ppt", response_model=CreateTaskResponse, status_code=202)
async def generate_ppt(request: GeneratePPTRequest) -> CreateTaskResponse:
    from src.services.ppt_service import create_ppt_task

    if (request.arxiv_id is None) == (request.file_id is None):
        raise APIError(
            400,
            "BAD_REQUEST_INVALID_PARAM",
            "Provide exactly one of arxivId or fileId",
        )

    return await create_ppt_task(arxiv_id=request.arxiv_id, file_id=request.file_id)


# =============================================================================
# Task status polling — Phase 2.5
# =============================================================================


@router.get("/task_status")
async def task_status(task_id: str = Query(..., alias="taskId")) -> JSONResponse:
    from src.services.ppt_service import get_task_status

    task = await get_task_status(task_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=task)


# =============================================================================
# PPT content (markdown or images) — Phase 2.5
# =============================================================================


@router.get("/ppt_content")
async def ppt_content(task_id: str = Query(..., alias="taskId")) -> JSONResponse:
    from src.services.ppt_service import get_ppt_content

    content = await get_ppt_content(task_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


# =============================================================================
# PPT file download — Phase 2.5
# =============================================================================


@router.get("/ppt_download")
async def ppt_download(task_id: str = Query(..., alias="taskId")) -> FileResponse:
    from src.services.ppt_service import resolve_ppt_download_path

    path, filename = await resolve_ppt_download_path(task_id)
    return FileResponse(path, filename=filename, media_type="application/octet-stream")


# =============================================================================
# PPT slide image (images mode) — Phase 2.5
# =============================================================================


@router.get("/ppt_image")
async def ppt_image(
    task_id: str = Query(..., alias="taskId"),
    slide: int = Query(..., ge=1),
) -> FileResponse:
    from src.services.ppt_service import resolve_ppt_image_path

    path = await resolve_ppt_image_path(task_id, slide)
    return FileResponse(path, media_type="image/png")
