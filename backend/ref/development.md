# Development Guide

## Setup

### Prerequisites
- Python 3.8+
- Poetry (for dependency management)
- API Keys:
  - Google Gemini API key
  - Gamma API key

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd Lundao-Backend-P2P3
```

2. **Install dependencies**
```bash
poetry install
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required `.env` configuration:
```env
# Gemini API Configuration
GOOGLE_API_KEY=your_gemini_api_key_here

# Gamma API Configuration
GAMMA_API_KEY=your_gamma_api_key_here
GAMMA_EXPORT_FORMAT=pdf  # or pptx

# Image Server Configuration
IMAGE_SERVER_HOST=localhost
IMAGE_SERVER_PORT=8001
IMAGE_SERVER_BASE_URL=http://localhost:8001

# API Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Output Configuration
OUTPUT_DIR=./outputs

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# LangGraph Configuration
LANGGRAPH_CHECKPOINT_DIR=./checkpoints
```

---

## Project Structure

```
Lundao-Backend-P2P3/
├── src/
│   ├── agents/           # AI agent implementations
│   │   ├── base.py       # Base agent class
│   │   ├── prompt_p1.py  # P1: Gamma PPT blueprint
│   │   ├── prompt_p2.py  # P2: Deep analysis
│   │   ├── prompt_p3.py  # P3: Technical article
│   │   └── prompt_p4.py  # P4: Speech script
│   ├── api/              # FastAPI web interface
│   │   ├── main.py       # FastAPI app
│   │   ├── routes.py     # API routes
│   │   └── schemas.py    # Pydantic schemas
│   ├── cli/              # CLI interface
│   │   └── main.py       # Typer CLI commands
│   ├── core/             # Core workflow logic
│   │   ├── config.py     # Pydantic settings
│   │   ├── state.py      # LangGraph state
│   │   └── workflow.py   # Workflow definition
│   ├── services/         # External service clients
│   │   ├── gemini_client.py   # Gemini API
│   │   ├── gamma_client.py    # Gamma API
│   │   └── image_server.py    # Image HTTP server
│   └── utils/            # Utilities
│       ├── file_handler.py    # File I/O
│       ├── logger.py          # Logging setup
│       └── prompts.py         # Prompt utilities
├── docs/                 # Prompt templates
│   ├── Prompt-P1.md
│   ├── Prompt-P2.md
│   ├── Prompt-P3.md
│   └── Prompt-P4.md
├── examples/             # Example paper data
├── outputs/              # Generated outputs
├── ref/                  # Reference documentation
├── tests/                # Test suite
├── .env                  # Environment variables
├── pyproject.toml        # Poetry dependencies
└── README.md
```

---

## Running the System

### CLI Mode

**Process a paper**:
```bash
poetry run python -m src.cli.main process examples/2410.05779v3
```

**With custom output directory**:
```bash
poetry run python -m src.cli.main process examples/2410.05779v3 --output-dir ./my-outputs
```

### API Mode

**Start the server**:
```bash
poetry run python -m src.api.main
```

Server runs on `http://localhost:8000`

**Process via API**:
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "paper_id": "2410.05779v3",
    "paper_md": "...",
    "paper_meta": {...},
    "image_paths": [...]
  }'
```

**Health check**:
```bash
curl http://localhost:8000/health
```

---

## Development Workflow

### 1. Adding a New Feature

**Example: Add email notification after workflow completion**

1. **Create service client**:
```python
# src/services/email_client.py
import smtplib
from src.core.config import get_settings

class EmailClient:
    def __init__(self):
        settings = get_settings()
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port

    async def send_notification(self, subject: str, body: str):
        # Implementation
        pass
```

2. **Update configuration**:
```python
# src/core/config.py
class Settings(BaseSettings):
    # ... existing fields ...
    smtp_server: str = Field(default="smtp.gmail.com")
    smtp_port: int = Field(default=587)
    notification_email: str = Field(...)
```

3. **Integrate into workflow**:
```python
# src/core/workflow.py
async def finalize_node(state: WorkflowState) -> WorkflowState:
    # ... existing cleanup ...

    # Send notification
    if settings.notification_email:
        email_client = EmailClient()
        await email_client.send_notification(
            subject=f"Paper processing complete: {state['paper_id']}",
            body=f"Outputs saved to {settings.output_dir}"
        )

    return state
```

4. **Update .env.example**:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
NOTIFICATION_EMAIL=your_email@example.com
```

### 2. Modifying an Agent

**Example: Customize P3 article output format**

1. **Update prompt template**:
```markdown
<!-- docs/Prompt-P3.md -->
# Generate Technical Article

... existing instructions ...

## Additional Requirements
- Include a "Quick Reference" section at the end
- Add code snippets where applicable
- Use emoji section markers (📌, 💡, ⚠️)
```

2. **Test changes**:
```bash
poetry run python -m src.cli.main process examples/2410.05779v3
```

3. **Verify output**:
```bash
cat outputs/2410.05779v3/p3_tech_article.md
```

### 3. Debugging

**Enable debug logging**:
```python
# .env
LOG_LEVEL=DEBUG
```

**Add debug statements**:
```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

logger.debug(f"Input data: {data}")
logger.info(f"Processing step 1 complete")
logger.warning(f"Unexpected value: {value}")
logger.error(f"Operation failed: {error}")
```

**View logs**:
```bash
tail -f logs/app.log
```

---

## Testing

### Running Tests

**All tests**:
```bash
poetry run pytest
```

**With coverage**:
```bash
poetry run pytest --cov=src --cov-report=html
```

**Specific test file**:
```bash
poetry run pytest tests/test_workflow.py
```

### Writing Tests

**Example: Test Gamma client**:
```python
# tests/test_gamma_client.py
import pytest
from unittest.mock import AsyncMock, patch
from src.services.gamma_client import GammaClient

@pytest.mark.asyncio
async def test_create_generation():
    client = GammaClient()

    with patch.object(client, 'create_generation', new=AsyncMock(return_value="test-gen-id")):
        gen_id = await client.create_generation(
            input_text="# Test",
            export_as="pdf"
        )

    assert gen_id == "test-gen-id"

@pytest.mark.asyncio
async def test_generate_presentation_timeout():
    client = GammaClient()

    with pytest.raises(TimeoutError):
        await client.generate_presentation(
            input_text="# Test",
            max_wait_time=1,
            poll_interval=0.1
        )
```

**Example: Test workflow node**:
```python
# tests/test_workflow.py
import pytest
from src.core.workflow import execute_p1_node
from src.core.state import create_initial_state

@pytest.mark.asyncio
async def test_execute_p1_node():
    state = create_initial_state(
        paper_md="# Test Paper\n\nContent...",
        paper_meta={"title": "Test"},
        image_paths=["test.jpg"],
        paper_id="test123"
    )
    state["image_urls"] = {"test.jpg": "http://localhost:8001/images/test.jpg"}

    result = await execute_p1_node(state)

    assert "p1_markdown" in result
    assert len(result["p1_markdown"]) > 0
    assert "execution_time" in result
```

---

## Code Style

### Python Style Guide

**Use Black for formatting**:
```bash
poetry run black src/
```

**Use isort for import sorting**:
```bash
poetry run isort src/
```

**Use flake8 for linting**:
```bash
poetry run flake8 src/
```

### Type Hints

Always use type hints:
```python
from typing import Dict, List, Optional

async def process_paper(
    paper_md: str,
    image_paths: List[str],
    config: Optional[Dict] = None
) -> Dict[str, str]:
    """Process paper and return outputs.

    Args:
        paper_md: Paper markdown content
        image_paths: List of image file paths
        config: Optional configuration overrides

    Returns:
        Dictionary of output file paths
    """
    ...
```

### Docstrings

Use Google-style docstrings:
```python
class GammaClient:
    """Client for interacting with Gamma API.

    Attributes:
        api_key: Gamma API authentication key
        base_url: Base URL for API endpoints

    Example:
        >>> client = GammaClient()
        >>> result = await client.generate_presentation("# Title")
        >>> print(result['gammaUrl'])
    """

    async def create_generation(
        self,
        input_text: str,
        export_as: Optional[str] = None
    ) -> str:
        """Create a new presentation generation.

        Args:
            input_text: Markdown text with --- separators
            export_as: Export format (pdf or pptx)

        Returns:
            Generation ID string

        Raises:
            ValueError: If export_as is not pdf or pptx
            httpx.HTTPStatusError: If API request fails

        Example:
            >>> gen_id = await client.create_generation(
            ...     input_text="# Slide 1\\n---\\n# Slide 2",
            ...     export_as="pdf"
            ... )
        """
        ...
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Not Working

**Symptom**: 401 Unauthorized errors

**Solution**:
```bash
# Verify .env file
cat .env | grep API_KEY

# Test Gamma key manually
curl -H "X-API-KEY: your-key" \
  https://public-api.gamma.app/v1.0/generations

# Test Gemini key manually
curl "https://generativelanguage.googleapis.com/v1beta/models?key=your-key"
```

#### 2. Image Server Port Already in Use

**Symptom**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Check what's using the port
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or change port in .env
IMAGE_SERVER_PORT=8002
```

#### 3. Gamma Generation Timeout

**Symptom**: `TimeoutError: Generation did not complete within 180s`

**Solution**:
```python
# Increase timeout in workflow.py
response = await client.generate_presentation(
    input_text=state["p1_markdown"],
    max_wait_time=300,  # Increase to 5 minutes
    poll_interval=5
)
```

#### 4. Out of Memory

**Symptom**: System kills Python process during P2 execution

**Solution**:
- P2 generates very large outputs (up to 250KB)
- Process papers one at a time
- Consider streaming/chunking for very long papers

#### 5. LangGraph Concurrent Update Error

**Symptom**: `INVALID_CONCURRENT_GRAPH_UPDATE`

**Solution**:
- Ensure parallel nodes return `Dict` not `WorkflowState`
- Only include fields that node is updating
- Don't return shared fields like `paper_md`

```python
# ❌ Wrong
async def execute_p2_node(state: WorkflowState) -> WorkflowState:
    state["p2_document"] = result
    return state  # Returns full state

# ✅ Correct
async def execute_p2_node(state: WorkflowState) -> Dict:
    return {"p2_document": result}  # Only return updates
```

---

## Performance Optimization

### 1. Reduce Gemini Latency
- Use `thinking_level="medium"` for less critical tasks
- Cache prompt templates
- Batch requests when possible

### 2. Parallel Execution
- Keep P2, P3, P4 independent
- No inter-agent dependencies
- Use async/await properly

### 3. Gamma API
- Default timeout (180s) is usually sufficient
- Don't poll too frequently (5s interval is good)
- Download exports immediately (links expire)

### 4. Memory Management
- Stream large files instead of loading entirely
- Clean up temporary files in finalize node
- Use generators for large data processing

---

## Contributing

### Pull Request Process

1. **Create feature branch**:
```bash
git checkout -b feature/my-new-feature
```

2. **Make changes with tests**:
```python
# src/new_feature.py
# tests/test_new_feature.py
```

3. **Run checks**:
```bash
poetry run black src/ tests/
poetry run isort src/ tests/
poetry run flake8 src/ tests/
poetry run pytest
```

4. **Commit with clear message**:
```bash
git commit -m "Add feature: Brief description

- Detailed point 1
- Detailed point 2

Closes #123"
```

5. **Push and create PR**:
```bash
git push origin feature/my-new-feature
# Create PR on GitHub
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example**:
```
feat: Add email notifications after workflow completion

- Add EmailClient service
- Integrate into finalize node
- Add SMTP configuration to settings
- Update documentation

Closes #42
```
