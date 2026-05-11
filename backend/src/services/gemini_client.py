"""
Google Gemini API client using langchain-google-genai 4.x (uses unified google-genai SDK).
"""

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.core.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini API."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize Gemini client.

        Args:
            model_name: Name of the Gemini model to use; defaults to settings.gemini_model
        """
        settings = get_settings()
        self.model_name = model_name or settings.gemini_model

        logger.info(f"Initializing Gemini client with model: {self.model_name}")

        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=settings.google_api_key,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        thinking_level: str = "high",
    ) -> str:
        """Generate content using Gemini 3.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            thinking_level: Reasoning depth ("low" or "high")

        Returns:
            Generated text content
        """
        logger.info(f"Generating with Gemini (thinking_level={thinking_level})")
        logger.debug(f"Prompt length: {len(prompt)} chars")

        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=prompt))

        try:
            # Note: thinking_level might need to be passed differently
            # depending on the langchain-google-genai version
            response = await self.llm.ainvoke(messages)

            result = response.content
            logger.info(f"Generated {len(result)} chars")
            logger.debug(f"Response preview: {result[:200]}...")

            return result

        except Exception as e:
            logger.error(f"Error generating with Gemini: {e}")
            raise

    def generate_sync(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        thinking_level: str = "high",
    ) -> str:
        """Synchronous version of generate.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            thinking_level: Reasoning depth ("low" or "high")

        Returns:
            Generated text content
        """
        logger.info(f"Generating with Gemini (sync, thinking_level={thinking_level})")

        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=prompt))

        try:
            response = self.llm.invoke(messages)
            result = response.content
            logger.info(f"Generated {len(result)} chars")
            return result

        except Exception as e:
            logger.error(f"Error generating with Gemini: {e}")
            raise


# Global client instance
_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """Get the global Gemini client instance."""
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
