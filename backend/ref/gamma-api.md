# Gamma API Integration Guide

## Overview

The Gamma API integration enables automated PPT generation and export. This document covers the complete integration details.

## Official Documentation

- [API Overview](https://developers.gamma.app/docs/understand-the-api-options)
- [Generate Parameters](https://developers.gamma.app/docs/generate-api-parameters-explained)
- [API Reference](https://developers.gamma.app/reference)

## API Details

### Base URL
```
https://public-api.gamma.app
```

### Endpoint
```
POST /v1.0/generations
GET  /v1.0/generations/{generationId}
```

### Authentication
**Header**: `X-API-KEY: sk-gamma-xxx`

**NOT** `Authorization: Bearer` (common mistake!)

## Two-Step Workflow

### Step 1: Create Generation

**Request**:
```http
POST https://public-api.gamma.app/v1.0/generations
X-API-KEY: sk-gamma-xxx
Content-Type: application/json

{
  "inputText": "# Slide 1\n\n* Point 1\n* Point 2\n\n---\n\n# Slide 2\n\n* Point 3",
  "textMode": "generate",
  "cardSplit": "inputTextBreaks",
  "exportAs": "pdf"
}
```

**Response**:
```json
{
  "generationId": "abc123xyz"
}
```

### Step 2: Poll for Completion

**Request**:
```http
GET https://public-api.gamma.app/v1.0/generations/abc123xyz
X-API-KEY: sk-gamma-xxx
```

**Response (Pending)**:
```json
{
  "generationId": "abc123xyz",
  "status": "pending"
}
```

**Response (Completed)**:
```json
{
  "generationId": "abc123xyz",
  "status": "completed",
  "gammaUrl": "https://gamma.app/docs/xyz123abc",
  "exportUrl": "https://assets.api.gamma.app/export/pdf/xyz123abc/hash/filename.pdf",
  "credits": {
    "deducted": 80,
    "remaining": 4724
  }
}
```

**Response (Failed)**:
```json
{
  "generationId": "abc123xyz",
  "status": "failed",
  "error": "Input text exceeds maximum length"
}
```

## Request Parameters

### Required Parameters

#### `inputText` (string)
Markdown content with card separators.

**Format**:
```markdown
# Card Title

* Bullet point 1
* Bullet point 2

---

# Next Card

Content here...
```

**Requirements**:
- Use `---` (triple dash) to separate cards
- Use `#` or `##` for titles
- Use `*` or `-` for bullet points
- Max length: 100K tokens

#### `textMode` (string)
Text generation mode.

**Options**:
- `"generate"`: Expand and enhance content (default)
- `"condense"`: Compress content
- `"preserve"`: Keep original text

**Recommendation**: Use `"generate"` for most cases

#### `cardSplit` (string)
Card splitting strategy.

**Options**:
- `"inputTextBreaks"`: Split at `---` markers (recommended)
- `"auto"`: Automatic splitting based on content

**With `inputTextBreaks`**:
```markdown
# Card 1
Content
---
# Card 2
Content
```
Creates exactly 2 cards.

**With `auto`**:
- Must specify `numCards` parameter
- System decides split points
- Less predictable

### Optional Parameters

#### `exportAs` (string)
Export format for download.

**Options**:
- `"pdf"`: PDF document (4-5 MB for 17 pages)
- `"pptx"`: PowerPoint file

**Response includes**:
```json
{
  "exportUrl": "https://assets.api.gamma.app/export/pdf/..."
}
```

**⚠️ Important**: Export URLs are temporary and expire after some time. Download immediately!

#### `numCards` (integer)
Number of cards to generate (only with `cardSplit: "auto"`).

**Example**:
```json
{
  "inputText": "Long content...",
  "cardSplit": "auto",
  "numCards": 15
}
```

#### `themeId` (string)
Gamma theme identifier.

**Popular themes**:
- `"Oasis"`
- `"Noir"`
- `"Clarity"`

#### `tone` (string)
Presentation tone.

**Examples**:
- `"professional"`
- `"casual"`
- `"inspiring"`
- `"technical"`

#### `additionalInstructions` (string)
Extra instructions for generation.

**Example**:
```json
{
  "additionalInstructions": "Make the titles catchy and use technical terminology"
}
```

## Implementation in Code

### Client Initialization

```python
from src.services.gamma_client import get_gamma_client

client = get_gamma_client()
```

### Basic Generation

```python
# Simple generation
result = await client.generate_presentation(
    input_text=markdown_content,
    card_split="inputTextBreaks",
    max_wait_time=180,
    poll_interval=5
)

gamma_url = result.get("gammaUrl")
print(f"View at: {gamma_url}")
```

### Generation with Export

```python
# With PDF export
result = await client.generate_presentation(
    input_text=markdown_content,
    card_split="inputTextBreaks",
    export_as="pdf",
    max_wait_time=180,
    poll_interval=5
)

gamma_url = result.get("gammaUrl")
export_url = result.get("exportUrl")

# Download the PDF
from pathlib import Path
output_path = Path("outputs/presentation.pdf")
await client.download_export(export_url, output_path)
```

### Manual Two-Step Process

```python
# Step 1: Create generation
gen_id = await client.create_generation(
    input_text=markdown_content,
    text_mode="generate",
    card_split="inputTextBreaks",
    export_as="pdf"
)

# Step 2: Poll manually
import asyncio

while True:
    result = await client.get_generation_status(gen_id)
    status = result.get("status")

    if status == "completed":
        print(f"Done! URL: {result['gammaUrl']}")
        break
    elif status == "failed":
        print(f"Failed: {result.get('error')}")
        break
    else:
        print(f"Status: {status}")
        await asyncio.sleep(5)
```

## Error Handling

### Common Errors

#### 401 Unauthorized
**Cause**: Invalid or missing API key

**Solution**:
```bash
# Check .env
cat .env | grep GAMMA_API_KEY

# Test with curl
curl -H "X-API-KEY: your-key" \
  https://public-api.gamma.app/v1.0/generations
```

#### 400 Bad Request
**Cause**: Invalid parameters

**Common issues**:
- `textMode` not set (required)
- Invalid `cardSplit` value
- `numCards` used with `inputTextBreaks`
- `exportAs` not `"pdf"` or `"pptx"`

**Solution**: Check request payload format

#### 429 Too Many Requests
**Cause**: Rate limit exceeded

**Solution**: Implement exponential backoff

```python
import asyncio
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
async def create_with_retry(client, **kwargs):
    return await client.create_generation(**kwargs)
```

#### TimeoutError
**Cause**: Generation taking too long

**Solution**: Increase `max_wait_time`

```python
result = await client.generate_presentation(
    input_text=markdown_content,
    max_wait_time=300,  # 5 minutes
    poll_interval=5
)
```

### Error Handling Pattern

```python
try:
    result = await client.generate_presentation(
        input_text=markdown_content,
        export_as="pdf"
    )

    if result.get("status") == "completed":
        gamma_url = result["gammaUrl"]
        export_url = result.get("exportUrl")

        if export_url:
            await client.download_export(export_url, output_path)
        else:
            logger.warning("No export URL in response")

except TimeoutError:
    logger.error("Generation timed out")
    # Handle timeout (retry, notify user, etc.)

except httpx.HTTPStatusError as e:
    logger.error(f"HTTP error: {e.response.status_code}")
    logger.error(f"Response: {e.response.text}")
    # Handle API error

except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle unexpected error
```

## Best Practices

### 1. Input Text Format

**✅ Good**:
```markdown
# Introduction to AI

* Artificial Intelligence is transforming industries
* Machine learning enables computers to learn from data
* Deep learning achieves human-level performance in many tasks

---

# Key Applications

* Computer Vision: Image recognition and object detection
* Natural Language Processing: Text understanding and generation
* Robotics: Autonomous navigation and manipulation
```

**❌ Bad**:
```markdown
Introduction to AI. Artificial Intelligence is transforming industries, machine learning enables computers to learn from data, deep learning achieves human-level performance.

Key Applications include Computer Vision, NLP, and Robotics.
```

### 2. Card Structure

- **1 main idea per card**
- **3-5 bullet points per card**
- **Clear hierarchical titles**
- **Consistent formatting**

### 3. Polling Strategy

**Recommended settings**:
```python
max_wait_time=180  # 3 minutes (typical: 60-120s)
poll_interval=5     # 5 seconds (don't poll too frequently)
```

**Why**:
- Most generations complete in 60-120 seconds
- 180s timeout provides buffer
- 5s interval balances responsiveness vs. API load

### 4. Export Management

```python
# Always download immediately
export_url = result.get("exportUrl")
if export_url:
    # Download right away (links expire!)
    await client.download_export(export_url, output_path)
    logger.info(f"Downloaded to: {output_path}")
else:
    logger.warning("No export URL - file not generated")
```

### 5. Credits Monitoring

```python
result = await client.generate_presentation(...)

credits_used = result.get("credits", {}).get("deducted", 0)
credits_remaining = result.get("credits", {}).get("remaining", 0)

logger.info(f"Used {credits_used} credits, {credits_remaining} remaining")

if credits_remaining < 100:
    logger.warning("Low credits - consider purchasing more")
```

## Performance Characteristics

### Generation Time
- **Typical**: 60-120 seconds
- **Range**: 30-180 seconds
- **Factors**: Content length, complexity, export format

### File Sizes
- **PDF**: ~4-5 MB for 17 pages
- **PPTX**: Variable (usually smaller than PDF)

### Credits Cost
- **Standard generation**: 80 credits
- **With export**: Same cost (no extra charge)
- **Failed generation**: No credits deducted

## Testing

### Manual Testing with cURL

**Create generation**:
```bash
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H "X-API-KEY: sk-gamma-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "inputText": "# Test Slide\n\n* Point 1\n* Point 2",
    "textMode": "generate",
    "cardSplit": "inputTextBreaks",
    "exportAs": "pdf"
  }'
```

**Check status**:
```bash
curl https://public-api.gamma.app/v1.0/generations/abc123xyz \
  -H "X-API-KEY: sk-gamma-xxx"
```

**Download export**:
```bash
curl -o presentation.pdf "https://assets.api.gamma.app/export/pdf/..."
```

### Automated Testing

```python
import pytest
from src.services.gamma_client import GammaClient

@pytest.mark.asyncio
async def test_gamma_generation():
    """Integration test for Gamma API."""
    client = GammaClient()

    # Create test content
    test_content = """# Test Slide

* Test point 1
* Test point 2

---

# Second Slide

* Another point
"""

    # Generate
    result = await client.generate_presentation(
        input_text=test_content,
        card_split="inputTextBreaks",
        export_as="pdf",
        max_wait_time=180
    )

    # Assertions
    assert result["status"] == "completed"
    assert "gammaUrl" in result
    assert "exportUrl" in result
    assert result["gammaUrl"].startswith("https://gamma.app/docs/")
```

## Migration Notes

### From Old API (Pre-2025)

**Old endpoint** (wrong):
```
https://api.gamma.app/api/v1/generate
```

**New endpoint** (correct):
```
https://public-api.gamma.app/v1.0/generations
```

**Key changes**:
1. ✅ Two-step process (create → poll)
2. ✅ `X-API-KEY` header instead of `Authorization: Bearer`
3. ✅ `textMode` is now required
4. ✅ Export via `exportAs` parameter
5. ✅ `exportUrl` in response (temporary link)

### Code Updates Required

**Before**:
```python
# Single POST request
response = await client.post(
    "https://api.gamma.app/api/v1/generate",
    json={"inputText": text},
    headers={"Authorization": f"Bearer {api_key}"}
)
gamma_url = response.json()["url"]
```

**After**:
```python
# Two-step process
gen_id = await client.create_generation(
    input_text=text,
    text_mode="generate",
    export_as="pdf"
)

# Poll for completion
result = await client.get_generation_status(gen_id)
while result["status"] == "pending":
    await asyncio.sleep(5)
    result = await client.get_generation_status(gen_id)

gamma_url = result["gammaUrl"]
export_url = result["exportUrl"]
```

## Troubleshooting

### Issue: Generation never completes

**Symptoms**:
- Status stays "pending" forever
- Eventually times out

**Solutions**:
1. Check content length (max 100K tokens)
2. Verify markdown format is correct
3. Check for special characters in `inputText`
4. Try simpler content first

### Issue: Export URL returns 404

**Cause**: Link expired or generation failed

**Solution**:
- Download immediately after generation
- Don't store export URLs for later use
- Re-generate if link expired

### Issue: Inconsistent card splitting

**Cause**: Using `cardSplit: "auto"` or ambiguous `---` placement

**Solution**:
- Always use `cardSplit: "inputTextBreaks"`
- Ensure exactly 3 dashes: `---`
- Put `---` on its own line
- Add blank lines before/after `---`

## Reference Links

- [Update Documentation](../GAMMA_API_UPDATE.md)
- [Export Feature Documentation](../GAMMA_EXPORT_UPDATE.md)
- [Official API Docs](https://developers.gamma.app/docs)
