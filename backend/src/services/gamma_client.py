"""
Gamma API client for generating presentations.
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, Optional

import httpx

from src.core.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GammaClient:
    """Client for interacting with Gamma API."""

    def __init__(self):
        """Initialize Gamma client."""
        settings = get_settings()
        self.api_key = settings.gamma_api_key

        # Correct API endpoints based on documentation
        self.base_url = "https://public-api.gamma.app"
        self.generations_url = f"{self.base_url}/v1.0/generations"

        self.timeout = httpx.Timeout(300.0, connect=60.0)  # 5 min timeout

        logger.info(f"Initialized Gamma client with base URL: {self.base_url}")

    async def create_generation(
        self,
        input_text: str,
        text_mode: str = "generate",
        card_split: str = "inputTextBreaks",
        num_cards: Optional[int] = None,
        export_as: Optional[str] = None,
        additional_params: Optional[Dict] = None,
    ) -> str:
        """Create a generation request (Step 1).

        Args:
            input_text: Markdown text with --- separators
            text_mode: "generate" (expand), "condense", or "preserve"
            card_split: "inputTextBreaks" or "auto"
            num_cards: Number of cards (only used when card_split="auto")
            export_as: Export format - "pdf" or "pptx" (optional)
            additional_params: Additional API parameters (themeId, tone, etc.)

        Returns:
            generationId string

        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        logger.info(f"Creating Gamma generation (text_mode={text_mode}, card_split={card_split})")
        logger.debug(f"Input text length: {len(input_text)} chars")

        # Build request payload
        payload = {
            "inputText": input_text,
            "textMode": text_mode,
            "cardSplit": card_split,
        }

        # Add optional parameters
        if num_cards and card_split == "auto":
            payload["numCards"] = num_cards

        if export_as:
            if export_as not in ["pdf", "pptx"]:
                raise ValueError(f"export_as must be 'pdf' or 'pptx', got '{export_as}'")
            payload["exportAs"] = export_as

        if additional_params:
            payload.update(additional_params)

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    self.generations_url,
                    json=payload,
                    headers=headers,
                )

                response.raise_for_status()
                result = response.json()

                generation_id = result.get("generationId")
                if not generation_id:
                    raise ValueError(f"No generationId in response: {result}")

                logger.info(f"Generation created: {generation_id}")
                return generation_id

            except httpx.HTTPStatusError as e:
                logger.error(f"Gamma API HTTP error: {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")
                raise

            except Exception as e:
                logger.error(f"Gamma API error: {e}")
                raise

    async def get_generation_status(self, generation_id: str) -> Dict:
        """Get generation status and result (Step 2).

        Args:
            generation_id: The generation ID from create_generation

        Returns:
            Generation status dict with gammaUrl, status, etc.

        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        url = f"{self.generations_url}/{generation_id}"
        headers = {
            "X-API-KEY": self.api_key,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                result = response.json()

                logger.debug(f"Generation status: {result.get('status')}")
                return result

            except httpx.HTTPStatusError as e:
                logger.error(f"Gamma API HTTP error: {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")
                raise

            except Exception as e:
                logger.error(f"Gamma API error: {e}")
                raise

    async def generate_presentation(
        self,
        input_text: str,
        card_split: str = "inputTextBreaks",
        num_cards: Optional[int] = None,
        export_as: Optional[str] = None,
        max_wait_time: int = 300,
        poll_interval: int = 5,
    ) -> Dict:
        """Generate a presentation and wait for completion (convenience method).

        Args:
            input_text: Markdown text with --- separators
            card_split: "inputTextBreaks" or "auto"
            num_cards: Number of cards (only used when card_split="auto")
            export_as: Export format - "pdf" or "pptx" (optional)
            max_wait_time: Maximum wait time in seconds
            poll_interval: Polling interval in seconds

        Returns:
            Final generation result with gammaUrl

        Raises:
            TimeoutError: If generation takes too long
            httpx.HTTPStatusError: If API request fails
        """
        # Step 1: Create generation
        generation_id = await self.create_generation(
            input_text=input_text,
            text_mode="generate",
            card_split=card_split,
            num_cards=num_cards,
            export_as=export_as,
        )

        # Step 2: Poll for completion
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            result = await self.get_generation_status(generation_id)

            status = result.get("status")
            logger.info(f"Generation {generation_id} status: {status}")

            if status == "completed":
                gamma_url = result.get("gammaUrl")
                logger.info(f"Gamma presentation completed: {gamma_url}")
                return result

            elif status == "failed":
                error_msg = result.get("error", "Unknown error")
                raise RuntimeError(f"Generation failed: {error_msg}")

            # Wait before polling again
            await asyncio.sleep(poll_interval)

        raise TimeoutError(f"Generation {generation_id} did not complete within {max_wait_time}s")

    def generate_presentation_sync(
        self,
        input_text: str,
        card_split: str = "inputTextBreaks",
        num_cards: Optional[int] = None,
        max_wait_time: int = 300,
        poll_interval: int = 5,
    ) -> Dict:
        """Synchronous version of generate_presentation.

        Args:
            input_text: Markdown text with --- separators
            card_split: "inputTextBreaks" or "auto"
            num_cards: Number of cards (only used when card_split="auto")
            max_wait_time: Maximum wait time in seconds
            poll_interval: Polling interval in seconds

        Returns:
            Final generation result with gammaUrl
        """
        # Run async method in sync context
        return asyncio.run(
            self.generate_presentation(
                input_text=input_text,
                card_split=card_split,
                num_cards=num_cards,
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
            )
        )

    async def download_export(
        self,
        export_url: str,
        output_path: Path,
    ) -> Path:
        """Download exported file from Gamma API.

        Args:
            export_url: The export URL from generation result
            output_path: Path to save the downloaded file

        Returns:
            Path to the downloaded file

        Raises:
            httpx.HTTPError: If download fails
        """
        logger.info(f"Downloading export from: {export_url}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(export_url)
                response.raise_for_status()

                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Write file
                with open(output_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Export downloaded to: {output_path}")
                return output_path

            except Exception as e:
                logger.error(f"Failed to download export: {e}")
                raise


# Global client instance
_client: Optional[GammaClient] = None


def get_gamma_client() -> GammaClient:
    """Get the global Gamma client instance."""
    global _client
    if _client is None:
        _client = GammaClient()
    return _client
