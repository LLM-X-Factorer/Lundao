.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend build build-frontend test test-backend lint lint-backend lint-frontend typecheck typecheck-backend docker-build docker-up docker-down docker-logs clean

.DEFAULT_GOAL := help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# === Install ===

install: install-backend install-frontend  ## Install all dependencies (backend + frontend)

install-backend:  ## Install backend Python dependencies (uv)
	cd backend && uv sync

install-frontend:  ## Install frontend Node dependencies (npm)
	cd frontend && npm install

# === Dev ===

dev:  ## Start backend (:8000) and frontend (:5173) in parallel
	@echo "Starting backend and frontend (Ctrl+C stops both)..."
	@$(MAKE) -j 2 dev-backend dev-frontend

dev-backend:  ## Start backend dev server (FastAPI on :8000)
	cd backend && uv run python -m src.api.main

dev-frontend:  ## Start frontend dev server (Vite on :5173)
	cd frontend && npm run dev

# === Build ===

build: build-frontend  ## Production build (frontend only — backend doesn't build)

build-frontend:  ## Build frontend for production
	cd frontend && npm run build

# === Test ===

test: test-backend  ## Run all tests

test-backend:  ## Run backend pytest
	cd backend && uv run pytest

# === Lint ===

lint: lint-backend lint-frontend  ## Lint both projects (formatting + style)

lint-backend:  ## Format + style-check backend (black + ruff)
	cd backend && uv run black --check src/ && uv run ruff check src/

lint-frontend:  ## Lint frontend (ESLint with auto-fix)
	cd frontend && npm run lint

typecheck: typecheck-backend  ## Type-check (mypy) — optional, has pre-existing issues in legacy modules

typecheck-backend:  ## Run mypy on backend
	cd backend && uv run mypy src/

# === Docker (production-ish local deployment) ===

docker-build:  ## Build both Docker images
	docker compose build

docker-up:  ## Start backend + frontend via docker compose (detached)
	docker compose up -d

docker-down:  ## Stop and remove docker compose services
	docker compose down

docker-logs:  ## Tail docker compose logs
	docker compose logs -f

# === Clean ===

clean:  ## Remove build artifacts and caches
	cd backend && rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	cd frontend && rm -rf dist .vite node_modules/.cache
