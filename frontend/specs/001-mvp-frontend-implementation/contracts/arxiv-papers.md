# API Contract: Get arXiv Papers

## Endpoint
```
GET /api/arxiv_papers
```

## Description
Fetches a paginated list of trending academic papers from arXiv, organized by time period.

## Request

### Query Parameters

| Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `period` | String (enum) | Yes | Time period for trending papers | Must be one of: `"daily"`, `"weekly"`, `"monthly"` |
| `page` | Number | No | Page number (1-indexed) | Integer >= 1, default: 1 |
| `limit` | Number | No | Items per page | Integer 1-50, default: 20 |

### Headers
```
Accept: application/json
```

### Example Request
```http
GET /api/arxiv_papers?period=daily&page=1&limit=20 HTTP/1.1
Host: api.lundao.com
Accept: application/json
```

## Response

### Success Response (200 OK)

**Body**:
```json
{
  "papers": [
    {
      "id": "arxiv-2301.00000",
      "title": "Attention Is All You Need",
      "authors": ["Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki"],
      "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
      "arxivId": "2301.00000",
      "field": "Machine Learning",
      "keywords": ["transformers", "attention", "NLP"],
      "publicationDate": "2023-01-01",
      "pdfUrl": "https://arxiv.org/pdf/2301.00000.pdf",
      "arxivUrl": "https://arxiv.org/abs/2301.00000"
    }
    // ... more papers
  ],
  "pagination": {
    "currentPage": 1,
    "totalPages": 5,
    "totalItems": 98,
    "itemsPerPage": 20
  }
}
```

**Schema**:
- `papers`: Array of Paper objects
  - `id`: String - Unique identifier (format: `"arxiv-{arxivId}"`)
  - `title`: String - Full paper title
  - `authors`: Array<String> - Author names
  - `abstract`: String - Original English abstract
  - `arxivId`: String - arXiv identifier (e.g., "2301.00000")
  - `field`: String - Research field/category
  - `keywords`: Array<String> - Research keywords
  - `publicationDate`: String (ISO 8601) - Publication date
  - `pdfUrl`: String - URL to download PDF
  - `arxivUrl`: String - URL to arXiv page
- `pagination`: Object
  - `currentPage`: Number - Current page number
  - `totalPages`: Number - Total available pages
  - `totalItems`: Number - Total papers matching criteria
  - `itemsPerPage`: Number - Papers per page

### Error Responses

#### 400 Bad Request
Invalid query parameters.

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Invalid period value. Must be one of: daily, weekly, monthly",
    "details": {
      "parameter": "period",
      "value": "yesterday"
    }
  }
}
```

#### 503 Service Unavailable
arXiv API temporarily unavailable.

```json
{
  "error": {
    "code": "UPSTREAM_UNAVAILABLE",
    "message": "arXiv service is temporarily unavailable. Please try again later.",
    "retryAfter": 30
  }
}
```

#### 504 Gateway Timeout
arXiv API did not respond within 10 seconds.

```json
{
  "error": {
    "code": "UPSTREAM_TIMEOUT",
    "message": "Request to arXiv timed out. Please try again.",
    "retryAfter": 5
  }
}
```

## Frontend Integration

### Axios Service (paperService.js)
```javascript
export async function fetchArxivPapers(period, page = 1, limit = 20) {
  const response = await apiClient.get('/arxiv_papers', {
    params: { period, page, limit }
  })
  return response.data
}
```

### Pinia Store Action (papers.js)
```javascript
async fetchPapers(period, page = 1) {
  this.loading = true
  this.error = null

  try {
    const { papers, pagination } = await fetchArxivPapers(period, page)
    this.papers = papers
    this.currentPage = pagination.currentPage
    this.totalPages = pagination.totalPages
    this.selectedPeriod = period
  } catch (error) {
    this.error = error.response?.data?.error?.message || 'Failed to load papers'
    throw error
  } finally {
    this.loading = false
  }
}
```

## Edge Cases

1. **Empty results**: Backend returns `papers: []` with `totalItems: 0`
   - Frontend displays friendly empty state: "No papers found for this period"

2. **Page out of range**: Requesting `page: 999` when only 5 pages exist
   - Backend returns 400 with error code `PAGE_OUT_OF_RANGE`
   - Frontend shows error toast, resets to page 1

3. **Slow response (>2s)**: arXiv API slow but within timeout
   - Frontend displays loading skeleton during wait
   - Success criteria: UI remains responsive, cancel option available

## Performance Expectations

- **Response time**: P95 < 2 seconds
- **Timeout**: 10 seconds (backend-enforced)
- **Cache**: Backend may cache results for 5 minutes per period
- **Rate limiting**: Not enforced for MVP

## Notes

- Papers are pre-sorted by trending score (backend logic)
- No search/filter capabilities in MVP
- arXivId format: `\d{4}\.\d{5}` (e.g., "2301.00000")
- PDF URLs are direct links to arXiv PDFs
