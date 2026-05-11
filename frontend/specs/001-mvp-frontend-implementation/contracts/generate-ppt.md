# API Contract: Generate PPT

## Endpoint
```
POST /api/generate_ppt
```

## Description
Creates a presentation generation task for a paper. Returns a task ID for tracking generation progress via polling.

## Request

### Content-Type
```
application/json
```

### Request Body

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `arxivId` | String | Conditional | arXiv paper identifier | Required if `fileId` not provided. Format: `\d{4}\.\d{5}` |
| `fileId` | String (UUID) | Conditional | Uploaded file identifier | Required if `arxivId` not provided. Format: `upload-{uuid}` |

**Note**: Exactly one of `arxivId` or `fileId` must be provided.

### Example Requests

**For arXiv paper**:
```http
POST /api/generate_ppt HTTP/1.1
Host: api.lundao.com
Content-Type: application/json

{
  "arxivId": "2301.00000"
}
```

**For uploaded file**:
```http
POST /api/generate_ppt HTTP/1.1
Host: api.lundao.com
Content-Type: application/json

{
  "fileId": "upload-550e8400-e29b-41d4-a716-446655440000"
}
```

## Response

### Success Response (201 Created)

**Body**:
```json
{
  "taskId": "task-660f9511-f3ac-52e5-b827-557766551111",
  "paperId": "arxiv-2301.00000",
  "paperTitle": "Attention Is All You Need",
  "status": "queued",
  "createdAt": "2025-10-14T10:35:00Z",
  "estimatedCompletionTime": "2025-10-14T10:40:00Z"
}
```

**Schema**:
- `taskId`: String (UUID) - Unique task identifier (format: `task-{uuid}`)
- `paperId`: String - Paper identifier from request
- `paperTitle`: String - Paper title (for UI display)
- `status`: String (enum) - Initial status (always `"queued"`)
- `createdAt`: String (ISO 8601) - Task creation timestamp
- `estimatedCompletionTime`: String (ISO 8601) - Expected completion (usually 3-5 minutes)

### Error Responses

#### 400 Bad Request
Missing or invalid parameters.

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Either arxivId or fileId must be provided",
    "details": {
      "providedFields": []
    }
  }
}
```

#### 404 Not Found
Paper or analysis not found.

```json
{
  "error": {
    "code": "PAPER_NOT_FOUND",
    "message": "No paper found with the provided identifier. Please ensure the paper has been analyzed first.",
    "details": {
      "arxivId": "9999.99999"
    }
  }
}
```

#### 409 Conflict
Task already exists for this paper (duplicate request).

```json
{
  "error": {
    "code": "TASK_EXISTS",
    "message": "A PPT generation task is already in progress for this paper",
    "details": {
      "existingTaskId": "task-660f9511-f3ac-52e5-b827-557766551111",
      "status": "generating"
    }
  }
}
```

**Frontend behavior**: Show existing task in history, don't create duplicate.

#### 503 Service Unavailable
PPT generation service temporarily unavailable.

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "PPT generation service is temporarily unavailable. Please try again later.",
    "retryAfter": 60
  }
}
```

## Frontend Integration

### Axios Service (taskService.js)
```javascript
export async function createPPTTask(paperId, isArxiv = true) {
  const body = isArxiv
    ? { arxivId: paperId.replace('arxiv-', '') }
    : { fileId: paperId }

  const response = await apiClient.post('/generate_ppt', body)
  return response.data
}
```

### Pinia Store Action (tasks.js)
```javascript
async createTask(paperId, paperTitle) {
  try {
    const isArxiv = paperId.startsWith('arxiv-')
    const taskData = await createPPTTask(paperId, isArxiv)

    // Add to local task list
    const newTask = {
      id: taskData.taskId,
      paperId: taskData.paperId,
      paperTitle: taskData.paperTitle,
      status: taskData.status,
      createdAt: taskData.createdAt,
      completedAt: null,
      downloadUrl: null,
      errorMessage: null,
      retryCount: 0
    }

    this.tasks.unshift(newTask) // Add to beginning of array
    this.saveTasksToLocalStorage()

    // Start polling if not already active
    if (!this.pollingActive) {
      this.startPolling()
    }

    // Close modal, show toast
    uiStore.closeModal()
    uiStore.showToast('PPT generation task created, check history below', 'success')

    return newTask
  } catch (error) {
    if (error.response?.status === 409) {
      // Task exists, find it and show
      const existingTaskId = error.response.data.error.details.existingTaskId
      // Scroll to existing task in history
    }
    throw error
  }
}
```

## Task Creation Flow

1. **User clicks "Generate PPT"**: In paper modal after viewing analysis
2. **Request sent**: POST /api/generate_ppt with paper ID
3. **Task created**: Backend returns task ID and queued status
4. **UI updates**:
   - Modal closes
   - Toast notification: "PPT generation task created"
   - New task appears at top of history section with "Queued" badge
5. **Polling starts**: If not already active (see [task-status.md](./task-status.md))

## Task Lifecycle

```
Created (queued) → Generating → Completed
                            └→ Failed
```

**Timeline**:
- `queued`: 0-30 seconds (waiting for worker)
- `generating`: 2-5 minutes (typical), up to 10 minutes (max)
- `completed`: Terminal state with downloadUrl
- `failed`: Terminal state with errorMessage

## Edge Cases

1. **Duplicate task request**: User clicks "Generate PPT" twice
   - Backend returns 409 Conflict with existing task ID
   - Frontend shows: "PPT generation already in progress for this paper"
   - Scrolls to existing task in history

2. **Task created but modal closed**: User closes modal after creating task
   - Task persists in localStorage
   - Polling continues in background
   - Task visible in history section

3. **Task created offline**: User creates task, immediately goes offline
   - Task saved to localStorage with "queued" status
   - When online, polling attempts resume
   - If task expired (>24h), show as failed

4. **Rapid task creation**: User generates PPTs for 10 papers quickly
   - All tasks queued successfully
   - Polling handles multiple active tasks
   - Backend queues tasks, processes sequentially

## Button States in Modal

**Before task creation**:
```
┌──────────────────────────┐
│  一键生成组会PPT          │  ← Primary button, enabled
└──────────────────────────┘
```

**During request (loading)**:
```
┌──────────────────────────┐
│  ⏳ 创建中...             │  ← Disabled, spinner icon
└──────────────────────────┘
```

**After success (button disappears)**:
- Modal closes
- Task appears in history

**After error (button resets)**:
- Button returns to original state
- Error toast shown
- User can retry

## Performance Expectations

- **Request time**: <500ms (task creation only, not generation)
- **Timeout**: 10 seconds
- **Rate limiting**: Not enforced in MVP (trust-based)
- **Concurrent tasks**: User can create unlimited tasks

## Notes

- Tasks are asynchronous; creation is instant, generation takes minutes
- Frontend must poll /api/task_status to track progress
- Tasks expire 24 hours after completion (downloadUrl becomes invalid)
- Failed tasks can be retried (creates new task)
- No task cancellation in MVP (runs to completion or failure)
