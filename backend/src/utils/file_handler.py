"""
File handling utilities for reading and writing paper materials.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_paper_materials(paper_dir: Path) -> Tuple[str, Dict, List[str], str]:
    """Load paper materials from a directory.

    Expected directory structure:
    paper_dir/
        {paper_id}.md          # Paper markdown
        {paper_id}_meta.json   # Paper metadata
        *.jpeg / *.png         # Images

    Args:
        paper_dir: Path to paper directory

    Returns:
        Tuple of (paper_md, paper_meta, image_paths, paper_id)

    Raises:
        FileNotFoundError: If required files are missing
        ValueError: If directory structure is invalid
    """
    paper_dir = Path(paper_dir)
    if not paper_dir.exists() or not paper_dir.is_dir():
        raise FileNotFoundError(f"Paper directory not found: {paper_dir}")

    # Find the markdown file
    md_files = list(paper_dir.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No markdown file found in {paper_dir}")
    if len(md_files) > 1:
        logger.warning(f"Multiple markdown files found, using first: {md_files[0]}")

    md_file = md_files[0]
    paper_id = md_file.stem

    # Read markdown content
    logger.info(f"Loading paper markdown: {md_file}")
    with open(md_file, "r", encoding="utf-8") as f:
        paper_md = f.read()

    # Read metadata JSON
    meta_file = paper_dir / f"{paper_id}_meta.json"
    if not meta_file.exists():
        logger.warning(f"Metadata file not found: {meta_file}, using empty dict")
        paper_meta = {}
    else:
        logger.info(f"Loading paper metadata: {meta_file}")
        with open(meta_file, "r", encoding="utf-8") as f:
            paper_meta = json.load(f)

    # Find all image files
    image_extensions = ["*.jpeg", "*.jpg", "*.png", "*.gif"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(paper_dir.glob(ext))

    image_paths_str = [str(p) for p in image_paths]
    logger.info(f"Found {len(image_paths_str)} images in {paper_dir}")

    return paper_md, paper_meta, image_paths_str, paper_id


def save_output(
    output_dir: Path,
    paper_id: str,
    p1_markdown: str = None,
    p2_document: str = None,
    p3_article: str = None,
    p4_script: str = None,
    gamma_ppt_url: str = None,
    metadata: Dict = None,
) -> None:
    """Save workflow outputs to disk.

    Args:
        output_dir: Base output directory
        paper_id: Paper identifier (used for subdirectory)
        p1_markdown: P1 Gamma markdown output
        p2_document: P2 deep analysis document
        p3_article: P3 technical article
        p4_script: P4 speech script
        gamma_ppt_url: URL to generated Gamma PPT
        metadata: Additional metadata to save
    """
    paper_output_dir = output_dir / paper_id
    paper_output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Saving outputs to {paper_output_dir}")

    # Save each output if provided
    if p1_markdown:
        p1_file = paper_output_dir / "p1_gamma_markdown.md"
        p1_file.write_text(p1_markdown, encoding="utf-8")
        logger.info(f"Saved P1 output to {p1_file}")

    if p2_document:
        p2_file = paper_output_dir / "p2_deep_analysis.md"
        p2_file.write_text(p2_document, encoding="utf-8")
        logger.info(f"Saved P2 output to {p2_file}")

    if p3_article:
        p3_file = paper_output_dir / "p3_tech_article.md"
        p3_file.write_text(p3_article, encoding="utf-8")
        logger.info(f"Saved P3 output to {p3_file}")

    if p4_script:
        p4_file = paper_output_dir / "p4_speech_script.md"
        p4_file.write_text(p4_script, encoding="utf-8")
        logger.info(f"Saved P4 output to {p4_file}")

    # Save metadata including Gamma PPT URL
    if metadata or gamma_ppt_url:
        meta = metadata or {}
        if gamma_ppt_url:
            meta["gamma_ppt_url"] = gamma_ppt_url

        meta_file = paper_output_dir / "metadata.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved metadata to {meta_file}")


def read_prompt_template(prompt_name: str) -> str:
    """Read a prompt template from the docs directory.

    Args:
        prompt_name: Name of the prompt (e.g., 'P1', 'P2', 'P3', 'P4')

    Returns:
        Prompt template content

    Raises:
        FileNotFoundError: If prompt file not found
    """
    # Assuming docs/ is at project root
    docs_dir = Path(__file__).parent.parent.parent / "docs"
    prompt_file = docs_dir / f"Prompt-{prompt_name}.md"

    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_file}")

    logger.info(f"Loading prompt template: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8")
