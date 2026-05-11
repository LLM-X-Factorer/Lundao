# Lundao Backend P2P3 - Claude Reference

## Project Overview

**Lundao Backend P2P3** is an automated academic paper processing system that transforms research papers into multiple output formats using AI agents orchestrated by LangGraph.

### What It Does
- Takes academic papers (markdown + images) as input
- Generates 5 outputs using AI:
  1. **Gamma PPT** (PDF/PPTX) - Presentation slides via Gamma API
  2. **Deep Analysis** - Comprehensive technical document
  3. **Technical Article** - Accessible medium-style article
  4. **Speech Script** - Conference presentation script
  5. **Metadata** - Execution stats and errors

### Key Technologies
- **LangGraph**: Workflow orchestration with parallel execution
- **Gemini 3**: AI generation (model: `gemini-2.0-flash-thinking-exp`)
- **Gamma API**: PPT generation and export
- **FastAPI**: Web API interface
- **Typer + Rich**: CLI interface
- **Pydantic**: Configuration and validation

---

## Quick Links

### Getting Started
- **[README.md](./README.md)** - Project overview and quick start
- **[QUICKSTART.md](./QUICKSTART.md)** - Step-by-step setup guide
- **[.env.example](./.env.example)** - Environment configuration template

### Reference Documentation
- **[Architecture](./ref/architecture.md)** - System design and data flow
- **[API Reference](./ref/api-reference.md)** - Complete API documentation
- **[Agents Guide](./ref/agents.md)** - AI agent details (P1-P4)
- **[Development Guide](./ref/development.md)** - Setup, testing, contributing
- **[Gamma API](./ref/gamma-api.md)** - Gamma integration deep dive

### Update Logs
- **[GAMMA_API_UPDATE.md](./GAMMA_API_UPDATE.md)** - Gamma API fixes (2025-11-20)
- **[GAMMA_EXPORT_UPDATE.md](./GAMMA_EXPORT_UPDATE.md)** - Export feature (2025-11-20)

---

## System Architecture

```
Input: Paper MD + Images + Metadata
           ↓
    prepare_images (Image Server)
           ↓
    execute_p1 (Gemini 3 + Prompt-P1)
           ↓
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
call_gamma    P2 Agent   P3 Agent   P4 Agent
(+ Download)  (Analysis) (Article)  (Script)
    │             │          │          │
    └──────┬──────┴──────────┴──────────┘
           ↓
    finalize (Cleanup + Save)
           ↓
Output: 5 files (PPT PDF, Analysis, Article, Script, Metadata)
```

### Key Features
- **Parallel Execution**: P2, P3, P4, Gamma API run concurrently after P1
- **State Management**: LangGraph TypedDict with merge annotations
- **Error Handling**: Graceful degradation, all errors collected
- **Auto Export**: Gamma PPT automatically downloaded as PDF/PPTX

---

## Project Structure

```
Lundao-Backend-P2P3/
├── src/
│   ├── agents/              # AI agents (P1-P4)
│   │   ├── base.py          # Abstract base
│   │   ├── prompt_p1.py     # Gamma PPT blueprint
│   │   ├── prompt_p2.py     # Deep analysis
│   │   ├── prompt_p3.py     # Technical article
│   │   └── prompt_p4.py     # Speech script
│   ├── api/                 # FastAPI web interface
│   ├── cli/                 # Typer CLI interface
│   ├── core/                # Workflow, state, config
│   │   ├── workflow.py      # LangGraph workflow (7 nodes)
│   │   ├── state.py         # WorkflowState TypedDict
│   │   └── config.py        # Pydantic Settings
│   ├── services/            # External API clients
│   │   ├── gemini_client.py # Gemini 3 integration
│   │   ├── gamma_client.py  # Gamma API (2-step flow)
│   │   └── image_server.py  # Temporary HTTP server
│   └── utils/               # File handlers, logging
├── docs/                    # Prompt templates
│   ├── Prompt-P1.md         # PPT generation
│   ├── Prompt-P2.md         # Analysis generation
│   ├── Prompt-P3.md         # Article generation
│   └── Prompt-P4.md         # Script generation
├── ref/                     # Reference docs (this)
├── examples/                # Sample papers
├── outputs/                 # Generated outputs
└── pyproject.toml           # uv / PEP 621 dependencies
```

---

## Important Files

### Core Workflow
- **`src/core/workflow.py`** - Main LangGraph workflow definition
  - 7 nodes: prepare_images → execute_p1 → [4 parallel] → finalize
  - Parallel execution: P2, P3, P4, Gamma API
  - State merging with Annotated types

### Configuration
- **`src/core/config.py`** - Pydantic Settings
  - Loads from `.env` file
  - Validates required API keys
  - Provides `get_settings()` singleton

- **`.env`** - Environment variables (not in git)
  ```env
  GOOGLE_API_KEY=xxx
  GAMMA_API_KEY=sk-gamma-xxx
  GAMMA_EXPORT_FORMAT=pdf
  IMAGE_SERVER_PORT=8001
  OUTPUT_DIR=./outputs
  ```

### API Clients
- **`src/services/gamma_client.py`** - Gamma API client
  - Two-step flow: `create_generation()` → `get_generation_status()`
  - Export support: PDF/PPTX
  - Auto download: `download_export()`
  - **Auth**: `X-API-KEY` header (not Bearer!)
  - **Endpoint**: `https://public-api.gamma.app/v1.0/generations`

- **`src/services/gemini_client.py`** - Gemini 3 client
  - Model: `gemini-2.0-flash-thinking-exp`
  - 1M token context window
  - Thinking mode enabled
  - Uses langchain-google-genai

### Agents
- **`src/agents/prompt_p1.py`** - Generates Gamma markdown
  - Input: paper MD, images, metadata
  - Output: Markdown with `---` card separators
  - Execution: 40-140s
  - Prompt: `docs/Prompt-P1.md`

- **`src/agents/prompt_p2.py`** - Deep analysis
  - Input: P1 markdown, original paper
  - Output: 20-250 KB comprehensive doc
  - Execution: 95-186s (longest)
  - Prompt: `docs/Prompt-P2.md`

- **`src/agents/prompt_p3.py`** - Technical article
  - Input: P1 markdown, original paper
  - Output: 3-10 KB accessible article
  - Execution: 28-114s
  - Prompt: `docs/Prompt-P3.md`

- **`src/agents/prompt_p4.py`** - Speech script
  - Input: P1 markdown, original paper
  - Output: 9-10 KB presentation script
  - Execution: 38-45s (fastest)
  - Prompt: `docs/Prompt-P4.md`

---

## Common Operations

### Running the System

**CLI Mode** (recommended for development):
```bash
uv run python -m src.cli.main process examples/2410.05779v3
```

**API Mode** (for production):
```bash
uv run python -m src.api.main
# Then POST to http://localhost:8000/process
```

### Understanding Output

After processing, outputs are saved to `outputs/{paper_id}/`:
- `p1_gamma_markdown.md` - PPT blueprint (10-20 KB)
- `gamma_presentation.pdf` - Downloaded PPT (4-5 MB, 17 pages)
- `p2_deep_analysis.md` - Technical analysis (20-250 KB)
- `p3_tech_article.md` - Accessible article (3-10 KB)
- `p4_speech_script.md` - Presentation script (9-10 KB)
- `metadata.json` - Execution stats and errors

### Workflow Execution Times

Typical execution (total ~5-7 minutes):
- `prepare_images`: 2s
- `execute_p1`: 40-140s (Gemini thinking)
- Parallel phase (max):
  - `call_gamma`: 105-127s (generation + download)
  - `execute_p2`: 95-186s (longest)
  - `execute_p3`: 28-114s
  - `execute_p4`: 38-45s
- `finalize`: <1s

---

## Key Concepts

### LangGraph State Management

**WorkflowState** is a TypedDict with special merge behavior:
```python
class WorkflowState(TypedDict):
    # Regular fields (overwrite)
    paper_md: str
    p1_markdown: str

    # Merged fields (Annotated)
    image_urls: Annotated[Dict[str, str], merge_dicts]
    errors: Annotated[List[str], lambda x, y: x + y]
    execution_time: Annotated[Dict[str, float], merge_dicts]
```

**Parallel node pattern** (critical for concurrent updates):
```python
# ❌ Wrong - returns full state
async def execute_p2_node(state: WorkflowState) -> WorkflowState:
    state["p2_document"] = result
    return state

# ✅ Correct - returns only updates
async def execute_p2_node(state: WorkflowState) -> Dict:
    return {"p2_document": result}
```

### Gamma API Two-Step Flow

**Step 1: Create**
```python
gen_id = await client.create_generation(
    input_text=markdown,
    text_mode="generate",
    card_split="inputTextBreaks",
    export_as="pdf"
)
```

**Step 2: Poll**
```python
while True:
    result = await client.get_generation_status(gen_id)
    if result["status"] == "completed":
        gamma_url = result["gammaUrl"]
        export_url = result["exportUrl"]  # Download this!
        break
    await asyncio.sleep(5)
```

**Critical**: Export URLs are temporary - download immediately!

### Gemini 3 Thinking Mode

All agents use high thinking level:
```python
response = await gemini_client.generate(
    prompt=filled_prompt,
    thinking_level="high"  # Deep reasoning
)
```

Benefits:
- Better understanding of complex papers
- More coherent outputs
- Improved technical accuracy

---

## Troubleshooting

### 401 Unauthorized (Gamma API)
**Cause**: Wrong auth header format

**Fix**: Use `X-API-KEY`, NOT `Authorization: Bearer`
```python
# ✅ Correct
headers = {"X-API-KEY": api_key}

# ❌ Wrong
headers = {"Authorization": f"Bearer {api_key}"}
```

### INVALID_CONCURRENT_GRAPH_UPDATE
**Cause**: Parallel nodes returning full state

**Fix**: Return only updates as Dict
```python
# ✅ Correct
return {"p2_document": result, "execution_time": {"p2": 123}}

# ❌ Wrong
state["p2_document"] = result
return state
```

### Gamma Generation Timeout
**Cause**: Generation taking longer than expected

**Fix**: Increase timeout in workflow.py
```python
response = await client.generate_presentation(
    input_text=state["p1_markdown"],
    max_wait_time=300,  # 5 minutes instead of 3
    poll_interval=5
)
```

### Image Server Port in Use
**Cause**: Port 8001 already occupied

**Fix**: Change port in .env
```env
IMAGE_SERVER_PORT=8002
```

---

## Development Workflow

### 1. Modifying Prompts
- Edit `docs/Prompt-P*.md` files
- No code changes needed
- Test immediately

### 2. Adding New Agent
1. Create `src/agents/prompt_p5.py` (copy existing agent)
2. Create `docs/Prompt-P5.md` template
3. Add node to `src/core/workflow.py`
4. Update `src/core/state.py` with new field
5. Test with CLI

### 3. Running Tests
```bash
uv run pytest                    # All tests
uv run pytest tests/test_workflow.py  # Specific file
uv run pytest --cov=src          # With coverage
```

### 4. Code Formatting
```bash
uv run black src/
uv run isort src/
uv run flake8 src/
```

---

## Architecture Decisions

### Why LangGraph?
- Built-in state management
- Parallel execution support
- Type-safe state with TypedDict
- Clean node-based workflow

### Why Gemini 3?
- 1M token context (entire papers)
- Thinking mode for reasoning
- Multi-modal (text + images)
- Reliable performance

### Why Two Interfaces (CLI + API)?
- CLI: Development, testing, debugging
- API: Production, integration, scaling

### Why Parallel Execution?
- P2, P3, P4 are independent
- Reduces total time by ~60%
- Better resource utilization

---

## Performance Tips

1. **Reduce Gemini Latency**
   - Cache prompt templates
   - Use `thinking_level="medium"` for simpler tasks

2. **Optimize Gamma API**
   - Default 180s timeout is usually enough
   - Don't poll more frequently than 5s
   - Download exports immediately

3. **Memory Management**
   - P2 can generate 250KB+ outputs
   - Process one paper at a time
   - Clean up temporary files

4. **Parallel Execution**
   - Keep agents independent
   - No inter-agent dependencies
   - Use async/await properly

---

## Future Improvements

### Potential Features
- [ ] Batch processing of multiple papers
- [ ] Resume from checkpoint (LangGraph feature)
- [ ] Email notifications on completion
- [ ] S3/Cloud storage for outputs
- [ ] Web dashboard for monitoring
- [ ] Customizable agent selection
- [ ] Multi-language support

### Known Limitations
- No retry logic for failed agents
- No partial result saving
- Single paper per workflow
- No streaming outputs
- Fixed agent pipeline

---

## Getting Help

### Documentation
1. Start with **[README.md](./README.md)** for overview
2. Read **[QUICKSTART.md](./QUICKSTART.md)** for setup
3. Check **[ref/](./ref/)** for detailed guides
4. Review update logs for recent changes

### Code Navigation
- Start from `src/cli/main.py` (entry point)
- Follow to `src/core/workflow.py` (main logic)
- Check `src/agents/` for agent implementations
- Review `src/services/` for external integrations

### Common Questions

**Q: How do I add a new output format?**
A: Create new agent in `src/agents/`, add node to workflow, update state

**Q: Can I use a different LLM?**
A: Yes, modify `src/services/gemini_client.py` or create new client

**Q: How do I change PPT format?**
A: Edit `docs/Prompt-P1.md` template, no code changes needed

**Q: Can I skip certain agents?**
A: Yes, modify workflow edges in `src/core/workflow.py`

**Q: How do I deploy this?**
A: Use API mode + container (Docker) + process manager (Supervisor)

---

## Contact & Support

- **Repository**: [Project URL]
- **Issues**: Use GitHub Issues for bugs
- **Documentation**: All docs in `ref/` directory
- **Updates**: Check GAMMA_*_UPDATE.md files

---

## Version History

- **2025-11-20**: Gamma export feature added
- **2025-11-20**: Gamma API fixed (endpoint + auth)
- **2025-11-19**: Initial release with P1-P4 agents

---

*Last Updated: 2025-11-20*
