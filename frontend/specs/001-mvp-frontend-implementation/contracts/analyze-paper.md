# API Contract: Analyze Paper

## Endpoint
```
GET /api/analyze_paper
```

## Description
Retrieves AI-generated analysis (Chinese summary and innovation points) for a paper identified by either arXiv ID or uploaded file ID.

## Request

### Query Parameters

| Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `arxivId` | String | Conditional | arXiv paper identifier | Required if `fileId` not provided. Format: `\d{4}\.\d{5}` |
| `fileId` | String (UUID) | Conditional | Uploaded file identifier | Required if `arxivId` not provided. Format: `upload-{uuid}` |

**Note**: Exactly one of `arxivId` or `fileId` must be provided.

### Headers
```
Accept: application/json
```

### Example Requests

**For arXiv paper**:
```http
GET /api/analyze_paper?arxivId=2301.00000 HTTP/1.1
Host: api.lundao.com
Accept: application/json
```

**For uploaded file**:
```http
GET /api/analyze_paper?fileId=upload-550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: api.lundao.com
Accept: application/json
```

## Response

### Success Response (200 OK)

**Body**:
```json
{
  "paperId": "arxiv-2301.00000",
  "chineseSummary": "本文提出了Transformer模型，这是一种完全基于注意力机制的序列转换模型。作者摒弃了传统的循环神经网络和卷积神经网络结构，仅使用注意力机制来捕捉序列中的依赖关系。实验表明，该模型在机器翻译任务上达到了当时的最佳性能，且训练速度显著提升。Transformer的核心创新在于多头自注意力机制，它允许模型同时关注输入序列的不同位置，并行计算所有位置的表示。",
  "innovationPoints": [
    "提出了完全基于注意力机制的Transformer架构，摒弃了循环和卷积层，实现了更高的并行化程度",
    "引入多头自注意力机制，使模型能够同时从不同表示子空间学习信息",
    "在WMT 2014英德和英法翻译任务上达到了SOTA性能，同时训练时间大幅减少",
    "位置编码（Positional Encoding）的设计使模型能够利用序列顺序信息，弥补了注意力机制对位置不敏感的缺陷",
    "自注意力机制的可解释性优于RNN，能够直观地可视化不同词之间的注意力权重分布"
  ],
  "analysisTimestamp": "2025-10-14T10:30:45Z",
  "analysisStatus": "completed"
}
```

**Schema**:
- `paperId`: String - Paper identifier (matches request parameter)
- `chineseSummary`: String - AI-generated Chinese summary (200-800 characters)
- `innovationPoints`: Array<String> - List of 3-10 innovation points in Chinese
- `analysisTimestamp`: String (ISO 8601) - When analysis completed
- `analysisStatus`: String (enum) - Analysis status (`"pending"`, `"completed"`, `"failed"`)

### Pending Analysis (202 Accepted)

Analysis is in progress. Client should retry after delay.

```json
{
  "paperId": "arxiv-2301.00000",
  "analysisStatus": "pending",
  "estimatedCompletionTime": "2025-10-14T10:31:00Z",
  "retryAfter": 15
}
```

**Frontend behavior**: Show skeleton loading, retry after 15 seconds.

### Error Responses

#### 400 Bad Request
Missing or invalid parameters.

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Either arxivId or fileId must be provided",
    "details": {
      "providedParameters": []
    }
  }
}
```

#### 404 Not Found
Paper or file not found.

```json
{
  "error": {
    "code": "PAPER_NOT_FOUND",
    "message": "No paper found with the provided identifier",
    "details": {
      "arxivId": "9999.99999"
    }
  }
}
```

#### 422 Unprocessable Entity
PDF cannot be analyzed (corrupted, non-English, etc.).

```json
{
  "error": {
    "code": "ANALYSIS_FAILED",
    "message": "Unable to analyze this paper. The PDF may be corrupted or in an unsupported format.",
    "details": {
      "reason": "text_extraction_failed"
    }
  }
}
```

#### 504 Gateway Timeout
AI analysis exceeded 60-second timeout.

```json
{
  "error": {
    "code": "ANALYSIS_TIMEOUT",
    "message": "AI analysis took too long. Please try again or contact support if the issue persists.",
    "retryAfter": 30
  }
}
```

## Frontend Integration

### Axios Service (paperService.js)
```javascript
export async function analyzePaper(paperId, isArxiv = true) {
  const params = isArxiv
    ? { arxivId: paperId.replace('arxiv-', '') }
    : { fileId: paperId }

  const response = await apiClient.get('/analyze_paper', {
    params,
    timeout: 65000 // 65s (slightly longer than backend 60s timeout)
  })

  return response.data
}
```

### Pinia Store Action (ui.js)
```javascript
async openModal(paperId) {
  this.modalOpen = true
  this.currentPaper = findPaperById(paperId) // From papers store
  this.analysisLoading = true
  this.currentAnalysis = null

  try {
    const isArxiv = paperId.startsWith('arxiv-')
    const analysis = await analyzePaper(paperId, isArxiv)

    if (analysis.analysisStatus === 'pending') {
      // Retry after delay
      await new Promise(resolve => setTimeout(resolve, 15000))
      return this.openModal(paperId) // Recursive retry
    }

    this.currentAnalysis = analysis
  } catch (error) {
    this.showToast(
      error.response?.data?.error?.message || 'Failed to load analysis',
      'error'
    )
  } finally {
    this.analysisLoading = false
  }
}
```

## Analysis Flow

1. **User triggers analysis**: Clicks paper card or uploads PDF
2. **Initial request**: GET /api/analyze_paper with identifier
3. **Pending response (202)**: Analysis in progress
   - Frontend displays skeleton loading
   - Retry after `retryAfter` seconds (typically 15s)
4. **Completed response (200)**: Analysis ready
   - Chinese summary displayed prominently
   - Innovation points rendered as bullet list
5. **Timeout (60s)**: If analysis not complete
   - Frontend shows error: "Analysis taking longer than expected"
   - User can retry or close modal

## Loading States

**Skeleton Screen Layout**:
```
┌─────────────────────────────────┐
│ [████████████] Title            │
│ [██████] Authors                │
│                                 │
│ 中文摘要                         │
│ [████████████████████████]      │
│ [████████████████████]          │
│ [████████████████]              │
│                                 │
│ 创新点                          │
│ • [████████████████]            │
│ • [██████████████████]          │
│ • [█████████████]               │
└─────────────────────────────────┘
```

**Loading Animation**: Pulse effect on skeleton bars.

## Edge Cases

1. **Multiple rapid requests**: User clicks same paper multiple times
   - Frontend debounces/ignores duplicate requests while analysis loading
   - Only one analysis request active per paper

2. **Analysis fails permanently**: Backend returns 422 after retries
   - Frontend shows error message in modal
   - User can close modal and try different paper

3. **Very long paper (>100 pages)**: May timeout
   - Backend enforces 60s limit regardless of length
   - Error message suggests contacting support

4. **Non-English paper**: Backend attempts analysis but quality may degrade
   - MVP: No language detection, best effort
   - Future: Warn user if non-English detected

## Performance Expectations

- **Analysis time**: P50: 5-15s, P95: 30-45s, Max: 60s
- **Cache duration**: 24 hours (same paper + identifier)
- **Retry strategy**: Exponential backoff (15s, 30s, 60s)
- **Max retries**: 3 attempts before showing error

## Notes

- Analysis results are cached for 24 hours
- Same paper analyzed twice uses cached result
- Uploaded files deleted after 24 hours; analysis cached separately
- Chinese summary length: 200-800 characters (target: 400)
- Innovation points: 3-10 bullets, each 30-100 characters
