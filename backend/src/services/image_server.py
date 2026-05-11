"""
Local image HTTP server for serving paper images to Gamma API.
"""

import multiprocessing
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_image_server_app(image_dir: Path) -> FastAPI:
    """Create a FastAPI app to serve images.

    Args:
        image_dir: Directory containing images

    Returns:
        FastAPI application
    """
    app = FastAPI(title="Paper Image Server")

    # Mount the image directory as static files
    app.mount("/images", StaticFiles(directory=str(image_dir)), name="images")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


def run_image_server(image_dir: str, host: str, port: int):
    """Run the image server (used in subprocess).

    Args:
        image_dir: Directory containing images
        host: Server host
        port: Server port
    """
    app = create_image_server_app(Path(image_dir))
    uvicorn.run(app, host=host, port=port, log_level="warning")


class ImageServer:
    """Manager for the local image HTTP server."""

    def __init__(self):
        """Initialize image server manager."""
        self.process: Optional[multiprocessing.Process] = None
        self.image_dir: Optional[Path] = None
        self.host: str = ""
        self.port: int = 0

    def start(self, image_paths: List[str]) -> Dict[str, str]:
        """Start the image server and return URL mappings.

        Args:
            image_paths: List of local image file paths

        Returns:
            Dictionary mapping image filename to HTTP URL

        Raises:
            RuntimeError: If server is already running or fails to start
        """
        if self.process and self.process.is_alive():
            raise RuntimeError("Image server is already running")

        if not image_paths:
            logger.warning("No images provided, skipping image server startup")
            return {}

        settings = get_settings()

        # Get the common directory of all images (assume they're in the same dir)
        first_image = Path(image_paths[0])
        self.image_dir = first_image.parent

        self.host = settings.image_server_host
        self.port = settings.image_server_port

        logger.info(
            f"Starting image server for directory: {self.image_dir} on {self.host}:{self.port}"
        )

        # Start server in subprocess
        self.process = multiprocessing.Process(
            target=run_image_server,
            args=(str(self.image_dir), self.host, self.port),
            daemon=True,
        )
        self.process.start()

        # Wait a bit for server to start
        time.sleep(2)

        if not self.process.is_alive():
            raise RuntimeError("Image server failed to start")

        # Generate URL mappings
        base_url = settings.image_server_url
        image_urls = {}

        for img_path in image_paths:
            filename = Path(img_path).name
            url = f"{base_url}/images/{filename}"
            image_urls[filename] = url

        logger.info(f"Image server started, serving {len(image_urls)} images")
        logger.debug(f"Image URLs: {image_urls}")

        return image_urls

    def stop(self):
        """Stop the image server."""
        if self.process and self.process.is_alive():
            logger.info("Stopping image server")
            self.process.terminate()
            self.process.join(timeout=5)

            if self.process.is_alive():
                logger.warning("Image server did not terminate gracefully, killing")
                self.process.kill()

            self.process = None
            logger.info("Image server stopped")

    def __del__(self):
        """Cleanup: ensure server is stopped."""
        self.stop()


async def start_image_server(image_paths: List[str]) -> Tuple[ImageServer, Dict[str, str]]:
    """Start image server and return server instance and URL mappings.

    Args:
        image_paths: List of local image file paths

    Returns:
        Tuple of (ImageServer instance, URL mappings)
    """
    server = ImageServer()
    urls = server.start(image_paths)
    return server, urls


def stop_image_server(server: ImageServer):
    """Stop the image server.

    Args:
        server: ImageServer instance to stop
    """
    if server:
        server.stop()
