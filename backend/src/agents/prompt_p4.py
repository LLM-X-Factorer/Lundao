"""
P4 Agent: Generate speech script.
"""

from src.agents.base import BaseAgent
from src.utils.prompts import build_p4_prompt


class P4Agent(BaseAgent):
    """Agent for executing Prompt P4: Speech Script Generation."""

    def __init__(self):
        """Initialize P4 agent."""
        super().__init__(name="P4")

    def build_prompt(self, p1_markdown: str, paper_md: str) -> str:
        """Build P4 prompt.

        Args:
            p1_markdown: P1 generated Gamma markdown
            paper_md: Original paper markdown

        Returns:
            Complete P4 prompt
        """
        return build_p4_prompt(p1_markdown, paper_md)
