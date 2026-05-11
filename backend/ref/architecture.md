# System Architecture

## Overview

Lundao Backend P2P3 is an automated academic paper processing system that transforms research papers into multiple output formats using AI agents orchestrated by LangGraph.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Input Layer                             │
│  Paper Markdown + Images + Metadata (JSON)                  │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                  LangGraph Workflow                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 1. prepare_images (Image Server)                     │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │ 2. execute_p1 (Gemini 3 + Prompt-P1)                 │   │
│  │    → Generate Gamma PPT Markdown                     │   │
│  └─────┬──────────────────────────────────────────┬─────┘   │
│        │                                           │         │
│  ┌─────▼─────────┐  ┌──────────┐  ┌──────────┐  ┌▼─────┐   │
│  │ 3a. call_gamma│  │3b. P2    │  │3c. P3    │  │3d. P4│   │
│  │  (Gamma API)  │  │(Analysis)│  │(Article) │  │(Scrpt)│   │
│  │  + Download   │  │          │  │          │  │      │   │
│  └────────┬──────┘  └────┬─────┘  └────┬─────┘  └──┬───┘   │
│           │              │             │            │       │
│  ┌────────▼──────────────▼─────────────▼────────────▼────┐  │
│  │ 4. finalize (Cleanup + Summary)                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                    Output Layer                              │
│  • p1_gamma_markdown.md                                     │
│  • gamma_presentation.pdf (Downloaded)                       │
│  • p2_deep_analysis.md                                      │
│  • p3_tech_article.md                                       │
│  • p4_speech_script.md                                      │
│  • metadata.json                                            │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Workflow Engine (LangGraph)
- **Location**: `src/core/workflow.py`
- **Purpose**: Orchestrates the entire pipeline with 7 nodes
- **State Management**: `src/core/state.py` - TypedDict with annotated merge strategies
- **Execution**: Parallel execution after P1 (P2, P3, P4, Gamma API run concurrently)

### 2. AI Agents
- **Base Agent**: `src/agents/base.py` - Abstract agent class
- **P1 Agent**: `src/agents/prompt_p1.py` - Gamma PPT blueprint generator
- **P2 Agent**: `src/agents/prompt_p2.py` - Deep analysis document
- **P3 Agent**: `src/agents/prompt_p3.py` - Technical article
- **P4 Agent**: `src/agents/prompt_p4.py` - Speech script

### 3. External Services

#### Gemini 3 API
- **Client**: `src/services/gemini_client.py`
- **Model**: `gemini-2.0-flash-thinking-exp`
- **Features**: 1M token context, thinking mode, multi-modal support
- **Library**: `langchain-google-genai`

#### Gamma API
- **Client**: `src/services/gamma_client.py`
- **Endpoint**: `https://public-api.gamma.app/v1.0/generations`
- **Features**:
  - Two-step async generation (create → poll)
  - Export to PDF/PPTX
  - Automatic download
- **Authentication**: `X-API-KEY` header

#### Image Server
- **Server**: `src/services/image_server.py`
- **Purpose**: Temporary HTTP server for serving local images
- **Framework**: FastAPI + Uvicorn
- **Lifecycle**: Started before P1, stopped in finalize

### 4. Configuration
- **File**: `src/core/config.py`
- **Framework**: Pydantic Settings
- **Source**: `.env` file
- **Key Settings**:
  - `GOOGLE_API_KEY`: Gemini API key
  - `GAMMA_API_KEY`: Gamma API key
  - `GAMMA_EXPORT_FORMAT`: pdf or pptx
  - `IMAGE_SERVER_HOST`, `IMAGE_SERVER_PORT`
  - `OUTPUT_DIR`: Output directory path

### 5. Interfaces

#### CLI Interface
- **File**: `src/cli/main.py`
- **Framework**: Typer + Rich
- **Commands**:
  - `process <paper_dir>`: Process a paper
- **Features**: Progress bars, colored output, result tables

#### Web API Interface
- **File**: `src/api/main.py`
- **Framework**: FastAPI
- **Endpoints**:
  - `POST /process`: Process paper (async)
  - `GET /health`: Health check
- **Schemas**: `src/api/schemas.py`
- **Routes**: `src/api/routes.py`

## Data Flow

### Input Processing
1. Load paper materials from directory:
   - `{paper_id}.md`: Paper markdown content
   - `{paper_id}_meta.json`: Metadata
   - `*.jpeg`, `*.png`: Images
2. Create initial workflow state

### P1 Generation
1. Start image server on `localhost:8001`
2. Generate image URLs mapping
3. Load Prompt-P1 template
4. Call Gemini 3 with paper + images + prompt
5. Output: Gamma-compatible markdown with `---` card separators

### Parallel Execution
All run concurrently after P1:
- **Gamma API**: Create generation → Poll → Download PDF/PPTX
- **P2**: Generate deep analysis using P1 + original paper
- **P3**: Generate technical article using P1 + original paper
- **P4**: Generate speech script using P1 + original paper

### Finalization
1. Wait for all parallel tasks to complete
2. Stop image server
3. Save all outputs to disk
4. Generate metadata.json with execution times and errors

## State Management

### WorkflowState (TypedDict)
```python
{
    # Inputs
    "paper_md": str,
    "paper_meta": Dict,
    "image_paths": List[str],
    "paper_id": str,

    # Intermediate
    "image_urls": Dict[str, str],  # Merged
    "image_server_process": object,
    "p1_markdown": str,

    # Outputs
    "gamma_ppt_url": str,
    "gamma_export_path": str,
    "p2_document": str,
    "p3_article": str,
    "p4_script": str,

    # Metadata
    "errors": List[str],  # Concatenated
    "execution_time": Dict[str, float],  # Merged
}
```

### Concurrent Update Strategy
- Parallel nodes (P2, P3, P4, Gamma) return `Dict` with only their updates
- LangGraph merges updates using Annotated types:
  - `Annotated[Dict, merge_dicts]`: Merge dictionaries
  - `Annotated[List, lambda x, y: x + y]`: Concatenate lists

## Error Handling

### Graceful Degradation
- Errors in one agent don't stop others
- All errors collected in `state["errors"]`
- Workflow completes even with partial failures
- Detailed error logging at every step

### Retry Logic
- Gamma API: Polling with timeout (default 180s)
- HTTP requests: 300s timeout with 60s connect timeout
- No automatic retries (fail fast)

## Performance Characteristics

### Typical Execution Time
- **prepare_images**: 2s
- **execute_p1**: 40-140s (Gemini thinking)
- **call_gamma**: 105-127s (generation + download)
- **execute_p2**: 95-186s (longest agent)
- **execute_p3**: 28-114s
- **execute_p4**: 38-45s
- **Total**: 5-7 minutes

### Parallelization
- P2, P3, P4, Gamma API run in parallel
- Max concurrency: 4 tasks
- Gemini API: No rate limiting observed
- Gamma API: Single generation per call

## Deployment Considerations

### Requirements
- Python 3.8+
- Poetry for dependency management
- API keys: Gemini + Gamma
- Network access for API calls
- Disk space for outputs

### Scalability
- Single workflow per process
- No persistent state between runs
- Stateless design enables horizontal scaling
- Each paper processing is independent

### Monitoring
- Structured logging with Loguru
- Execution time tracking per node
- Error collection and reporting
- Rich CLI output for visibility
