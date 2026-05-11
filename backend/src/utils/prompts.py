"""
Prompt template management and formatting.
"""

from pathlib import Path
from typing import Dict, List

from src.utils.file_handler import read_prompt_template
from src.utils.logger import get_logger

logger = get_logger(__name__)


def format_paper_images_list(image_paths: List[str], image_urls: Dict[str, str]) -> str:
    """Format the list of paper images with their URLs.

    Args:
        image_paths: List of local image paths
        image_urls: Mapping from image filename to HTTP URL

    Returns:
        Formatted string listing images
    """
    if not image_paths:
        return "No images provided."

    lines = ["**Available Images:**\n"]
    for img_path in image_paths:
        filename = Path(img_path).name
        url = image_urls.get(filename, "[URL not available]")
        lines.append(f"- {filename}: {url}")

    return "\n".join(lines)


def build_p1_prompt(
    paper_md: str,
    paper_meta: Dict,
    image_paths: List[str],
    image_urls: Dict[str, str],
) -> str:
    """Build the complete P1 prompt.

    Args:
        paper_md: Paper markdown content
        paper_meta: Paper metadata
        image_paths: List of image paths
        image_urls: Image filename to URL mapping

    Returns:
        Complete P1 prompt
    """
    template = read_prompt_template("P1")

    # Format metadata
    meta_str = "\n".join([f"- {k}: {v}" for k, v in paper_meta.items()])

    # Format images
    images_str = format_paper_images_list(image_paths, image_urls)

    # Build full prompt
    full_prompt = f"""{template}

---

## Provided Materials

### Paper Metadata
{meta_str}

### Paper Content
{paper_md}

### Images
{images_str}

---

Please generate the Gamma API-ready Markdown following the format specified above.
"""

    return full_prompt


def build_p2_prompt(p1_markdown: str, paper_md: str) -> str:
    """Build the complete P2 prompt.

    Args:
        p1_markdown: P1 generated Gamma markdown
        paper_md: Original paper markdown

    Returns:
        Complete P2 prompt
    """
    template = read_prompt_template("P2")

    full_prompt = f"""{template}

---

## Provided Materials

### PPT Blueprint (from P1)
{p1_markdown}

### Original Paper Content
{paper_md}

---

Please generate the deep analysis document following the requirements above.
"""

    return full_prompt


def build_p3_prompt(p1_markdown: str, paper_md: str) -> str:
    """Build the complete P3 prompt.

    Args:
        p1_markdown: P1 generated Gamma markdown
        paper_md: Original paper markdown

    Returns:
        Complete P3 prompt
    """
    template = read_prompt_template("P3")

    full_prompt = f"""{template}

---

## Provided Materials

### PPT Blueprint (from P1)
{p1_markdown}

### Original Paper Content
{paper_md}

---

Please generate the technical experience article following the style requirements above.
"""

    return full_prompt


def build_p4_prompt(p1_markdown: str, paper_md: str) -> str:
    """Build the complete P4 prompt.

    Args:
        p1_markdown: P1 generated Gamma markdown
        paper_md: Original paper markdown

    Returns:
        Complete P4 prompt
    """
    template = read_prompt_template("P4")

    full_prompt = f"""{template}

---

## Provided Materials

### PPT Blueprint (from P1)
{p1_markdown}

### Original Paper Content
{paper_md}

---

Please generate the speech script following the presentation style requirements above.
"""

    return full_prompt
