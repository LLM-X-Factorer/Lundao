"""Unified error responses.

Every non-2xx response is wrapped as:
    {"error": {"code": "<stable enum>", "message": "<human msg>", "details": {...}}}

`code` is the stable identifier the frontend branches on; `message` is for
humans; `details` is optional context.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class APIError(Exception):
    """Raise this from routes to produce a standardized error response."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}


def _make_response(
    status_code: int, code: str, message: str, details: Optional[dict[str, Any]] = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details or {}}},
    )


async def _api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    return _make_response(exc.status_code, exc.code, exc.message, exc.details)


async def _http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        413: "PAYLOAD_TOO_LARGE",
        415: "UNSUPPORTED_MEDIA_TYPE",
        429: "RATE_LIMITED",
        500: "INTERNAL_ERROR",
        501: "NOT_IMPLEMENTED",
        502: "UPSTREAM_ERROR",
        503: "SERVICE_UNAVAILABLE",
    }
    code = code_map.get(exc.status_code, f"HTTP_{exc.status_code}")
    return _make_response(exc.status_code, code, str(exc.detail))


async def _validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _make_response(
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST_INVALID_PARAM",
        "Request validation failed",
        {"errors": exc.errors()},
    )


async def _generic_handler(request: Request, exc: Exception) -> JSONResponse:
    return _make_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "INTERNAL_ERROR",
        "An unexpected error occurred",
        {"type": type(exc).__name__},
    )


def register_error_handlers(app: FastAPI) -> None:
    """Wire all standard exception handlers onto the FastAPI app."""
    app.add_exception_handler(APIError, _api_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_handler)
    app.add_exception_handler(Exception, _generic_handler)
