# Research: PPT Task Mock System

**Feature**: PPT Task Mock System
**Branch**: `003-ppt-task-mock`
**Date**: 2025-01-15
**Purpose**: Document technical decisions and research findings for mock system implementation

---

## RT-001: Mock Data Architecture Pattern

### Question
How should mock task data be structured to match real API contract while enabling status progression simulation?

### Investigation

**Analyzed**:
- Existing `paperData.js` mock structure (static data export)
- Real API response format from backend contracts (`/api/generate_ppt`, `/api/task_status`)
- Requirements for task lifecycle simulation (queued → generating → completed)

**Real API Contract** (from backend spec):
```javascript
// POST /api/generate_ppt response
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000"  // UUID format
}

// GET /api/task_status response
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",              // queued | generating | completed | failed
  "progress": 100,                    // 0-100 or null
  "downloadUrl": "/downloads/task123.pptx",  // null until completed
  "errorMessage": null                // null unless failed
}
```

### Decision

**Mock Data Schema**:
```javascript
// src/mocks/taskData.js
export const mockHistoricalTasks = [
  {
    id: 'mock-task-001',           // PREFIX: 'mock-task-' to distinguish from real UUIDs
    paperId: 'daily-0001',          // References existing paperData.js
    paperTitle: 'Hierarchical Reasoning Models...',
    status: 'completed',
    createdAt: '2025-01-14T10:00:00.000Z',  // ISO 8601 format
    completedAt: '2025-01-14T10:03:00.000Z',
    downloadUrl: '/mock/downloads/mock-task-001.pptx',  // Mock path
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },
  // ... 2 more tasks (1 completed, 1 failed)
]
```

### Rationale

1. **ID Format** (`mock-task-*`): Prefix distinguishes mock tasks from real UUIDs, enabling coexistence in localStorage without collision
2. **Paper References**: Use existing `paperData.js` paper IDs (daily-0001, etc.) for consistency
3. **Timestamps**: ISO 8601 format matches backend convention, enables sorting by creation time
4. **Download URLs**: Use `/mock/downloads/` prefix to identify mock files in download handling logic
5. **Extra Fields** (`paperTitle`, `retryCount`): Enhance UX by including display data directly in task object

### Alternatives Considered

- **Alternative A**: Use real UUID format for mock tasks
  - **Rejected**: Risk of ID collision when switching between mock/real modes, harder to identify mock data in debugging

- **Alternative B**: Store only minimal fields (id, status, progress)
  - **Rejected**: Would require additional paper lookups in components, reducing performance and complicating rendering logic

---

## RT-002: Time-Based Status Progression Strategy

### Question
What's the best approach to simulate asynchronous task status transitions in a synchronous mock environment?

### Investigation

**Evaluated Options**:

**Option A**: setInterval in mock service
```javascript
// Start interval when task created, update status every N seconds
export const mockCreatePPTTask = (paperId) => {
  const taskId = generateId()
  setTimeout(() => updateStatus(taskId, 'generating'), 5000)
  setTimeout(() => updateStatus(taskId, 'completed'), 15000)
  return { taskId }
}
```
**Pros**: Simple, automatic progression
**Cons**: Requires cross-service communication to update store, memory leaks if intervals not cleared, doesn't work across page refreshes

**Option B**: In-memory timestamp tracking + calculated state (CHOSEN)
```javascript
// Track creation time, calculate status on each poll
const taskCreationTimes = new Map()  // taskId → { createdAt, paperId }

export const mockPollTaskStatus = (taskId) => {
  const task = taskCreationTimes.get(taskId)
  const elapsedSeconds = (Date.now() - task.createdAt) / 1000

  if (elapsedSeconds < 5) return { status: 'queued', progress: null }
  if (elapsedSeconds < 15) return { status: 'generating', progress: Math.floor((elapsedSeconds - 5) * 9) }
  return { status: 'completed', progress: 100, downloadUrl: `/mock/downloads/${taskId}.pptx` }
}
```
**Pros**: Stateless (status derived from time), no timers to manage, works with existing 5s polling, simple to debug
**Cons**: Loses state on page refresh (acceptable - tasks marked failed on reload)

**Option C**: localStorage-based state persistence
```javascript
// Store task creation time + current status in localStorage
localStorage.setItem(`mock-task-${taskId}`, JSON.stringify({ createdAt, status: 'queued' }))
```
**Pros**: Survives page refresh
**Cons**: Extra localStorage writes, complicates quota management, violates separation of concerns (mock service shouldn't manage store persistence)

### Decision

**Strategy**: **Option B** - In-memory timestamp tracking with calculated state

**Implementation**:
1. Create `taskCreationTimes` Map in `src/mocks/taskService.js`
2. `mockCreatePPTTask` records `{ taskId → { createdAt, paperId, isArxiv } }` in Map
3. `mockPollTaskStatus` calculates elapsed time and returns appropriate status/progress
4. On page refresh: Map clears → tasks in queued/generating status fail (handled in store initialization)

**Time Thresholds**:
- 0-5s: `queued` (no progress bar)
- 5-15s: `generating` (progress = `Math.min(90, Math.floor((elapsed - 5) * 9))`)
- 15s+: `completed` (progress = 100, downloadUrl provided)

### Rationale

- **Simplicity**: No timers/intervals to manage, minimal memory footprint (<1KB for 100 tasks)
- **Consistency**: Leverages existing 5s polling interval in tasks.js store (no changes needed)
- **Debuggability**: Easy to test (create task, wait N seconds, poll → verify status)
- **Acceptable Trade-off**: Page refresh clearing Map is acceptable because tasks.js store already handles orphaned tasks

### Timing Diagram

```
Time (s):    0        5               15
             │        │                │
Status:   queued  generating      completed
Progress:   null    0% → 90%          100%
Action:     [--]   [==========>]    [Download]

Polling:     ↓        ↓                ↓
(5s interval)  poll1   poll2   poll3   poll4
```

---

## RT-003: Mock/Real API Routing Pattern

### Question
How should `taskService.js` conditionally route to mock vs real API to minimize code duplication and maintain clean separation?

### Investigation

**Existing Pattern** (from `papers.js` store):
```javascript
// src/stores/papers.js
import { fetchArxivPapers } from '@/api/paperService'
import { dailyPapers, weeklyPapers } from '@/mocks/paperData'

const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

const fetchMockPapers = (period, page) => {
  // Mock logic here
}

const fetchPapers = async (period, page) => {
  let response
  if (USE_MOCK_DATA) {
    response = await fetchMockPapers(period, page)
  } else {
    response = await fetchArxivPapers(period, page, 20)
  }
  papers.value = response.papers
}
```

**Evaluated Patterns**:

**Option A**: Inline if-else in service functions (CHOSEN)
```javascript
// src/api/taskService.js
import apiClient from './index'
import { mockCreatePPTTask, mockPollTaskStatus } from '@/mocks/taskService'

const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const createPPTTask = async (paperId, isArxiv = true) => {
  if (USE_MOCK_DATA) {
    return mockCreatePPTTask(paperId, isArxiv)
  }

  const requestBody = isArxiv ? { arxivId: paperId } : { fileId: paperId }
  const response = await apiClient.post('/generate_ppt', requestBody, { timeout: 30000 })
  return response.data
}
```

**Option B**: Factory pattern with environment-based service selection
```javascript
// src/api/taskServiceFactory.js
const createTaskService = () => {
  if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
    return import('@/mocks/taskService')
  }
  return import('./taskServiceReal')
}

export default createTaskService()
```
**Pros**: Clean separation, no conditionals in service code
**Cons**: Adds complexity, dynamic imports may confuse bundler, doesn't match existing pattern in codebase

**Option C**: Wrapper functions with conditional imports
```javascript
// Wrapper layer that imports based on env
```
**Pros**: Type safety if using TypeScript
**Cons**: Over-engineering for JavaScript codebase, inconsistent with existing patterns

### Decision

**Pattern**: **Option A** - Inline if-else in service functions

**Implementation**:
```javascript
// src/api/taskService.js
import apiClient from './index'
import { mockCreatePPTTask, mockPollTaskStatus } from '@/mocks/taskService'

const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const createPPTTask = async (paperId, isArxiv = true) => {
  if (USE_MOCK_DATA) {
    return mockCreatePPTTask(paperId, isArxiv)
  }
  // ... real API logic (unchanged)
}

export const pollTaskStatus = async (taskId) => {
  if (USE_MOCK_DATA) {
    return mockPollTaskStatus(taskId)
  }
  // ... real API logic (unchanged)
}
```

### Rationale

1. **Consistency**: Matches existing pattern in `papers.js` store (established precedent)
2. **Simplicity**: Single file for both mock and real logic, easy to understand
3. **No Dynamic Imports**: Build-time resolution, no runtime overhead
4. **Minimal Changes**: Only 2-3 lines added per function (minimal diff, easier code review)
5. **Discoverability**: Developers can see both code paths in same file

### Integration Points

- `src/api/taskService.js`: Add conditional routing (2 functions modified)
- `src/mocks/taskService.js`: Create mock implementations (new file)
- Environment variable: `VITE_USE_MOCK_DATA` (already exists in project)

---

## RT-004: LocalStorage Migration Strategy

### Question
How should the system handle localStorage data when switching between mock and real modes?

### Investigation

**ID Format Analysis**:
- Mock tasks: `mock-task-{timestamp}-{random}` (e.g., `mock-task-1705300000-a3f8e9`)
- Real tasks: UUID v4 format (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- **No collision risk**: Formats mutually exclusive (mock prefix vs UUID pattern)

**Coexistence Scenarios**:
1. User creates mock tasks → switches to real mode → creates real tasks
   - localStorage contains mix: `[{id: 'mock-task-...'}, {id: '550e8400-...'}]`
   - Polling mock tasks in real mode: API call with mock ID → 404 error → task marked failed
   - **Acceptable**: Failed tasks show error message, user can delete manually

2. User creates real tasks → switches to mock mode → creates mock tasks
   - localStorage contains mix (same as above)
   - Polling real tasks in mock mode: `mockPollTaskStatus` doesn't find real UUID in Map → returns failed status
   - **Acceptable**: Same graceful degradation

**Migration Alternatives**:

**Option A**: No migration - allow coexistence (CHOSEN)
- Tasks with unrecognized IDs fail gracefully
- User can manually delete failed tasks or clear localStorage
- Simple, no data transformation risk

**Option B**: Clear localStorage on mode switch
- Requires detecting mode change (compare current vs previous env var)
- Risk of data loss if user accidentally switches modes
- **Rejected**: Too aggressive, violates user expectations

**Option C**: Filter tasks by ID format
```javascript
// Only show mock tasks in mock mode, real tasks in real mode
const validTasks = tasks.filter(t =>
  USE_MOCK_DATA ? t.id.startsWith('mock-task-') : !t.id.startsWith('mock-task-')
)
```
- **Rejected**: Hides user's task history, confusing UX

### Decision

**Strategy**: **No migration** - Allow mock and real tasks to coexist in localStorage

**Behavior**:
- Mock mode: All tasks visible, mock tasks poll successfully, real task UUIDs return `{ status: 'failed', errorMessage: '任务不存在或已过期' }`
- Real mode: All tasks visible, real tasks poll successfully, mock task IDs return 404 → marked failed
- User can delete failed tasks manually via TaskHistory UI (existing delete functionality)

### Rationale

1. **Simplicity**: Zero migration code, no data transformation risks
2. **Transparent Failure**: Failed tasks clearly show error messages
3. **Manual Control**: Users can choose to delete or keep failed tasks
4. **Edge Case**: Mode switching is rare (developer workflow, not end-user scenario)
5. **Existing Cleanup**: `useTaskHistory` composable already implements auto-pruning of old completed tasks (max 50 recent)

### Failure Modes

| Scenario | Behavior | User Impact |
|----------|----------|-------------|
| Mock task ID in real mode | API 404 → task marked failed after first poll | Error message shown, task deletable |
| Real task UUID in mock mode | mockPollTaskStatus returns failed status | Error message shown, task deletable |
| Page refresh with mixed tasks | All tasks loaded, polling continues per mode | No impact (each task polled independently) |

---

## RT-005: Mock Download Link Handling

### Question
How should mock mode handle download button clicks when no real PPTX file exists?

### Investigation

**User Context**:
- Mock mode is developer-facing feature, not production scenario
- Primary use case: Testing UI/UX, demonstrating product to stakeholders
- Users understand mock limitations when explicitly enabled via environment variable

**UX Options**:

**Option A**: Display toast message (CHOSEN)
```javascript
// src/components/core/TaskItem.vue (or inline in component)
const handleDownload = () => {
  const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

  if (USE_MOCK_DATA && props.task.downloadUrl?.startsWith('/mock/')) {
    uiStore.showToast('Mock模式: 实际部署后可下载真实PPT文件', 'info')
    return
  }

  // Real download logic
  window.open(props.task.downloadUrl, '_blank')
}
```
**Pros**: Simple, clear feedback, no file generation overhead
**Cons**: Breaks illusion of complete mock (but acceptable for developer tool)

**Option B**: Download empty/sample PPTX file
```javascript
// Generate minimal PPTX using PptxGenJS or similar library
import PptxGenJS from 'pptxgenjs'

const generatePlaceholderPPT = () => {
  const pptx = new PptxGenJS()
  pptx.addSlide().addText('Mock Presentation Placeholder', { x: 1, y: 1 })
  pptx.writeFile({ fileName: `mock-${taskId}.pptx` })
}
```
**Pros**: More realistic simulation, actual file download
**Cons**: Adds 100KB+ library dependency, slower performance, unnecessary complexity for mock mode

**Option C**: Open placeholder page
```javascript
window.open(`/mock-download-info?taskId=${taskId}`, '_blank')
```
**Pros**: Can show detailed mock info/instructions
**Cons**: Requires new route (violates single-page principle), overengineered

### Decision

**Strategy**: **Option A** - Display informational toast message

**Implementation**:
```javascript
// Check if download URL is mock path
if (USE_MOCK_DATA && downloadUrl.startsWith('/mock/downloads/')) {
  showToast('Mock模式: 实际部署后可下载真实PPT文件', 'info')
  return
}

// Otherwise proceed with real download
window.open(downloadUrl, '_blank')
```

### Rationale

1. **Simplicity**: Zero dependencies, 3 lines of code
2. **Clarity**: Toast explicitly states mock limitation
3. **Performance**: No file generation overhead
4. **Acceptable UX**: Developers understand mock mode limitations
5. **Consistency**: Matches existing toast usage pattern in UI

### User Experience Flow

```
1. User clicks "Download PPT" on completed mock task
2. Toast appears: "Mock模式: 实际部署后可下载真实PPT文件" (info style, 3s duration)
3. No file download occurs
4. User acknowledges mock limitation, continues testing other features
```

**Alternative for Demos**: If realistic download is needed for stakeholder demos, developer can temporarily create a sample PPTX file and place it in `public/mock/downloads/` directory, which will be served by Vite dev server. This is optional and not part of default mock implementation.

---

## Summary of Decisions

| Research Task | Decision | Implementation Complexity |
|---------------|----------|--------------------------|
| RT-001: Mock Data Schema | Prefix-based ID format (`mock-task-*`), ISO timestamps, reference existing papers | Low - Static data export |
| RT-002: Status Progression | In-memory timestamp tracking, calculated state on poll | Low - Single Map + math logic |
| RT-003: API Routing | Inline if-else in service functions (matches existing pattern) | Low - 2-3 lines per function |
| RT-004: LocalStorage Migration | No migration, allow coexistence, graceful failure | Zero - No code needed |
| RT-005: Download Handling | Toast message for mock downloads | Low - Conditional check + toast call |

**Total Implementation Complexity**: **Low** - All decisions prioritize simplicity and consistency with existing codebase patterns.

**Risk Assessment**: **Minimal** - No external dependencies, no data migration risks, graceful degradation in edge cases.

**Next Phase**: Proceed to Phase 1 (Data Model, Contracts, Quickstart) with confidence in technical approach.
