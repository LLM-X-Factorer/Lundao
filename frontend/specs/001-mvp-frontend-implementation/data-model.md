# Data Model

**Feature**: 论导Lite MVP Frontend
**Date**: 2025-10-14
**Phase**: 1 - Design

## Overview

This document defines the data entities, their attributes, relationships, and validation rules for the 论导Lite MVP frontend. All entities are designed for client-side state management (Pinia stores and localStorage) with data sourced from backend APIs.

## Entity Definitions

### 1. Paper

Represents an academic paper, either discovered from arXiv or uploaded by the user.

**Attributes**:

| Attribute | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `id` | String | Yes | Unique identifier (arXiv ID or generated UUID for uploads) | Non-empty string |
| `title` | String | Yes | Full paper title | Non-empty, max 500 chars |
| `authors` | Array<String> | Yes | List of author names | Min 1 author, each max 100 chars |
| `abstract` | String | No | Original English abstract | Max 5000 chars |
| `arxivId` | String | No | arXiv identifier (e.g., "2301.00000") | Format: `\d{4}\.\d{5}` or null |
| `uploadedFileId` | String | No | Backend file ID for uploaded PDFs | UUID format or null |
| `field` | String | No | Research field/category | Max 100 chars |
| `keywords` | Array<String> | No | Research keywords | Max 10 keywords, each max 50 chars |
| `publicationDate` | String (ISO 8601) | No | Publication or upload date | ISO date format: `YYYY-MM-DD` |
| `pdfUrl` | String | No | URL to download original PDF | Valid URL or null |
| `arxivUrl` | String | No | URL to arXiv page | Valid URL or null |
| `source` | Enum | Yes | Origin of paper | `"arxiv"` or `"upload"` |

**Relationships**:
- One-to-one with AIAnalysis (when analysis completed)
- One-to-many with PPTTask (user may generate multiple PPTs from same paper)

**State Lifecycle**:
1. `discovered`: Paper fetched from arXiv API
2. `uploaded`: Paper uploaded by user, awaiting analysis
3. `analyzed`: AI analysis completed and available

**Example**:
```javascript
{
  id: "arxiv-2301.00000",
  title: "Attention Is All You Need",
  authors: ["Vaswani, Ashish", "Shazeer, Noam", ...],
  abstract: "The dominant sequence transduction models...",
  arxivId: "2301.00000",
  uploadedFileId: null,
  field: "Machine Learning",
  keywords: ["transformers", "attention", "NLP"],
  publicationDate: "2023-01-01",
  pdfUrl: "https://arxiv.org/pdf/2301.00000.pdf",
  arxivUrl: "https://arxiv.org/abs/2301.00000",
  source: "arxiv"
}
```

---

### 2. AIAnalysis

Represents AI-generated insights for a paper, including Chinese summary and innovation points.

**Attributes**:

| Attribute | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `paperId` | String | Yes | Reference to associated Paper.id | Must match existing Paper |
| `chineseSummary` | String | Yes | AI-generated Chinese summary | Non-empty, max 2000 chars |
| `innovationPoints` | Array<String> | Yes | List of key innovation points in Chinese | Min 1, max 10 points, each max 500 chars |
| `analysisTimestamp` | String (ISO 8601) | Yes | When analysis completed | ISO datetime format |
| `analysisStatus` | Enum | Yes | Analysis completion status | `"pending"`, `"completed"`, `"failed"` |
| `errorMessage` | String | No | Error details if analysis failed | Max 500 chars or null |

**Relationships**:
- One-to-one with Paper (foreign key: paperId)

**State Lifecycle**:
1. `pending`: Analysis requested, awaiting backend response
2. `completed`: Analysis successful, data available
3. `failed`: Analysis failed, error message provided

**Example**:
```javascript
{
  paperId: "arxiv-2301.00000",
  chineseSummary: "本文提出了Transformer模型，这是一种完全基于注意力机制的序列转换模型...",
  innovationPoints: [
    "提出了完全基于注意力机制的架构，摒弃了循环和卷积层",
    "引入了多头自注意力机制，实现并行计算",
    "在机器翻译任务上达到了SOTA性能，训练速度提升显著"
  ],
  analysisTimestamp: "2025-10-14T10:30:45Z",
  analysisStatus: "completed",
  errorMessage: null
}
```

---

### 3. PPTTask

Represents a presentation generation request and its execution status.

**Attributes**:

| Attribute | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `id` | String (UUID) | Yes | Unique task identifier | UUID v4 format |
| `paperId` | String | Yes | Reference to Paper.id | Must match existing Paper |
| `paperTitle` | String | Yes | Cached paper title for display | Non-empty, max 500 chars |
| `status` | Enum | Yes | Current task status | `"queued"`, `"generating"`, `"completed"`, `"failed"` |
| `createdAt` | String (ISO 8601) | Yes | Task creation timestamp | ISO datetime format |
| `completedAt` | String (ISO 8601) | No | Task completion timestamp | ISO datetime or null |
| `downloadUrl` | String | No | URL to download generated PPT | Valid URL or null (only when completed) |
| `errorMessage` | String | No | Error details if failed | Max 500 chars or null |
| `retryCount` | Number | Yes | Number of retry attempts | Integer >= 0, max 3 |

**Relationships**:
- Many-to-one with Paper (foreign key: paperId)

**State Lifecycle**:
1. `queued`: Task created, awaiting backend processing
2. `generating`: Backend actively generating PPT
3. `completed`: PPT ready, downloadUrl available
4. `failed`: Generation failed, errorMessage provided

**Status Transitions**:
- `queued` → `generating` → `completed` (success path)
- `queued` → `generating` → `failed` (error path)
- `failed` → `queued` (retry action)

**Validation Rules**:
- `downloadUrl` MUST be null unless status is `"completed"`
- `errorMessage` MUST be null unless status is `"failed"`
- `completedAt` MUST be null unless status is `"completed"` or `"failed"`
- `retryCount` increments on retry, max 3 attempts before permanent failure

**Example**:
```javascript
{
  id: "550e8400-e29b-41d4-a716-446655440000",
  paperId: "arxiv-2301.00000",
  paperTitle: "Attention Is All You Need",
  status: "completed",
  createdAt: "2025-10-14T10:35:00Z",
  completedAt: "2025-10-14T10:38:30Z",
  downloadUrl: "https://api.lundao.com/downloads/ppt-550e8400.pptx",
  errorMessage: null,
  retryCount: 0
}
```

---

### 4. TaskHistory

Represents the persisted collection of all PPT generation tasks in localStorage.

**Storage Structure**:
```javascript
{
  "lundao_tasks_v1": [
    { /* PPTTask object 1 */ },
    { /* PPTTask object 2 */ },
    // ...
  ],
  "lundao_meta_v1": {
    "version": "1.0",
    "lastCleanup": "2025-10-14T10:00:00Z",
    "totalTasks": 45,
    "storageBytes": 123456
  }
}
```

**Capacity Management**:
- **Max storage**: 4MB (80% of 5MB localStorage limit)
- **Cleanup trigger**: When `storageBytes` > 4MB
- **Cleanup strategy**: Remove oldest `completed` tasks first, preserve `queued`, `generating`, and `failed` tasks
- **Cleanup frequency**: Check on every task addition

**Access Pattern**:
- Read all tasks: On application mount
- Add task: On PPT generation request
- Update task: On polling status change
- Delete task: On user explicit deletion
- Bulk cleanup: On storage capacity exceeded

**Validation Rules**:
- Task IDs must be unique
- Tasks sorted by `createdAt` descending (newest first)
- Failed tasks with `retryCount >= 3` eligible for automatic cleanup

**Example localStorage Entry**:
```javascript
{
  "lundao_tasks_v1": [
    {
      id: "task-uuid-1",
      paperId: "arxiv-2301.00000",
      paperTitle: "Attention Is All You Need",
      status: "completed",
      createdAt: "2025-10-14T10:35:00Z",
      completedAt: "2025-10-14T10:38:30Z",
      downloadUrl: "https://...",
      errorMessage: null,
      retryCount: 0
    }
  ],
  "lundao_meta_v1": {
    "version": "1.0",
    "lastCleanup": "2025-10-14T10:00:00Z",
    "totalTasks": 1,
    "storageBytes": 512
  }
}
```

---

## Pinia Store Mapping

### papers.js Store
**State**:
- `papers`: Array<Paper> - Currently displayed papers
- `currentPage`: Number - Active pagination page
- `totalPages`: Number - Total pages available
- `selectedPeriod`: Enum - Active tab (`"daily"`, `"weekly"`, `"monthly"`)
- `loading`: Boolean - Fetching papers indicator
- `error`: String | null - Error message if fetch failed

**Actions**:
- `fetchPapers(period, page)`: Fetch papers from backend
- `selectPaper(paperId)`: Set active paper for modal display

### tasks.js Store
**State**:
- `tasks`: Array<PPTTask> - All tasks from localStorage + current session
- `pollingActive`: Boolean - Whether polling is running

**Getters**:
- `activeTasks`: Tasks with status `queued` or `generating`
- `completedTasks`: Tasks with status `completed`
- `failedTasks`: Tasks with status `failed`

**Actions**:
- `loadTasksFromStorage()`: Initialize tasks from localStorage on mount
- `createTask(paperId, paperTitle)`: Add new PPT generation task
- `updateTaskStatus(taskId, statusData)`: Update task after polling
- `deleteTask(taskId)`: Remove task from list and localStorage
- `retryTask(taskId)`: Reset failed task to queued
- `startPolling()`: Begin 5-second interval polling
- `stopPolling()`: Clear polling interval

### ui.js Store
**State**:
- `modalOpen`: Boolean - Paper modal visibility
- `currentPaper`: Paper | null - Active paper in modal
- `currentAnalysis`: AIAnalysis | null - Analysis for current paper
- `analysisLoading`: Boolean - AI analysis fetching indicator
- `toastQueue`: Array<Toast> - Notification messages

**Actions**:
- `openModal(paperId)`: Show paper modal, fetch analysis
- `closeModal()`: Hide modal, clear current paper
- `showToast(message, type)`: Add notification to queue
- `dismissToast(id)`: Remove notification

---

## Data Flow Examples

### Scenario 1: Discover and View Paper
1. User selects "Daily" tab
2. `papers.fetchPapers("daily", 1)` called
3. Papers array populated from API response
4. User clicks paper card
5. `ui.openModal(paperId)` called
6. `currentPaper` set, `analysisLoading` = true
7. AI analysis fetched from backend
8. `currentAnalysis` populated, `analysisLoading` = false
9. Modal displays paper + analysis

### Scenario 2: Generate and Track PPT
1. User clicks "Generate PPT" in modal
2. `tasks.createTask(paperId, paperTitle)` called
3. New PPTTask created with `status: "queued"`
4. Task saved to localStorage
5. `tasks.startPolling()` initiated
6. Every 5s, `tasks.updateTaskStatus()` called for active tasks
7. Backend returns `status: "generating"`, UI updates
8. Backend returns `status: "completed"` with `downloadUrl`
9. Task status updated, "Download PPT" button enabled
10. Polling stops when no active tasks remain

### Scenario 3: localStorage Capacity Management
1. User generates 50th PPT task
2. `tasks.createTask()` checks storage size
3. Size exceeds 4MB threshold
4. Cleanup triggered: oldest 10 completed tasks removed
5. New task added, storage within limits
6. User notified: "Old completed tasks cleaned up"

---

## Validation Summary

| Entity | Validation Points |
|--------|-------------------|
| **Paper** | Non-empty title, at least 1 author, valid source enum |
| **AIAnalysis** | Non-empty summary, min 1 innovation point, valid status enum |
| **PPTTask** | UUID format ID, valid status enum, downloadUrl only when completed, max 3 retries |
| **TaskHistory** | Unique task IDs, sorted by createdAt, capacity < 4MB |

---

## Next Steps

Proceed to API contract definitions in the `contracts/` directory.
