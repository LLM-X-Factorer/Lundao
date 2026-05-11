"""
P1 Agent: Generate Gamma API-ready PPT blueprint markdown.
"""

from typing import Dict, List

from src.agents.base import BaseAgent
from src.utils.prompts import build_p1_prompt


class P1Agent(BaseAgent):
    """Agent for executing Prompt P1: PPT Blueprint Generation."""

    def __init__(self):
        """Initialize P1 agent."""
        super().__init__(name="P1")

    def build_prompt(
        self,
        paper_md: str,
        paper_meta: Dict,
        image_paths: List[str],
        image_urls: Dict[str, str],
    ) -> str:
        """Build P1 prompt.

        Args:
            paper_md: Paper markdown content
            paper_meta: Paper metadata
            image_paths: List of image paths
            image_urls: Image filename to URL mapping

        Returns:
            Complete P1 prompt
        """
        return build_p1_prompt(paper_md, paper_meta, image_paths, image_urls)
