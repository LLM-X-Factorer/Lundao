"""Paper AI analysis service.

Returns the cached Chinese analysis (summary + innovation points) for a paper,
or kicks off a background Gemini call and replies 202 'pending' so the
frontend can retry with Retry-After.
"""

from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timezone
from typing import Any, Optional

import httpx

from src.api.errors import APIError
from src.db.repositories import get_analysis, get_upload, upsert_analysis
from src.services.gemini_client import get_gemini_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


ANALYSIS_PROMPT = """你是学术论文分析助手。给定英文论文标题与摘要，输出 JSON：

{{
  "chineseSummary": "150-250 字的中文摘要，必须忠实于原文，不臆造结论",
  "innovationPoints": [
    {{"icon": "🚀", "iconLabel": "Performance breakthrough", "title": "10-20 字中文标题", "description": "30-60 字中文描述"}},
    {{"icon": "💡", "iconLabel": "Novel approach", "title": "...", "description": "..."}},
    {{"icon": "⚡", "iconLabel": "Efficiency gain", "title": "...", "description": "..."}}
  ]
}}

要求：
- 严格输出 JSON 对象，不要任何额外文字、不要 Markdown 围栏
- innovationPoints 恰好 3 条
- icon 选择合适的 emoji（🚀 突破 / 💡 创新 / ⚡ 效率 / 🎯 精度 / 🔬 理论 / 🌐 跨领域 等）
- 中文表达专业、避免翻译腔

论文标题: {title}
论文摘要: {abstract}
"""


async def get_or_start_analysis(
    arxiv_id: Optional[str] = None, file_id: Optional[str] = None
) -> dict[str, Any]:
    """Return the analysis payload, or kick off generation and return pending."""
    source = "arxiv" if arxiv_id else "upload"
    paper_id_value = arxiv_id or file_id
    paper_key = f"{source}:{paper_id_value}"

    cached = await get_analysis(paper_key)
    if cached:
        if cached["status"] == "completed":
            return cached["payload"]
        if cached["status"] == "pending":
            return {
                "paperId": paper_id_value,
                "analysisStatus": "pending",
                "retryAfter": 5,
            }
        # failed → return as failed analysis (frontend treats errorMessage)
        return {
            "paperId": paper_id_value,
            "chineseSummary": "",
            "innovationPoints": [],
            "analysisTimestamp": _now_iso(),
            "analysisStatus": "failed",
            "errorMessage": cached["errorMessage"] or "Previous analysis failed",
        }

    # Cache miss — record pending and kick off background task
    await upsert_analysis(paper_key, source, status="pending")
    asyncio.create_task(_run_analysis(paper_key, source, arxiv_id, file_id))

    return {
        "paperId": paper_id_value,
        "analysisStatus": "pending",
        "retryAfter": 5,
    }


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


async def _run_analysis(
    paper_key: str, source: str, arxiv_id: Optional[str], file_id: Optional[str]
) -> None:
    """Background task: fetch paper metadata + call Gemini, persist result."""
    paper_id_value = arxiv_id or file_id

    try:
        if source == "arxiv":
            title, abstract = await _fetch_arxiv_metadata(arxiv_id)  # type: ignore[arg-type]
        else:
            title, abstract = await _resolve_upload_metadata(file_id)  # type: ignore[arg-type]
    except APIError as exc:
        logger.warning(f"Analysis source fetch failed for {paper_key}: {exc.message}")
        await upsert_analysis(paper_key, source, status="failed", error_message=exc.message)
        return

    try:
        payload = await _call_gemini(title, abstract)
        payload["paperId"] = paper_id_value
        payload["analysisStatus"] = "completed"
        payload["analysisTimestamp"] = _now_iso()
        payload["errorMessage"] = None
        await upsert_analysis(paper_key, source, status="completed", payload=payload)
        logger.info(f"Analysis completed for {paper_key}")
    except Exception as exc:
        logger.exception(f"Gemini call failed for {paper_key}: {exc}")
        await upsert_analysis(paper_key, source, status="failed", error_message=str(exc))


async def _fetch_arxiv_metadata(arxiv_id: str) -> tuple[str, str]:
    """Fetch a paper's title + abstract from arXiv. Strips version suffix."""
    base = arxiv_id.split("v")[0]
    url = f"https://export.arxiv.org/api/query?id_list={base}"
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise APIError(502, "UPSTREAM_ERROR", f"arXiv metadata fetch failed: {exc}")

    import xml.etree.ElementTree as ET

    NS = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(resp.text)
    entry = root.find("atom:entry", NS)
    if entry is None:
        raise APIError(404, "PAPER_NOT_FOUND", f"arXiv id {arxiv_id} not found")
    title = " ".join((entry.findtext("atom:title", default="", namespaces=NS)).split())
    abstract = " ".join((entry.findtext("atom:summary", default="", namespaces=NS)).split())
    return title, abstract


async def _resolve_upload_metadata(file_id: str) -> tuple[str, str]:
    """PDF text extraction not yet implemented — return placeholder strings."""
    row = await get_upload(file_id)
    if row is None:
        raise APIError(404, "FILE_NOT_FOUND", f"Upload {file_id} not found")
    # Phase 2.7 will plug in real PDF text extraction (pypdf or pdfplumber)
    return (
        row.file_name,
        f"[PDF text extraction pending. Source: {row.file_name}. "
        f"This is a placeholder until backend PDF parsing lands.]",
    )


async def _call_gemini(title: str, abstract: str) -> dict[str, Any]:
    """Invoke Gemini with the analysis prompt and parse the JSON response."""
    client = get_gemini_client()
    prompt = ANALYSIS_PROMPT.format(title=title, abstract=abstract)
    raw = await client.generate(prompt)
    return _parse_analysis_json(raw)


def _parse_analysis_json(text: str) -> dict[str, Any]:
    """Strip Markdown fences / stray text and extract the JSON object."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # Drop leading fence (with optional 'json' label) and trailing fence
        cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```\s*$", "", cleaned)
    # Pull the outermost JSON object if there's still extra prose
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object in Gemini response: {text[:200]}")
    return json.loads(cleaned[start : end + 1])
