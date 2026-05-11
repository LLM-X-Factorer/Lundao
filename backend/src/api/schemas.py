"""Pydantic schemas for the Lundao API.

All response models use camelCase aliases to match the frontend JS conventions.
The Pydantic `populate_by_name=True` lets internal code keep snake_case while
serializing to camelCase on the wire.
"""

from __future__ import annotations

from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base model: snake_case internally, camelCase on the wire."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


# =============================================================================
# Domain objects (response payloads)
# =============================================================================


class Paper(CamelModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    arxiv_id: Optional[str] = None
    uploaded_file_id: Optional[str] = None
    field: str
    keywords: List[str]
    publication_date: str
    pdf_url: Optional[str] = None
    arxiv_url: Optional[str] = None
    source: Literal["arxiv", "upload"]


class InnovationPoint(CamelModel):
    icon: str
    icon_label: str
    title: str
    description: str


class Analysis(CamelModel):
    paper_id: str
    chinese_summary: str
    innovation_points: List[InnovationPoint]
    analysis_timestamp: str
    analysis_status: Literal["completed", "pending", "failed"]
    error_message: Optional[str] = None


class PPTTask(CamelModel):
    id: str
    paper_id: str
    paper_title: str
    source: Literal["arxiv", "upload"]
    status: Literal["queued", "generating", "completed", "failed"]
    progress: Optional[int] = None
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    download_url: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0


class PPTContentMarkdown(CamelModel):
    task_id: str
    paper_id: str
    type: Literal["markdown"] = "markdown"
    markdown: str
    total_slides: int
    metadata: dict[str, Any]


class PPTContentImages(CamelModel):
    task_id: str
    paper_id: str
    type: Literal["images"] = "images"
    slides: List[str]
    total_slides: int
    metadata: dict[str, Any]


PPTContent = Union[PPTContentMarkdown, PPTContentImages]


# =============================================================================
# List endpoints
# =============================================================================


class Pagination(CamelModel):
    page: int
    limit: int
    total_count: int
    total_pages: int


class PapersListResponse(CamelModel):
    papers: List[Paper]
    pagination: Pagination
    cached_at: Optional[str] = None


# =============================================================================
# Upload
# =============================================================================


class UploadResponse(CamelModel):
    file_id: str
    file_name: str
    file_size: int
    uploaded_at: str


# =============================================================================
# Generate PPT
# =============================================================================


class GeneratePPTRequest(CamelModel):
    arxiv_id: Optional[str] = None
    file_id: Optional[str] = None


class CreateTaskResponse(CamelModel):
    task_id: str
    status: Literal["queued"]
    created_at: str


# =============================================================================
# Health
# =============================================================================


class HealthResponse(CamelModel):
    status: Literal["ok"]
    version: str


# =============================================================================
# Pending Analysis (HTTP 202)
# =============================================================================


class PendingAnalysisResponse(CamelModel):
    paper_id: str
    analysis_status: Literal["pending"] = "pending"
    retry_after: int = 5
