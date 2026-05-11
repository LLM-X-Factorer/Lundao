"""
Logging configuration using loguru.
"""

import sys

from loguru import logger

from src.core.config import get_settings


def setup_logger() -> None:
    """Configure the logger based on settings."""
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # Add file handler if configured
    if settings.log_file:
        settings.log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(settings.log_file),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=settings.log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
        )

    logger.info(f"Logger initialized with level: {settings.log_level}")


def get_logger(name: str):
    """Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logger.bind(name=name)
