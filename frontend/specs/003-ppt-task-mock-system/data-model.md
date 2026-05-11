# Data Model: PPT Task Mock System

**Feature**: PPT Task Mock System
**Branch**: `003-ppt-task-mock`
**Date**: 2025-01-15
**Purpose**: Document mock system entities, relationships, and state transitions

---

## Entity Definitions

### 1. MockHistoricalTask

**Purpose**: Represents pre-populated task history for demonstrating various task states on first app launch in mock mode.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | string | Required, must start with `mock-task-` | Unique task identifier, format: `mock-task-{nnn}` where `nnn` is zero-padded sequential number (001, 002, etc.) |
| `paperId` | string | Required, must reference existing paper in `paperData.js` | Foreign key to paper entity (e.g., `daily-0001`, `weekly-0005`) |
| `paperTitle` | string | Required | Denormalized paper title for display without lookup |
| `status` | enum | Required, one of: `completed`, `failed` | Task completion state (historical tasks never `queued` or `generating`) |
| `createdAt` | string | Required, ISO 8601 format | Task creation timestamp (e.g., `2025-01-14T10:00:00.000Z`) |
| `completedAt` | string \| null | ISO 8601 format if `status === 'completed'`, else `null` | Task completion timestamp |
| `downloadUrl` | string \| null | Format: `/mock/downloads/{taskId}.pptx` if completed, else `null` | Mock download path |
| `progress` | number \| null | 0-100 if `status === 'failed'` (partial progress), 100 if completed, else `null` | Percentage completion (0-100) |
| `errorMessage` | string \| null | Required if `status === 'failed'`, else `null` | User-facing error description |
| `retryCount` | number | Default: 0 | Number of retry attempts (used by retry button logic) |

**Sample Data**:
```javascript
{
  id: 'mock-task-001',
  paperId: 'daily-0001',
  paperTitle: 'Hierarchical Reasoning Models: Small-Scale Recursive Reasoning Outperforms LLMs',
  status: 'completed',
  createdAt: '2025-01-14T10:00:00.000Z',
  completedAt: '2025-01-14T10:03:00.000Z',
  downloadUrl: '/mock/downloads/mock-task-001.pptx',
  progress: 100,
  errorMessage: null,
  retryCount: 0
}
```

**Validation Rules**:
- `id` must match regex: `/^mock-task-\d{3}$/`
- `status` must be `completed` or `failed` (not `queued`/`generating` for historical data)
- If `status === 'completed'`: `completedAt` and `downloadUrl` must be non-null, `progress === 100`, `errorMessage === null`
- If `status === 'failed'`: `completedAt` and `downloadUrl` must be `null`, `errorMessage` must be non-null
- `createdAt` must be valid ISO 8601 date string
- `progress` must be `null` or integer between 0-100

---

### 2. TaskCreationRecord

**Purpose**: In-memory tracking of dynamically created mock tasks to calculate elapsed time for status progression simulation.

**Storage**: JavaScript `Map` object in `src/mocks/taskService.js` module scope
**Lifecycle**: Cleared on page refresh (not persisted)

**Attributes**:

| Field | Type | Description |
|-------|------|-------------|
| `taskId` | string (Map key) | Unique task identifier, format: `mock-task-{timestamp}-{random}` |
| `createdAt` | number | Unix timestamp (milliseconds) when task was created via `mockCreatePPTTask` |
| `paperId` | string | Paper ID reference (for debugging/logging) |
| `isArxiv` | boolean | Whether this is an arXiv paper (true) or uploaded PDF (false) |

**Sample Entry**:
```javascript
// Map structure
taskCreationTimes.set('mock-task-1705300123456-a3f8e9', {
  createdAt: 1705300123456,  // Date.now()
  paperId: 'daily-0002',
  isArxiv: true
})
```

**Access Pattern**:
1. **Create**: `mockCreatePPTTask` generates `taskId` → stores `{ createdAt, paperId, isArxiv }` in Map
2. **Read**: `mockPollTaskStatus` looks up `taskId` → calculates `elapsed = Date.now() - createdAt` → returns status
3. **Delete**: Optional cleanup via `cleanupExpiredTasks()` (removes entries >24 hours old)

**Memory Footprint**:
- ~100 bytes per entry
- Max expected: 100 concurrent tasks = ~10KB total (negligible)

---

### 3. MockTaskTiming

**Purpose**: Configuration object defining status transition thresholds for realistic task progression simulation.

**Storage**: Exported constant in `src/mocks/taskService.js`

**Attributes**:

| Field | Type | Value | Description |
|-------|------|-------|-------------|
| `QUEUE_DURATION` | number | `5` | Seconds in `queued` status before transitioning to `generating` |
| `GENERATE_DURATION` | number | `10` | Seconds in `generating` status before transitioning to `completed` |
| `TOTAL_DURATION` | number | `15` | Total seconds from creation to completion (QUEUE + GENERATE) |

**Usage**:
```javascript
// src/mocks/taskService.js
export const MOCK_TASK_TIMING = {
  QUEUE_DURATION: 5,      // 0-5s: queued
  GENERATE_DURATION: 10,  // 5-15s: generating
  TOTAL_DURATION: 15      // 15s+: completed
}

export const mockPollTaskStatus = (taskId) => {
  const task = taskCreationTimes.get(taskId)
  const elapsed = (Date.now() - task.createdAt) / 1000

  if (elapsed < MOCK_TASK_TIMING.QUEUE_DURATION) {
    return { status: 'queued', progress: null }
  }
  if (elapsed < MOCK_TASK_TIMING.TOTAL_DURATION) {
    const progress = Math.min(90, Math.floor((elapsed - MOCK_TASK_TIMING.QUEUE_DURATION) * 9))
    return { status: 'generating', progress }
  }
  return { status: 'completed', progress: 100, downloadUrl: `/mock/downloads/${taskId}.pptx` }
}
```

**Rationale**:
- **5s queue**: Realistic backend queue wait time, gives user time to observe initial state
- **10s generation**: Matches typical real backend PPT generation time, allows smooth progress bar animation
- **15s total**: Fast enough for developer testing, slow enough to observe all states

---

## Entity Relationships

```
MockHistoricalTask
    │
    └─(references)─> Paper (from paperData.js)
                         │
                         ├── daily-0001
                         ├── daily-0002
                         └── weekly-0005

TaskCreationRecord (in-memory Map)
    │
    ├── mock-task-1705300000-a3f8e9 → { createdAt, paperId, isArxiv }
    ├── mock-task-1705300123-b4e9f0 → { createdAt, paperId, isArxiv }
    └── ...

MockTaskTiming (constants)
    └── Used by mockPollTaskStatus to calculate status
```

**Relationship Rules**:
1. `MockHistoricalTask.paperId` must reference existing paper in `paperData.js`
2. `TaskCreationRecord.paperId` should reference valid paper (not enforced, for debugging only)
3. `TaskCreationRecord` entries are ephemeral (cleared on refresh), `MockHistoricalTask` is static

---

## State Transitions

### Dynamically Created Mock Tasks (via `mockCreatePPTTask`)

```
┌───────────────────────────────────────────────────────────┐
│              Task Lifecycle (15 seconds)                  │
└───────────────────────────────────────────────────────────┘

Time:      0s             5s                    15s
           │              │                      │
           ▼              ▼                      ▼
       ┌───────┐      ┌───────────┐       ┌───────────┐
       │ queued│─────>│generating │──────>│ completed │
       └───────┘      └───────────┘       └───────────┘
         │                 │                    │
    progress: null    progress: 0-90%     progress: 100%
    downloadUrl: null downloadUrl: null   downloadUrl: /mock/...

                            │
                            ▼
                    (If page refresh)
                            │
                            ▼
                       ┌─────────┐
                       │ failed  │  (taskId not in Map)
                       └─────────┘
                            │
                    errorMessage: "页面刷新导致任务中断"
```

**Transition Rules**:
1. **queued → generating**: Triggered when `elapsed >= 5s`
2. **generating → completed**: Triggered when `elapsed >= 15s`
3. **Any → failed**: Triggered when `taskId` not found in `taskCreationTimes` Map (page refresh scenario)

**Progress Calculation**:
```javascript
// generating phase (5-15s elapsed)
progress = Math.min(90, Math.floor((elapsed - 5) * 9))

// Examples:
// 5.0s → progress = 0%
// 7.5s → progress = 22% (floor((7.5 - 5) * 9) = floor(22.5))
// 10.0s → progress = 45%
// 14.9s → progress = 89%
// 15.0s+ → progress = 100% (status becomes 'completed')
```

---

### Historical Mock Tasks (pre-populated)

**States**: Only `completed` or `failed` (never `queued` or `generating`)

**Rationale**: Historical tasks represent past actions, so they always have final states. This simplifies initial display and avoids simulating progression for old tasks.

---

## Data Flow

### Task Creation Flow

```
1. User clicks "Generate PPT" on paper
         │
         ▼
2. PaperModal.vue calls tasksStore.createTask(paperId, paperTitle)
         │
         ▼
3. tasksStore calls createPPTTask(paperId, isArxiv)
         │
         ▼
4. taskService.js routes to mockCreatePPTTask (if VITE_USE_MOCK_DATA=true)
         │
         ▼
5. mockCreatePPTTask:
   - Generates taskId = `mock-task-${timestamp}-${random}`
   - Stores { createdAt: Date.now(), paperId, isArxiv } in taskCreationTimes Map
   - Returns { taskId }
         │
         ▼
6. tasksStore creates task object:
   {
     id: taskId,
     paperId,
     paperTitle,
     status: 'queued',    // Initial status
     createdAt: new Date().toISOString(),
     progress: null,
     downloadUrl: null,
     errorMessage: null
   }
         │
         ▼
7. tasksStore saves to localStorage via useTaskHistory composable
         │
         ▼
8. tasksStore starts polling (if not already active)
```

### Status Polling Flow

```
1. tasksStore polling interval (5s) triggers for all active tasks
         │
         ▼
2. For each task with status 'queued' or 'generating':
   tasksStore calls pollTaskStatus(taskId)
         │
         ▼
3. taskService.js routes to mockPollTaskStatus (if VITE_USE_MOCK_DATA=true)
         │
         ▼
4. mockPollTaskStatus:
   - Looks up taskId in taskCreationTimes Map
   - If found:
       Calculate elapsed = (Date.now() - createdAt) / 1000
       Return status/progress based on elapsed time
   - If not found:
       Return { status: 'failed', errorMessage: '任务不存在或已过期' }
         │
         ▼
5. tasksStore.updateTaskStatus(taskId, statusData):
   - Updates task.status, task.progress, task.downloadUrl
   - If status changed to 'completed': sets completedAt timestamp
   - Saves updated tasks array to localStorage
         │
         ▼
6. TaskItem.vue reactively renders new status/progress
         │
         ▼
7. If task.status === 'completed' or 'failed':
   tasksStore removes task from activeTasks
         │
         ▼
8. If activeTasks.length === 0:
   tasksStore.stopPolling()
```

### Initial Load Flow (Historical Tasks)

```
1. App starts, tasks.js store initializes
         │
         ▼
2. tasksStore loads tasks from localStorage via loadTasksFromLocalStorage()
         │
         ▼
3. If localStorage is empty AND VITE_USE_MOCK_DATA=true:
   Import mockHistoricalTasks from '@/mocks/taskData'
   Set tasks.value = [...mockHistoricalTasks]
   Save to localStorage
         │
         ▼
4. TaskHistory.vue renders tasks array
         │
         ▼
5. User sees 3 pre-populated tasks (2 completed + 1 failed)
```

---

## Validation & Constraints

### Mock Task ID Format

**Pattern**: `mock-task-{timestamp}-{random}`
- `timestamp`: Unix timestamp in milliseconds (13 digits)
- `random`: 6-character alphanumeric string (lowercase)
- **Example**: `mock-task-1705300123456-a3f8e9`

**Regex**: `/^mock-task-\d{13}-[a-z0-9]{6}$/`

**Generation**:
```javascript
// src/mocks/utils.js
export const generateMockTaskId = () => {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 8)
  return `mock-task-${timestamp}-${random}`
}
```

### Historical Task ID Format

**Pattern**: `mock-task-{nnn}`
- `nnn`: Zero-padded 3-digit sequential number (001, 002, 003)
- **Example**: `mock-task-001`

**Regex**: `/^mock-task-\d{3}$/`

---

## Summary

| Entity | Purpose | Storage | Lifecycle |
|--------|---------|---------|-----------|
| MockHistoricalTask | Pre-populated demo tasks | `taskData.js` static export | Permanent (code-defined) |
| TaskCreationRecord | Runtime task tracking | In-memory Map | Cleared on page refresh |
| MockTaskTiming | Status progression config | Constant object | Permanent (code-defined) |

**Key Design Principles**:
1. **Separation**: Historical tasks (static) vs dynamically created tasks (Map-tracked)
2. **Calculated State**: Status derived from elapsed time, not stored state
3. **Graceful Degradation**: Page refresh clears Map → tasks fail with clear error message
4. **ID Prefix**: `mock-task-` distinguishes from real UUIDs, enables coexistence in localStorage
