# API Services Reference

Complete guide to API client, service modules, and mock system.

---

## API Client

### index.js

**Location**: `src/api/index.js`

**Configuration**:
```javascript
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,  // From .env
  timeout: 60000,  // 60 seconds
  headers: {
    'Content-Type': 'application/json'
  }
})
```

**Interceptors**:
- **Request**: Logs requests (dev mode)
- **Response**: Global error handling, logs errors

**Usage**:
```javascript
import apiClient from '@/api/index'

// GET request
const response = await apiClient.get('/arxiv_papers?period=daily')

// POST request
const response = await apiClient.post('/generate_ppt', { arxivId: '2301.00000' })
```

---

## Service Modules

### paperService.js

**Location**: `src/api/paperService.js`

**Functions**:

#### `fetchArxivPapers(period, page, limit)`
Fetch trending papers from arXiv.

**Parameters**:
- `period`: `'daily' | 'weekly' | 'monthly'`
- `page`: `number` (default: 1)
- `limit`: `number` (default: 20)

**Returns**:
```javascript
{
  papers: Paper[],
  totalPages: number,
  currentPage: number
}
```

**Mock Mode**: Returns data from `mocks/paperData.js` with 500ms delay.

---

#### `analyzePaper(arxivId?, fileId?)`
Get AI analysis for a paper.

**Parameters**: One of:
- `arxivId`: `string` - arXiv paper ID
- `fileId`: `string` - Uploaded file ID

**Returns**:
```javascript
{
  summary: string,           // Chinese summary
  innovationPoints: string[] // Innovation points
}
```

**Special Behavior**:
- May return 202 (pending) if analysis not ready
- Includes `retryAfter` header for retry timing
- `ui.js` store handles retries automatically (up to 3)

**Mock Mode**: Returns data from `mocks/paperData.js` with 800ms delay.

---

### uploadService.js

**Location**: `src/api/uploadService.js`

**Functions**:

#### `uploadPDF(file, onProgress)`
Upload PDF file with progress tracking.

**Parameters**:
- `file`: `File` - PDF file object
- `onProgress`: `(percent: number) => void` - Progress callback

**Returns**:
```javascript
{
  fileId: string,      // Uploaded file ID
  fileName: string,    // Original filename
  fileSize: number,    // File size in bytes
  uploadedAt: string,  // ISO timestamp
  paperId?: string     // Mock mode only: links to daily-0001
}
```

**Validation**:
- File type: `application/pdf` only
- File size: ≤20MB

**Mock Mode**:
- Simulates progress (0 → 25 → 50 → 75 → 100 over 1.5s)
- Returns `paperId: 'daily-0001'` for demo purposes

---

### taskService.js

**Location**: `src/api/taskService.js`

**Functions**:

#### `createPPTTask(paperId, isArxiv)`
Create a new PPT generation task.

**Parameters**:
- `paperId`: `string` - Paper ID (arXivId or fileId)
- `isArxiv`: `boolean` - Whether paper is from arXiv

**Returns**:
```javascript
{
  taskId: string  // Task UUID or mock-task-xxx
}
```

**Mock Mode**: Returns `mock-task-{timestamp}-{random}` with 500ms delay.

---

#### `pollTaskStatus(taskId)`
Poll status of a PPT generation task.

**Parameters**:
- `taskId`: `string` - Task ID

**Returns**:
```javascript
{
  status: 'queued' | 'generating' | 'completed' | 'failed',
  progress: number | null,        // 0-100 during generating
  downloadUrl: string | null,     // .pptx URL when completed
  errorMessage: string | null     // Error message if failed
}
```

**Polling Strategy**:
- Interval: 5 seconds
- Auto-start when active tasks exist
- Auto-stop when no active tasks

**Mock Mode** (Time-based progression):
- 0-5s: `queued` (progress: null)
- 5-15s: `generating` (progress: 0-90%, linear)
- 15s+: `completed` (progress: 100, downloadUrl: `/ppt-files/{paperId}.pptx`)

---

### pptContentService.js

**Location**: `src/api/pptContentService.js`

**Functions**:

#### `getPPTContent(taskId)`
Fetch PPT content for preview.

**Parameters**:
- `taskId`: `string` - Task ID

**Returns**:
```javascript
{
  taskId: string,
  paperId: string,
  type: 'images',        // Content type (always 'images' for MVP)
  slides: string[],      // Array of slide image URLs
  totalSlides: number,   // Total number of slides
  metadata: {
    paperTitle: string,
    generatedAt: string,
    author: string,
    field: string
  }
}
```

**Mock Mode**: Returns data from `mocks/pptContentData.js`.

---

## Mock System

### Mock Mode Toggle

**Environment Variable**:
```env
VITE_USE_MOCK_DATA=true   # Enable mock mode
VITE_USE_MOCK_DATA=false  # Use real APIs
```

**Service Layer Routing**:
```javascript
// Each service module checks this flag
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const fetchArxivPapers = async (period, page) => {
  if (USE_MOCK_DATA) {
    return mockFetchArxivPapers(period, page)  // Mock implementation
  }
  // Real API call
  const response = await apiClient.get('/arxiv_papers', { params: { period, page } })
  return response.data
}
```

---

### Mock Data Files

#### paperData.js
**Location**: `src/mocks/paperData.js`

**Contents**:
- 24 papers (8 daily + 8 weekly + 8 monthly)
- Real paper information from arXiv and CVPR
- Chinese summaries and innovation points

**Structure**:
```javascript
export const mockPapers = {
  daily: [/* 8 papers */],
  weekly: [/* 8 papers */],
  monthly: [/* 8 papers */]
}
```

---

#### taskData.js
**Location**: `src/mocks/taskData.js`

**Contents**:
- 3 historical tasks (2 completed + 1 failed)
- Demonstrates different task states

**Structure**:
```javascript
export const mockHistoricalTasks = [
  {
    id: 'mock-task-001',
    paperId: 'daily-0001',
    status: 'completed',
    downloadUrl: '/ppt-files/daily-0001.pptx'
  },
  // ...
]
```

---

#### pptContentData.js
**Location**: `src/mocks/pptContentData.js`

**Contents**:
- PPT metadata for 8 papers (daily-0001 to daily-0008)
- Slide counts (14-19 slides per paper)
- Paper metadata

**Structure**:
```javascript
export const mockPPTContents = {
  'daily-0001': {
    taskId: 'daily-0001',
    paperId: 'daily-0001',
    type: 'images',
    totalSlides: 14,
    metadata: { paperTitle, generatedAt, author, field }
  }
}
```

---

#### taskService.js (Mock)
**Location**: `src/mocks/taskService.js`

**Functions**:
- `mockCreatePPTTask(paperId, isArxiv)` - Create mock task
- `mockPollTaskStatus(taskId)` - Time-based status progression

**Task Lifecycle**:
```javascript
// In-memory Map tracks creation timestamps
const taskCreationTimes = new Map()

// Status calculated from elapsed time
const elapsedSeconds = (Date.now() - createdAt) / 1000

if (elapsedSeconds < 5) return { status: 'queued' }
if (elapsedSeconds < 15) return { status: 'generating', progress: ... }
return { status: 'completed', downloadUrl: ... }
```

---

#### utils.js
**Location**: `src/mocks/utils.js`

**Functions**:
- `generateMockTaskId()` - Generate `mock-task-{timestamp}-{random}`
- `delay(ms)` - Promise-based delay for network simulation

---

## API Contracts

Full specifications available in `/specs/001-mvp-frontend-implementation/contracts/`:

- **arxiv-papers.md**: GET `/api/arxiv_papers`
- **analyze-paper.md**: GET `/api/analyze_paper`
- **upload-pdf.md**: POST `/api/upload_pdf`
- **generate-ppt.md**: POST `/api/generate_ppt`
- **task-status.md**: GET `/api/task_status`

---

**Last Updated**: 2025-11-17  
**See Also**: [State Management](./state-management.md), [Architecture](./architecture.md)
