-- Lundao backend SQLite schema
-- All timestamps stored as ISO 8601 UTC strings for portability.

CREATE TABLE IF NOT EXISTS tasks (
    id              TEXT PRIMARY KEY,            -- UUIDv4
    paper_id        TEXT NOT NULL,               -- arxivId or fileId reference
    paper_title     TEXT NOT NULL,
    source          TEXT NOT NULL,               -- 'arxiv' | 'upload'
    status          TEXT NOT NULL,               -- 'queued' | 'generating' | 'completed' | 'failed'
    progress        INTEGER,                     -- 0-100, NULL when queued
    created_at      TEXT NOT NULL,               -- ISO 8601
    started_at      TEXT,
    completed_at    TEXT,
    download_url    TEXT,
    error_message   TEXT,
    retry_count     INTEGER NOT NULL DEFAULT 0,
    output_dir      TEXT                         -- relative path to outputs/{taskId}/
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);

CREATE TABLE IF NOT EXISTS papers_cache (
    cache_key       TEXT PRIMARY KEY,            -- '{period}:{page}:{limit}'
    period          TEXT NOT NULL,
    page            INTEGER NOT NULL,
    payload         TEXT NOT NULL,               -- JSON: {papers, pagination}
    cached_at       TEXT NOT NULL,               -- ISO 8601, used for TTL check
    expires_at      TEXT NOT NULL                -- cached_at + TTL
);

CREATE INDEX IF NOT EXISTS idx_papers_cache_expires ON papers_cache(expires_at);

CREATE TABLE IF NOT EXISTS analysis_cache (
    paper_key       TEXT PRIMARY KEY,            -- 'arxiv:{arxivId}' or 'upload:{fileId}'
    source          TEXT NOT NULL,               -- 'arxiv' | 'upload'
    status          TEXT NOT NULL,               -- 'pending' | 'completed' | 'failed'
    payload         TEXT,                        -- JSON: full Analysis object, NULL while pending
    error_message   TEXT,
    started_at      TEXT NOT NULL,
    completed_at    TEXT
);

CREATE TABLE IF NOT EXISTS uploads (
    id              TEXT PRIMARY KEY,            -- UUIDv4 fileId
    file_name       TEXT NOT NULL,
    file_size       INTEGER NOT NULL,
    md5             TEXT,
    storage_path    TEXT NOT NULL,               -- e.g. 'uploads/{fileId}.pdf'
    uploaded_at     TEXT NOT NULL,
    expires_at      TEXT NOT NULL                -- 24h after upload
);

CREATE INDEX IF NOT EXISTS idx_uploads_expires ON uploads(expires_at);
