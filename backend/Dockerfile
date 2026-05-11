# Lundao backend — FastAPI + LangGraph
#
# Single-stage uv image: small enough, simple to maintain. The `uv` binary +
# Python 3.12 are pre-installed in the base image.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Faster dependency installs in CI and Docker layers.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies first (cached unless lockfile changes).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy source after deps so source edits don't bust the deps layer.
COPY src ./src

# Re-sync to install the project itself (entry points etc.).
RUN uv sync --frozen --no-dev

# Make .venv binaries available without `uv run`.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Simple liveness probe.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)" || exit 1

# Use uvicorn directly so we don't pick up the `reload=True` set in src.api.main.run_server().
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
