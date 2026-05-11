"""arXiv discovery service.

Proxies queries to the arXiv export API, parses the Atom feed, maps to the
internal Paper schema, and caches results in SQLite (24h TTL).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import List

import httpx

from src.api.errors import APIError
from src.api.schemas import Paper, Pagination, PapersListResponse
from src.core.config import get_settings
from src.db.repositories import get_papers_cache, set_papers_cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

ARXIV_API_URL = "https://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}

# Category set covering AI/ML/CV/NLP — the bread and butter of CS arXiv research
CATEGORIES = ["cs.AI", "cs.LG", "cs.CV", "cs.CL"]

PERIOD_DAYS = {"daily": 2, "weekly": 8, "monthly": 31}

# arXiv ID → field display name. Map the common CS categories users encounter.
FIELD_DISPLAY = {
    "cs.AI": "Artificial Intelligence",
    "cs.LG": "Machine Learning",
    "cs.CV": "Computer Vision",
    "cs.CL": "Natural Language Processing",
    "cs.RO": "Robotics",
    "cs.NE": "Neural Computing",
}


async def fetch_trending_papers(period: str, page: int, limit: int) -> PapersListResponse:
    """Return cached or freshly fetched paper list for the given period."""
    cached = await get_papers_cache(period, page, limit)
    if cached:
        logger.info(f"arXiv cache hit: period={period} page={page} limit={limit}")
        return PapersListResponse.model_validate(cached)

    logger.info(f"arXiv cache miss: fetching from upstream (period={period}, page={page})")
    response = await _fetch_from_arxiv(period=period, page=page, limit=limit)

    settings = get_settings()
    await set_papers_cache(
        period,
        page,
        limit,
        response.model_dump(by_alias=True, mode="json"),
        ttl_hours=settings.arxiv_cache_ttl_hours,
    )
    return response


async def _fetch_from_arxiv(period: str, page: int, limit: int) -> PapersListResponse:
    days = PERIOD_DAYS[period]
    now = datetime.now(timezone.utc)
    end = now.strftime("%Y%m%d%H%M")
    start_dt = (now - timedelta(days=days)).strftime("%Y%m%d%H%M")

    # arXiv expects literal `+`, `[`, `]`, `:` in search_query — httpx's params
    # would percent-encode them, so we build the query string ourselves.
    cat_clause = "+OR+".join(f"cat:{c}" for c in CATEGORIES)
    search_query = f"({cat_clause})+AND+submittedDate:[{start_dt}+TO+{end}]"
    url = (
        f"{ARXIV_API_URL}?search_query={search_query}"
        f"&start={(page - 1) * limit}"
        f"&max_results={limit}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )

    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error(f"arXiv upstream error: {exc}")
        raise APIError(502, "UPSTREAM_ERROR", f"arXiv API call failed: {exc}")

    try:
        papers, total = _parse_atom_feed(resp.text)
    except ET.ParseError as exc:
        logger.error(f"Failed to parse arXiv response: {exc}")
        raise APIError(502, "UPSTREAM_ERROR", "Malformed response from arXiv")

    # Paper.id == arxivId so the frontend can directly use it as the API key
    # for /analyze_paper and /generate_ppt without an extra resolution step.
    for p in papers:
        if p.arxiv_id:
            p.id = p.arxiv_id

    pagination = Pagination(
        page=page,
        limit=limit,
        total_count=total,
        total_pages=max(1, (total + limit - 1) // limit),
    )

    return PapersListResponse(
        papers=papers,
        pagination=pagination,
        cached_at=now.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    )


def _parse_atom_feed(xml_text: str) -> tuple[List[Paper], int]:
    root = ET.fromstring(xml_text)
    total_node = root.find("opensearch:totalResults", NS)
    total = int(total_node.text) if total_node is not None and total_node.text else 0

    papers: List[Paper] = []
    for entry in root.findall("atom:entry", NS):
        paper = _parse_entry(entry)
        if paper is not None:
            papers.append(paper)
    return papers, total


def _parse_entry(entry: ET.Element) -> Paper | None:
    id_node = entry.find("atom:id", NS)
    title_node = entry.find("atom:title", NS)
    summary_node = entry.find("atom:summary", NS)
    published_node = entry.find("atom:published", NS)
    if None in (id_node, title_node, summary_node, published_node):
        return None

    arxiv_url = (id_node.text or "").strip()
    # arxiv_url looks like "http://arxiv.org/abs/2510.21867v1"
    arxiv_id = arxiv_url.rsplit("/", 1)[-1] if arxiv_url else ""

    title = " ".join((title_node.text or "").split())
    abstract = " ".join((summary_node.text or "").split())
    publication_date = (published_node.text or "")[:10]

    authors = [
        " ".join((a.findtext("atom:name", default="", namespaces=NS) or "").split())
        for a in entry.findall("atom:author", NS)
    ]
    authors = [a for a in authors if a]

    categories = [c.attrib.get("term", "") for c in entry.findall("atom:category", NS)]
    primary = entry.find("arxiv:primary_category", NS)
    primary_term = (
        primary.attrib.get("term", "")
        if primary is not None
        else (categories[0] if categories else "")
    )
    field = FIELD_DISPLAY.get(primary_term, primary_term or "Computer Science")

    pdf_url = None
    for link in entry.findall("atom:link", NS):
        if link.attrib.get("title") == "pdf":
            pdf_url = link.attrib.get("href")
            break
    if not pdf_url and arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # arXiv doesn't give explicit keywords; surface secondary categories as the
    # closest equivalent. Strip the primary so the user sees variety.
    keywords = [c for c in categories if c and c != primary_term][:5]
    if not keywords and primary_term:
        keywords = [primary_term]

    return Paper(
        id="placeholder",  # overwritten by caller with {period}-{nnnn}
        title=title,
        authors=authors,
        abstract=abstract,
        arxiv_id=arxiv_id,
        uploaded_file_id=None,
        field=field,
        keywords=keywords,
        publication_date=publication_date,
        pdf_url=pdf_url,
        arxiv_url=arxiv_url,
        source="arxiv",
    )
