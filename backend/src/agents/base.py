"""
Base agent class for prompt execution.
"""

from abc import ABC, abstractmethod

from src.services.gemini_client import get_gemini_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all prompt agents."""

    def __init__(self, name: str):
        """Initialize agent.

        Args:
            name: Agent name (e.g., "P1", "P2", etc.)
        """
        self.name = name
        self.gemini_client = get_gemini_client()
        logger.info(f"Initialized {self.name} agent")

    @abstractmethod
    def build_prompt(self, **kwargs) -> str:
        """Build the complete prompt for this agent.

        Returns:
            Complete prompt string
        """
        pass

    async def execute(self, **kwargs) -> str:
        """Execute the agent with given inputs.

        Args:
            **kwargs: Agent-specific input parameters

        Returns:
            Generated output text
        """
        logger.info(f"Executing {self.name} agent")

        # Build prompt
        prompt = self.build_prompt(**kwargs)

        # Generate with Gemini
        try:
            result = await self.gemini_client.generate(
                prompt=prompt,
                thinking_level="high",  # Use deep reasoning
            )

            logger.info(f"{self.name} agent completed successfully")
            return result

        except Exception as e:
            logger.error(f"{self.name} agent failed: {e}")
            raise

    def execute_sync(self, **kwargs) -> str:
        """Synchronous version of execute.

        Args:
            **kwargs: Agent-specific input parameters

        Returns:
            Generated output text
        """
        logger.info(f"Executing {self.name} agent (sync)")

        prompt = self.build_prompt(**kwargs)

        try:
            result = self.gemini_client.generate_sync(
                prompt=prompt,
                thinking_level="high",
            )

            logger.info(f"{self.name} agent completed successfully")
            return result

        except Exception as e:
            logger.error(f"{self.name} agent failed: {e}")
            raise
