"""
Configuration management using Pydantic Settings.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Gemini API Configuration
    google_api_key: str = Field(..., description="Google Gemini API Key")
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model name (gemini-2.5-flash recommended; gemini-3-pro-preview for max quality)",
    )

    # Gamma API Configuration
    gamma_api_key: str = Field(..., description="Gamma API Key")
    gamma_export_format: Optional[str] = Field(
        default="pdf", description="Export format for Gamma presentations (pdf or pptx)"
    )

    # Image Server Configuration
    image_server_host: str = Field(default="localhost", description="Image server host")
    image_server_port: int = Field(default=8001, description="Image server port")
    image_server_base_url: Optional[str] = Field(
        default=None, description="Image server base URL (auto-generated if not set)"
    )

    # API Server Configuration
    api_host: str = Field(default="0.0.0.0", description="API server host")
    api_port: int = Field(default=8000, description="API server port")

    # Output Configuration
    output_dir: Path = Field(default=Path("./outputs"), description="Output directory path")
    uploads_dir: Path = Field(default=Path("./uploads"), description="PDF upload directory")

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")

    # LangGraph Configuration
    langgraph_checkpoint_dir: Path = Field(
        default=Path("./checkpoints"), description="LangGraph checkpoint directory"
    )

    # Database Configuration
    database_path: Path = Field(default=Path("./lundao.db"), description="SQLite database file")

    # Task Queue Configuration
    max_concurrent_tasks: int = Field(default=2, description="Max concurrent PPT tasks")
    arxiv_cache_ttl_hours: int = Field(default=24, description="arXiv list cache TTL")
    upload_ttl_hours: int = Field(default=24, description="Uploaded PDF retention before cleanup")
    task_archive_days: int = Field(
        default=7, description="Days before completed task outputs archived"
    )

    # Upload Constraints
    max_upload_size_mb: int = Field(default=20, description="Max PDF upload size in MB")

    @property
    def image_server_url(self) -> str:
        """Get the full image server URL."""
        if self.image_server_base_url:
            return self.image_server_base_url
        return f"http://{self.image_server_host}:{self.image_server_port}"

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.langgraph_checkpoint_dir.mkdir(parents=True, exist_ok=True)
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_directories()
    return _settings


def reset_settings() -> None:
    """Reset the global settings instance (mainly for testing)."""
    global _settings
    _settings = None
