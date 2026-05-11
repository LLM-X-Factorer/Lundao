# Mock API Contract: Poll Task Status

**Function**: `mockPollTaskStatus`
**File**: `src/mocks/taskService.js`
**Purpose**: Simulate task status polling with time-based progression

## Signature

```javascript
export const mockPollTaskStatus = async (taskId)
```

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task identifier (format: `mock-task-*`) |

## Output

**Type**: `Promise<Object>`

**Success Response**:
```javascript
{
  status: string,              // 'queued' | 'generating' | 'completed' | 'failed'
  progress: number | null,     // 0-100 or null
  downloadUrl: string | null,  // URL if completed, else null
  errorMessage: string | null  // Error if failed, else null
}
```

## Behavior by Elapsed Time

### Phase 1: Queued (0-5 seconds)

**Condition**: `elapsed < 5s`

**Response**:
```javascript
{
  status: 'queued',
  progress: null,
  downloadUrl: null,
  errorMessage: null
}
```

### Phase 2: Generating (5-15 seconds)

**Condition**: `5s <= elapsed < 15s`

**Response**:
```javascript
{
  status: 'generating',
  progress: 0-90,  // Linear progression: floor((elapsed - 5) * 9)
  downloadUrl: null,
  errorMessage: null
}
```

**Progress Calculation**:
```javascript
const elapsed = (Date.now() - task.createdAt) / 1000
const progress = Math.min(90, Math.floor((elapsed - 5) * 9))

// Examples:
// 5.0s → 0%
// 7.5s → 22%
// 10.0s → 45%
// 14.9s → 89%
```

### Phase 3: Completed (15+ seconds)

**Condition**: `elapsed >= 15s`

**Response**:
```javascript
{
  status: 'completed',
  progress: 100,
  downloadUrl: `/mock/downloads/${taskId}.pptx`,
  errorMessage: null
}
```

### Edge Case: Task Not Found

**Condition**: `taskId` not in `taskCreationTimes` Map (page refresh scenario)

**Response**:
```javascript
{
  status: 'failed',
  progress: 0,
  downloadUrl: null,
  errorMessage: '任务不存在或已过期'
}
```

## Behavior Details

1. **Lookup Task Record**:
   - Retrieve `{ createdAt, paperId, isArxiv }` from `taskCreationTimes` Map
   - If not found → return failed status

2. **Calculate Elapsed Time**:
   ```javascript
   const elapsedSeconds = (Date.now() - task.createdAt) / 1000
   ```

3. **Determine Status**:
   - Use `MOCK_TASK_TIMING` constants to determine phase
   - Calculate progress for generating phase

4. **Simulate Network Delay**:
   - Add 300ms delay via `await delay(300)`
   - Mimics real polling endpoint latency

5. **Return Status Object**:
   - Return appropriate status/progress/downloadUrl/errorMessage

## Error Handling

**No errors thrown** - Mock uses `failed` status for missing tasks instead of throwing exceptions.

## Usage Example

```javascript
// src/stores/tasks.js - polling logic
const statusData = await pollTaskStatus(task.id)
// statusData = { status: 'generating', progress: 45, downloadUrl: null, errorMessage: null }

// Update task in store
updateTaskStatus(task.id, statusData)
```

## Implementation

```javascript
// src/mocks/taskService.js
import { delay } from './utils'

export const MOCK_TASK_TIMING = {
  QUEUE_DURATION: 5,
  GENERATE_DURATION: 10,
  TOTAL_DURATION: 15
}

const taskCreationTimes = new Map()

export const mockPollTaskStatus = async (taskId) => {
  // Simulate network delay
  await delay(300)

  const task = taskCreationTimes.get(taskId)

  if (!task) {
    return {
      status: 'failed',
      progress: 0,
      downloadUrl: null,
      errorMessage: '任务不存在或已过期'
    }
  }

  const elapsedSeconds = (Date.now() - task.createdAt) / 1000

  if (elapsedSeconds < MOCK_TASK_TIMING.QUEUE_DURATION) {
    return { status: 'queued', progress: null, downloadUrl: null, errorMessage: null }
  }

  if (elapsedSeconds < MOCK_TASK_TIMING.TOTAL_DURATION) {
    const progress = Math.min(90, Math.floor((elapsedSeconds - MOCK_TASK_TIMING.QUEUE_DURATION) * 9))
    return { status: 'generating', progress, downloadUrl: null, errorMessage: null }
  }

  return {
    status: 'completed',
    progress: 100,
    downloadUrl: `/mock/downloads/${taskId}.pptx`,
    errorMessage: null
  }
}
```

## Testing

```javascript
// Manual test in browser console
const taskId = 'mock-task-1705300123456-a3f8e9'

// Immediately after creation (< 5s)
await mockPollTaskStatus(taskId)
// { status: 'queued', progress: null, ... }

// Wait 10 seconds
setTimeout(async () => {
  await mockPollTaskStatus(taskId)
  // { status: 'generating', progress: ~45, ... }
}, 10000)

// Wait 20 seconds
setTimeout(async () => {
  await mockPollTaskStatus(taskId)
  // { status: 'completed', progress: 100, downloadUrl: '/mock/...', ... }
}, 20000)
```

## Timeline Diagram

```
Time:  0s        5s               15s
       │         │                 │
       ▼         ▼                 ▼
   queued   generating        completed
   (null%)   (0% → 90%)        (100%)
              ╔═════════╗
              ║ Linear  ║
              ║Progress ║
              ╚═════════╝

Polling Interval: Every 5 seconds (from tasks.js store)
```

## Notes

- Progress intentionally stops at 90% during generating phase (realistic UX pattern)
- Final jump to 100% occurs when status changes to completed
- 300ms delay is shorter than creation (500ms) for faster polling response
- Map is cleared on page refresh → orphaned tasks auto-fail on next poll
