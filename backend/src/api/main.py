"""FastAPI application for the Lundao backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.errors import register_error_handlers
from src.api.routes import router
from src.core.config import get_settings
from src.db.connection import close_db, init_db
from src.services.task_queue import start_workers, stop_workers
from src.utils.logger import get_logger, setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB + start workers. Shutdown: stop workers + close DB."""
    setup_logger()
    logger = get_logger(__name__)
    logger.info("Starting Lundao API server")

    await init_db()
    await start_workers()

    yield

    logger.info("Shutting down Lundao API server")
    await stop_workers()
    await close_db()


app = FastAPI(
    title="Lundao API",
    description="Academic paper presentation automation API",
    version="0.2.0",
    lifespan=lifespan,
)

# CORS — dev allows any origin; tighten via env in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized error responses
register_error_handlers(app)

# All endpoints live under /api (no version prefix; v2 will be /api/v2 if needed).
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root: links to the OpenAPI docs."""
    return {"name": "Lundao API", "version": "0.2.0", "docs": "/docs"}


def run_server():
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )


if __name__ == "__main__":
    run_server()
