"""PDF upload handling.

Validates MIME type and size, persists to settings.uploads_dir, records
metadata in SQLite uploads table. Returns the public UploadResponse schema.
"""

from __future__ import annotations

import uuid

from fastapi import UploadFile

from src.api.errors import APIError
from src.api.schemas import UploadResponse
from src.core.config import get_settings
from src.db.repositories import create_upload
from src.utils.logger import get_logger

logger = get_logger(__name__)

CHUNK_SIZE = 1024 * 1024  # 1 MB


async def save_uploaded_pdf(file: UploadFile) -> UploadResponse:
    settings = get_settings()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    if file.content_type and file.content_type != "application/pdf":
        raise APIError(
            415,
            "UNSUPPORTED_MEDIA_TYPE",
            f"Only application/pdf is accepted (got {file.content_type})",
        )

    file_id = str(uuid.uuid4())
    file_name = file.filename or f"upload-{file_id}.pdf"
    storage_path = settings.uploads_dir / f"{file_id}.pdf"

    total = 0
    try:
        with storage_path.open("wb") as out:
            while chunk := await file.read(CHUNK_SIZE):
                total += len(chunk)
                if total > max_bytes:
                    out.close()
                    storage_path.unlink(missing_ok=True)
                    raise APIError(
                        413,
                        "PAYLOAD_TOO_LARGE",
                        f"File exceeds {settings.max_upload_size_mb} MB limit",
                    )
                out.write(chunk)
    except APIError:
        raise
    except Exception as exc:
        storage_path.unlink(missing_ok=True)
        logger.exception(f"Failed to save uploaded PDF: {exc}")
        raise APIError(500, "INTERNAL_ERROR", "Failed to persist uploaded file")

    if total == 0:
        storage_path.unlink(missing_ok=True)
        raise APIError(400, "BAD_REQUEST_NO_FILE", "Uploaded file is empty")

    row = await create_upload(
        file_id=file_id,
        file_name=file_name,
        file_size=total,
        storage_path=str(storage_path),
        ttl_hours=settings.upload_ttl_hours,
    )

    logger.info(f"Uploaded {file_name} ({total} bytes) as {file_id}")
    return UploadResponse(
        file_id=row.id,
        file_name=row.file_name,
        file_size=row.file_size,
        uploaded_at=row.uploaded_at,
    )
