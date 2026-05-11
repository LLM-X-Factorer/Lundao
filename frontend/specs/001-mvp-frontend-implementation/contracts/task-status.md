# API Contract: Poll Task Status

## Endpoint
```
GET /api/task_status
```

## Description
Retrieves the current status of a PPT generation task. Used for polling to update UI in real-time.

## Request

### Query Parameters

| Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `taskId` | String (UUID) | Yes | Task identifier | Format: `task-{uuid}` |

### Headers
```
Accept: application/json
```

### Example Request
```http
GET /api/task_status?taskId=task-660f9511-f3ac-52e5-b827-557766551111 HTTP/1.1
Host: api.lundao.com
Accept: application/json
```

## Response

### Success Responses

#### Queued Status (200 OK)
Task is waiting to be processed.

```json
{
  "taskId": "task-660f9511-f3ac-52e5-b827-557766551111",
  "status": "queued",
  "createdAt": "2025-10-14T10:35:00Z",
  "estimatedCompletionTime": "2025-10-14T10:40:00Z",
  "queuePosition": 3
}
```

#### Generating Status (200 OK)
Task is actively being processed.

```json
{
  "taskId": "task-660f9511-f3ac-52e5-b827-557766551111",
  "status": "generating",
  "createdAt": "2025-10-14T10:35:00Z",
  "startedAt": "2025-10-14T10:36:15Z",
  "progress": 45,
  "estimatedCompletionTime": "2025-10-14T10:39:30Z"
}
```

**Schema additions**:
- `progress`: Number (0-100) - Optional percentage completion
- `startedAt`: String (ISO 8601) - When generation began

#### Completed Status (200 OK)
Task finished successfully, PPT ready for download.

```json
{
  "taskId": "task-660f9511-f3ac-52e5-b827-557766551111",
  "status": "completed",
  "createdAt": "2025-10-14T10:35:00Z",
  "startedAt": "2025-10-14T10:36:15Z",
  "completedAt": "2025-10-14T10:38:30Z",
  "downloadUrl": "https://api.lundao.com/downloads/ppt-660f9511.pptx",
  "expiresAt": "2025-10-15T10:38:30Z",
  "fileSize": 1048576
}
```

**Schema additions**:
- `completedAt`: String (ISO 8601) - When generation completed
- `downloadUrl`: String - URL to download PPT file
- `expiresAt`: String (ISO 8601) - Download link expiration (24 hours)
- `fileSize`: Number - PPT file size in bytes

#### Failed Status (200 OK)
Task failed during processing.

```json
{
  "taskId": "task-660f9511-f3ac-52e5-b827-557766551111",
  "status": "failed",
  "createdAt": "2025-10-14T10:35:00Z",
  "startedAt": "2025-10-14T10:36:15Z",
  "failedAt": "2025-10-14T10:37:00Z",
  "errorMessage": "Failed to generate slides: unable to extract images from PDF",
  "errorCode": "IMAGE_EXTRACTION_FAILED",
  "retryable": true
}
```

**Schema additions**:
- `failedAt`: String (ISO 8601) - When failure occurred
- `errorMessage`: String - Human-readable error description
- `errorCode`: String - Machine-readable error code
- `retryable`: Boolean - Whether user can retry this task

### Error Responses

#### 404 Not Found
Task does not exist.

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "No task found with the provided ID",
    "details": {
      "taskId": "task-invalid"
    }
  }
}
```

#### 410 Gone
Task expired (>24 hours old).

```json
{
  "error": {
    "code": "TASK_EXPIRED",
    "message": "This task has expired and can no longer be accessed",
    "details": {
      "taskId": "task-660f9511-f3ac-52e5-b827-557766551111",
      "createdAt": "2025-10-13T10:35:00Z",
      "expiredAt": "2025-10-14T10:35:00Z"
    }
  }
}
```

## Frontend Integration

### Axios Service (taskService.js)
```javascript
export async function pollTaskStatus(taskId) {
  const response = await apiClient.get('/task_status', {
    params: { taskId },
    timeout: 10000 // 10s timeout
  })
  return response.data
}
```

### Pinia Store - Polling Logic (tasks.js)
```javascript
export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  let pollingIntervalId = null

  const activeTasks = computed(() =>
    tasks.value.filter(t => t.status === 'queued' || t.status === 'generating')
  )

  const startPolling = () => {
    if (pollingIntervalId) return // Already polling

    pollingIntervalId = setInterval(async () => {
      if (activeTasks.value.length === 0) {
        stopPolling()
        return
      }

      // Poll all active tasks concurrently
      const pollPromises = activeTasks.value.map(task =>
        pollTaskStatus(task.id)
          .then(statusData => updateTaskStatus(task.id, statusData))
          .catch(error => {
            console.error(`Failed to poll task ${task.id}:`, error)
            // Don't stop polling on individual errors
          })
      )

      await Promise.allSettled(pollPromises)
    }, 5000) // 5 seconds

    this.pollingActive = true
  }

  const stopPolling = () => {
    if (pollingIntervalId) {
      clearInterval(pollingIntervalId)
      pollingIntervalId = null
      this.pollingActive = false
    }
  }

  const updateTaskStatus = (taskId, statusData) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (!task) return

    // Update task properties
    task.status = statusData.status
    task.completedAt = statusData.completedAt || null
    task.downloadUrl = statusData.downloadUrl || null
    task.errorMessage = statusData.errorMessage || null

    // Save to localStorage
    saveTasksToLocalStorage()

    // Show toast on completion
    if (statusData.status === 'completed') {
      uiStore.showToast(`PPT for "${task.paperTitle}" is ready!`, 'success')
    } else if (statusData.status === 'failed') {
      uiStore.showToast(`PPT generation failed: ${statusData.errorMessage}`, 'error')
    }
  }

  // Lifecycle: Start polling on mount if active tasks exist
  onMounted(() => {
    loadTasksFromLocalStorage()
    if (activeTasks.value.length > 0) {
      startPolling()
    }
  })

  // Lifecycle: Stop polling on unmount
  onUnmounted(() => {
    stopPolling()
  })

  return {
    tasks,
    activeTasks,
    startPolling,
    stopPolling,
    updateTaskStatus
  }
})
```

## Polling Strategy

### Interval: 5 Seconds
- Constitution requirement: "5s task polling interval"
- Polls all active tasks (`queued` or `generating`) concurrently
- Uses `Promise.allSettled()` to handle individual task errors

### Start Conditions
- When task created: `createTask()` calls `startPolling()`
- On app mount: If localStorage contains active tasks

### Stop Conditions
- When no active tasks remain: `activeTasks.length === 0`
- On component unmount: `onUnmounted()` hook
- On manual user action: (Not implemented in MVP)

### Error Handling
- Individual polling errors don't stop the interval
- Network errors: Continue polling (auto-recover when online)
- 404 errors: Remove task from list (no longer exists)
- 410 errors: Mark task as expired, stop polling it

## UI Updates per Status

### Queued
```
┌────────────────────────────────────┐
│ Attention Is All You Need          │
│ 🟡 排队中  Created: 2 minutes ago  │
│ [━━━━━━━━━━] Waiting...            │
└────────────────────────────────────┘
```

### Generating
```
┌────────────────────────────────────┐
│ Attention Is All You Need          │
│ 🔵 生成中  Progress: 45%           │
│ [━━━━━━━━__] ~2 min remaining      │
└────────────────────────────────────┘
```

### Completed
```
┌────────────────────────────────────┐
│ Attention Is All You Need          │
│ 🟢 已完成  Completed 5 minutes ago │
│ [Download PPT] [Delete]            │
└────────────────────────────────────┘
```

### Failed
```
┌────────────────────────────────────┐
│ Attention Is All You Need          │
│ 🔴 失败  Error: Image extraction   │
│ [Retry] [Delete]                   │
└────────────────────────────────────┘
```

## Badge Colors (Tailwind)
- **Queued**: `bg-yellow-100 text-yellow-800` (🟡)
- **Generating**: `bg-blue-100 text-blue-800` (🔵)
- **Completed**: `bg-green-100 text-green-800` (🟢)
- **Failed**: `bg-red-100 text-red-800` (🔴)

## Edge Cases

1. **Polling during offline**: Network requests fail
   - Errors logged, polling continues
   - When online, polling resumes automatically
   - Task statuses sync once backend reachable

2. **Task completed between polls**: User sees delayed update
   - Max delay: 5 seconds (polling interval)
   - Acceptable per success criteria (5-10s tolerance)

3. **Task deleted while polling**: 404 response
   - Frontend removes task from list
   - Continues polling remaining tasks

4. **Very long generation (>10 min)**: Task stays "generating"
   - Polling continues indefinitely
   - User can manually refresh or close tab
   - Backend enforces max timeout (e.g., 15 min)

5. **Multiple tabs open**: Each tab polls independently
   - localStorage shared across tabs
   - Task updates visible in all tabs
   - Potential for duplicate API calls (acceptable for MVP)

## Performance Expectations

- **Polling frequency**: Every 5 seconds for active tasks
- **Request time**: <500ms per task
- **Concurrent polling**: Batch all active tasks in one interval
- **Network efficiency**: Only poll when tasks active, stop when idle
- **Battery impact**: Minimal (5s interval, stops when no active tasks)

## Notes

- Polling is the only status update mechanism (no WebSockets in MVP)
- Download URLs expire 24 hours after task completion
- Failed tasks remain in history until manually deleted
- Retry creates a new task (doesn't restart existing task)
- Task progress (0-100%) is optional; backend may not provide it
