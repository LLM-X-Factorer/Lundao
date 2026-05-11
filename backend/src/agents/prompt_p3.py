"""
P3 Agent: Generate technical experience article.
"""

from src.agents.base import BaseAgent
from src.utils.prompts import build_p3_prompt


class P3Agent(BaseAgent):
    """Agent for executing Prompt P3: Technical Article Generation."""

    def __init__(self):
        """Initialize P3 agent."""
        super().__init__(name="P3")

    def build_prompt(self, p1_markdown: str, paper_md: str) -> str:
        """Build P3 prompt.

        Args:
            p1_markdown: P1 generated Gamma markdown
            paper_md: Original paper markdown

        Returns:
            Complete P3 prompt
        """
        return build_p3_prompt(p1_markdown, paper_md)
