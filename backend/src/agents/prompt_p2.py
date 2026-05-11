"""
P2 Agent: Generate deep analysis document.
"""

from src.agents.base import BaseAgent
from src.utils.prompts import build_p2_prompt


class P2Agent(BaseAgent):
    """Agent for executing Prompt P2: Deep Analysis Document Generation."""

    def __init__(self):
        """Initialize P2 agent."""
        super().__init__(name="P2")

    def build_prompt(self, p1_markdown: str, paper_md: str) -> str:
        """Build P2 prompt.

        Args:
            p1_markdown: P1 generated Gamma markdown
            paper_md: Original paper markdown

        Returns:
            Complete P2 prompt
        """
        return build_p2_prompt(p1_markdown, paper_md)
