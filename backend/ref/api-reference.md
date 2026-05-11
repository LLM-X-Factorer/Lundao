# API Reference

## Gamma API Client

### Class: `GammaClient`

**Location**: `src/services/gamma_client.py`

#### `__init__()`
Initialize Gamma API client.

**Configuration**:
- API Key: From `settings.gamma_api_key`
- Base URL: `https://public-api.gamma.app`
- Endpoint: `/v1.0/generations`
- Timeout: 300s (5 minutes)

#### `create_generation()`
Create a new presentation generation (Step 1 of 2).

**Signature**:
```python
async def create_generation(
    input_text: str,
    text_mode: str = "generate",
    card_split: str = "inputTextBreaks",
    num_cards: Optional[int] = None,
    export_as: Optional[str] = None,
    additional_params: Optional[Dict] = None,
) -> str
```

**Parameters**:
- `input_text`: Markdown text with `---` separators
- `text_mode`: `"generate"`, `"condense"`, or `"preserve"`
- `card_split`: `"inputTextBreaks"` or `"auto"`
- `num_cards`: Number of cards (only when `card_split="auto"`)
- `export_as`: `"pdf"` or `"pptx"` (optional)
- `additional_params`: Additional API parameters (theme, tone, etc.)

**Returns**: `generationId` string

**Example**:
```python
client = get_gamma_client()
gen_id = await client.create_generation(
    input_text=markdown_content,
    text_mode="generate",
    card_split="inputTextBreaks",
    export_as="pdf"
)
```

#### `get_generation_status()`
Get generation status and result (Step 2 of 2).

**Signature**:
```python
async def get_generation_status(generation_id: str) -> Dict
```

**Parameters**:
- `generation_id`: The generation ID from `create_generation()`

**Returns**: Generation status dictionary
```python
{
    "generationId": "...",
    "status": "completed",  # or "pending", "failed"
    "gammaUrl": "https://gamma.app/docs/...",
    "exportUrl": "https://assets.api.gamma.app/export/...",  # if export_as was set
    "credits": {
        "deducted": 80,
        "remaining": 4724
    }
}
```

#### `generate_presentation()`
Convenience method: create generation and wait for completion.

**Signature**:
```python
async def generate_presentation(
    input_text: str,
    card_split: str = "inputTextBreaks",
    num_cards: Optional[int] = None,
    export_as: Optional[str] = None,
    max_wait_time: int = 300,
    poll_interval: int = 5,
) -> Dict
```

**Parameters**:
- `max_wait_time`: Maximum wait time in seconds (default: 300)
- `poll_interval`: Polling interval in seconds (default: 5)

**Returns**: Final generation result (same as `get_generation_status()`)

**Raises**:
- `TimeoutError`: If generation exceeds `max_wait_time`
- `httpx.HTTPStatusError`: If API request fails

**Example**:
```python
result = await client.generate_presentation(
    input_text=markdown_content,
    card_split="inputTextBreaks",
    export_as="pdf",
    max_wait_time=180,
    poll_interval=5
)

gamma_url = result.get("gammaUrl")
export_url = result.get("exportUrl")
```

#### `download_export()`
Download exported file from Gamma API.

**Signature**:
```python
async def download_export(
    export_url: str,
    output_path: Path,
) -> Path
```

**Parameters**:
- `export_url`: The export URL from generation result
- `output_path`: Path to save the downloaded file

**Returns**: Path to the downloaded file

**Example**:
```python
from pathlib import Path

export_url = result.get("exportUrl")
output_path = Path("outputs/paper_id/gamma_presentation.pdf")

downloaded = await client.download_export(export_url, output_path)
print(f"Downloaded to: {downloaded}")
```

#### `generate_presentation_sync()`
Synchronous wrapper around `generate_presentation()`.

**Signature**:
```python
def generate_presentation_sync(
    input_text: str,
    card_split: str = "inputTextBreaks",
    num_cards: Optional[int] = None,
    max_wait_time: int = 300,
    poll_interval: int = 5,
) -> Dict
```

**Example**:
```python
# Synchronous usage
result = client.generate_presentation_sync(
    input_text=markdown_content,
    card_split="inputTextBreaks"
)
```

#### `get_gamma_client()`
Get singleton Gamma client instance.

**Signature**:
```python
def get_gamma_client() -> GammaClient
```

**Example**:
```python
from src.services.gamma_client import get_gamma_client

client = get_gamma_client()
```

---

## Gemini API Client

### Class: `GeminiClient`

**Location**: `src/services/gemini_client.py`

#### `__init__()`
Initialize Gemini API client.

**Signature**:
```python
def __init__(self, model_name: str = "gemini-2.0-flash-thinking-exp")
```

**Parameters**:
- `model_name`: Gemini model identifier

**Configuration**:
- API Key: From `settings.google_api_key`
- Temperature: 1.0
- Max Tokens: None (unlimited)
- Framework: `langchain-google-genai`

#### `generate()`
Generate text using Gemini with thinking mode.

**Signature**:
```python
async def generate(
    self,
    prompt: str,
    thinking_level: str = "high"
) -> str
```

**Parameters**:
- `prompt`: The prompt text
- `thinking_level`: Thinking depth (`"high"`, `"medium"`, `"low"`)

**Returns**: Generated text content

**Example**:
```python
from src.services.gemini_client import get_gemini_client

client = get_gemini_client()
response = await client.generate(
    prompt="Summarize this paper: ...",
    thinking_level="high"
)
```

#### `generate_sync()`
Synchronous wrapper around `generate()`.

**Signature**:
```python
def generate_sync(self, prompt: str, thinking_level: str = "high") -> str
```

#### `get_gemini_client()`
Get singleton Gemini client instance.

**Signature**:
```python
def get_gemini_client(model_name: Optional[str] = None) -> GeminiClient
```

---

## Image Server

### Functions

**Location**: `src/services/image_server.py`

#### `start_image_server()`
Start temporary image server and generate URLs.

**Signature**:
```python
async def start_image_server(image_paths: List[str]) -> Tuple[ImageServer, Dict[str, str]]
```

**Parameters**:
- `image_paths`: List of local image file paths

**Returns**:
- `ImageServer`: Server instance
- `Dict[str, str]`: Mapping from filename to HTTP URL

**Example**:
```python
server, image_urls = await start_image_server([
    "/path/to/figure1.jpeg",
    "/path/to/figure2.png"
])

# image_urls = {
#     "figure1.jpeg": "http://localhost:8001/images/figure1.jpeg",
#     "figure2.png": "http://localhost:8001/images/figure2.png"
# }
```

#### `stop_image_server()`
Stop image server gracefully.

**Signature**:
```python
def stop_image_server(server: ImageServer) -> None
```

---

## Workflow State

### `WorkflowState` TypedDict

**Location**: `src/core/state.py`

```python
class WorkflowState(TypedDict):
    # Input materials
    paper_md: str
    paper_meta: Dict
    image_paths: List[str]
    paper_id: str

    # Intermediate data
    image_urls: Annotated[Dict[str, str], merge_dicts]
    image_server_process: Optional[object]

    # P1 output
    p1_markdown: str

    # Final outputs (parallel execution)
    gamma_ppt_url: Optional[str]
    gamma_export_path: Optional[str]
    p2_document: Optional[str]
    p3_article: Optional[str]
    p4_script: Optional[str]

    # Metadata
    errors: Annotated[List[str], lambda x, y: x + y]
    execution_time: Annotated[Dict[str, float], merge_dicts]
```

### `create_initial_state()`
Create initial workflow state.

**Signature**:
```python
def create_initial_state(
    paper_md: str,
    paper_meta: Dict,
    image_paths: List[str],
    paper_id: str,
) -> WorkflowState
```

---

## Configuration

### `Settings` (Pydantic Model)

**Location**: `src/core/config.py`

#### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `google_api_key` | `str` | Required | Google Gemini API Key |
| `gamma_api_key` | `str` | Required | Gamma API Key |
| `gamma_export_format` | `str` | `"pdf"` | Export format (pdf/pptx) |
| `image_server_host` | `str` | `"localhost"` | Image server host |
| `image_server_port` | `int` | `8001` | Image server port |
| `image_server_base_url` | `str` | Auto | Image server base URL |
| `api_host` | `str` | `"0.0.0.0"` | API server host |
| `api_port` | `int` | `8000` | API server port |
| `output_dir` | `Path` | `./outputs` | Output directory |
| `log_level` | `str` | `"INFO"` | Logging level |
| `log_file` | `Path` | `None` | Log file path |
| `langgraph_checkpoint_dir` | `Path` | `./checkpoints` | LangGraph checkpoints |

#### Methods

##### `image_server_url` (property)
Get full image server URL.

```python
settings = get_settings()
url = settings.image_server_url  # "http://localhost:8001"
```

##### `ensure_directories()`
Ensure all required directories exist.

```python
settings.ensure_directories()
```

#### `get_settings()`
Get singleton settings instance.

**Signature**:
```python
def get_settings() -> Settings
```

---

## File Handlers

### Functions

**Location**: `src/utils/file_handler.py`

#### `load_paper_materials()`
Load paper materials from directory.

**Signature**:
```python
def load_paper_materials(
    paper_dir: Path
) -> Tuple[str, Dict, List[str], str]
```

**Returns**:
- `str`: Paper markdown content
- `Dict`: Paper metadata
- `List[str]`: Image file paths
- `str`: Paper ID

#### `save_output()`
Save workflow outputs to disk.

**Signature**:
```python
def save_output(
    output_dir: Path,
    paper_id: str,
    p1_markdown: Optional[str] = None,
    p2_document: Optional[str] = None,
    p3_article: Optional[str] = None,
    p4_script: Optional[str] = None,
    gamma_ppt_url: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> None
```

#### `read_prompt_template()`
Read prompt template from docs/.

**Signature**:
```python
def read_prompt_template(prompt_name: str) -> str
```

**Example**:
```python
prompt = read_prompt_template("Prompt-P1")
# Reads from docs/Prompt-P1.md
```

---

## Web API Endpoints

**Location**: `src/api/main.py`, `src/api/routes.py`

### `POST /process`
Process a paper asynchronously.

**Request Body**:
```json
{
  "paper_id": "2410.05779v3",
  "paper_md": "# Paper Title\n...",
  "paper_meta": {...},
  "image_paths": ["/path/to/img1.jpg"]
}
```

**Response**:
```json
{
  "status": "success",
  "paper_id": "2410.05779v3",
  "outputs": {
    "gamma_ppt_url": "https://gamma.app/docs/...",
    "gamma_export_path": "outputs/2410.05779v3/gamma_presentation.pdf",
    "p1_markdown": "...",
    "p2_document": "...",
    "p3_article": "...",
    "p4_script": "..."
  },
  "execution_time": {...},
  "errors": []
}
```

### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "ok"
}
```

---

## CLI Commands

**Location**: `src/cli/main.py`

### `process`
Process a paper directory.

**Usage**:
```bash
python -m src.cli.main process <paper_dir> [--output-dir <dir>]
```

**Arguments**:
- `paper_dir`: Directory containing paper files
- `--output-dir`: Optional output directory (default: from config)

**Example**:
```bash
python -m src.cli.main process examples/2410.05779v3
```

**Output**:
```
Lundao Paper Processor
Processing paper from: examples/2410.05779v3

✓ Loaded paper: 2410.05779v3
  - Markdown: 93778 chars
  - Images: 5 files
  - Metadata: 3 fields

Running workflow...

Workflow completed!

               Results
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ Task           ┃ Status ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ prepare_images │ ✓      │     2.00 │
│ execute_p1     │ ✓      │   140.35 │
│ call_gamma     │ ✓      │   105.28 │
│ execute_p2     │ ✓      │   186.09 │
│ execute_p3     │ ✓      │   113.88 │
│ execute_p4     │ ✓      │    43.42 │
│ finalize       │ ✓      │     0.17 │
└────────────────┴────────┴──────────┘

Saving outputs to: outputs
✓ Outputs saved successfully

Gamma PPT URL: https://gamma.app/docs/txghe6sjdjz6cbi
Gamma Export: outputs/2410.05779v3/gamma_presentation.pdf

Done!
```
