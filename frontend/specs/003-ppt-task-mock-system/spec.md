# Feature Specification: PPT Task Mock System

**Feature Branch**: `003-ppt-task-mock`
**Created**: 2025-01-15
**Status**: Draft
**Input**: User description: "PPT任务Mock系统 - 为PPT生成和任务历史功能提供完整的mock数据支持"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mock Mode Task Creation (Priority: P1)

Frontend developers need to create PPT generation tasks in mock mode without backend API dependency, enabling independent frontend development and testing of the PPT generation workflow.

**Why this priority**: This is the foundation of the entire mock system. Without the ability to create tasks in mock mode, developers cannot test any of the subsequent task status flows, making this the highest priority blocking feature.

**Independent Test**: Can be fully tested by clicking "Generate PPT" button in mock mode (VITE_USE_MOCK_DATA=true) and verifying that a task appears in the task history with queued status, without any API errors.

**Acceptance Scenarios**:

1. **Given** user views a paper analysis in the modal AND mock mode is enabled, **When** user clicks "一键生成组会PPT" button, **Then** system displays success toast message "PPT生成任务已创建" AND modal closes AND new task appears in TaskHistory with queued status
2. **Given** task is created successfully, **When** user views the task in TaskHistory, **Then** task displays paper title, creation timestamp, and queued status indicator
3. **Given** user clicks "Generate PPT" for same paper twice, **When** both tasks are created, **Then** system creates two independent tasks with unique task IDs
4. **Given** mock mode is disabled (VITE_USE_MOCK_DATA=false), **When** user clicks "Generate PPT", **Then** system attempts real API call (expected to fail if backend unavailable)

---

### User Story 2 - Automatic Task Status Progression (Priority: P1)

Users need to observe realistic task status progression from queued to generating to completed, with smooth progress bar animation, to understand PPT generation progress and system responsiveness.

**Why this priority**: This is equally critical as task creation because it validates the core polling mechanism and provides essential user feedback. Without status progression, tasks would remain stuck in queued state forever, breaking the user experience.

**Independent Test**: Can be fully tested by creating a task in mock mode and observing automatic status transitions: queued (0-5s) → generating (5-15s, progress 0-90%) → completed (15s+, progress 100% with download link). No user interaction required after task creation.

**Acceptance Scenarios**:

1. **Given** task is newly created (0-5 seconds elapsed), **When** polling occurs, **Then** task status remains queued AND no progress bar is displayed
2. **Given** task has been queued for 5+ seconds, **When** next polling cycle executes, **Then** task status changes to generating AND progress bar appears showing 0%
3. **Given** task is in generating status (5-15 seconds elapsed), **When** polling occurs, **Then** progress bar smoothly increases from 0% to 90% proportional to elapsed time
4. **Given** task has been running for 15+ seconds, **When** next polling cycle executes, **Then** task status changes to completed AND progress shows 100% AND "Download PPT" button appears
5. **Given** multiple tasks exist with different states, **When** polling occurs, **Then** each task progresses independently based on its own creation timestamp

---

### User Story 3 - Historical Task Display (Priority: P2)

Users need to view previously created PPT tasks (both successful and failed) to access past generated presentations and understand failure reasons, enabling them to download previous work or retry failed attempts.

**Why this priority**: While important for usability, this is lower priority than P1 stories because users can still create and complete new tasks without historical data. Historical tasks enhance the experience but aren't blocking for core functionality.

**Independent Test**: Can be fully tested by starting the app in mock mode for the first time (empty localStorage) and verifying that 3 pre-populated historical tasks appear: 2 completed tasks with download buttons and 1 failed task with error message and retry button. Page refresh should preserve these tasks.

**Acceptance Scenarios**:

1. **Given** user launches app in mock mode for first time (empty localStorage), **When** TaskHistory component loads, **Then** system displays 3 pre-populated historical tasks: 2 completed + 1 failed
2. **Given** completed historical task is displayed, **When** user views task item, **Then** task shows paper title, completed timestamp, 100% progress, and "Download PPT" button
3. **Given** failed historical task is displayed, **When** user views task item, **Then** task shows paper title, error message "PPT生成超时,请重试", and "Retry" button with partial progress (45%)
4. **Given** user creates new tasks AND refreshes page, **When** TaskHistory reloads, **Then** all tasks persist (historical + newly created) in reverse chronological order (newest first)
5. **Given** user clicks download button on mock completed task, **When** download is triggered, **Then** system displays info toast "Mock模式: 实际部署后可下载真实PPT文件" instead of downloading file

---

### User Story 4 - Environment-Based Mode Switching (Priority: P2)

Developers need to easily switch between mock and real API modes via environment variable to support both isolated frontend development (mock) and integrated testing (real API) without code modifications.

**Why this priority**: Essential for development workflow but doesn't affect end-user functionality. Lower priority than core mock features because switching can be done less frequently and doesn't block daily development.

**Independent Test**: Can be fully tested by toggling VITE_USE_MOCK_DATA environment variable between true/false, restarting dev server, and verifying behavior changes: true = uses mock data/services, false = calls real API endpoints. Console should show clear warnings in mock mode.

**Acceptance Scenarios**:

1. **Given** environment variable VITE_USE_MOCK_DATA is set to "true", **When** application initializes, **Then** all task operations use mock services (taskService.js mock branch) AND console displays warning "🚧 Mock Mode Enabled 🚧"
2. **Given** environment variable VITE_USE_MOCK_DATA is set to "false", **When** application initializes, **Then** all task operations call real API endpoints AND no mock warning is displayed
3. **Given** developer changes environment variable from true to false, **When** dev server restarts, **Then** system seamlessly switches to real API mode without requiring code changes
4. **Given** production deployment (.env.production), **When** environment file is read, **Then** VITE_USE_MOCK_DATA is explicitly set to "false" to prevent accidental mock mode in production

---

### Edge Cases

- **What happens when user refreshes page while tasks are in queued/generating state?**
  - Mock system loses in-memory creation timestamps, so these tasks should be marked as failed with error message "页面刷新导致任务中断 (Mock模式)" to maintain data consistency

- **How does system handle localStorage quota exceeded?**
  - Existing useTaskHistory composable already implements auto-pruning of oldest completed tasks and displays warning toast, maintaining max 50 recent tasks

- **What happens if user creates many tasks rapidly (>20 tasks)?**
  - All tasks are tracked independently, but localStorage size limits may trigger auto-pruning of oldest completed tasks to stay within 5MB quota

- **How does system distinguish mock tasks from real tasks after mode switch?**
  - Mock tasks use ID prefix "mock-task-{timestamp}-{random}", real tasks use different format from backend, enabling coexistence in localStorage

- **What happens if task polling fails (network error, timeout)?**
  - Existing tasks.js store uses Promise.allSettled() to handle individual polling failures gracefully, continuing to poll other tasks

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide mock historical tasks data containing exactly 3 pre-populated tasks: 2 completed tasks and 1 failed task with realistic paper titles and timestamps
- **FR-002**: System MUST create mock PPT tasks that return unique task IDs in format "mock-task-{timestamp}-{random}" when createPPTTask is called in mock mode
- **FR-003**: System MUST simulate task status progression following timeline: queued (0-5 seconds) → generating (5-15 seconds with 0-90% progress) → completed (15+ seconds with 100% progress and download URL)
- **FR-004**: System MUST track task creation timestamps in memory to calculate elapsed time for status progression simulation
- **FR-005**: System MUST automatically load historical mock tasks into TaskHistory on first app launch when localStorage is empty AND mock mode is enabled
- **FR-006**: System MUST persist all tasks (historical mock + user-created) to localStorage after every task creation or status update
- **FR-007**: System MUST display console warning "🚧 Mock Mode Enabled 🚧" when VITE_USE_MOCK_DATA=true during application initialization (development environment only)
- **FR-008**: System MUST route API calls to mock services (mockCreatePPTTask, mockPollTaskStatus) when VITE_USE_MOCK_DATA=true, or to real API endpoints when false
- **FR-009**: System MUST generate mock download URLs in format "/mock/downloads/{taskId}.pptx" for completed tasks in mock mode
- **FR-010**: System MUST display informational toast "Mock模式: 实际部署后可下载真实PPT文件" when user attempts to download mock task results, instead of triggering actual file download
- **FR-011**: System MUST mark tasks as failed with error message "页面刷新导致任务中断 (Mock模式)" when page refreshes and tasks with queued/generating status are found in localStorage (mock mode only)
- **FR-012**: System MUST maintain existing 5-second polling interval for all tasks (mock and real) to ensure consistent behavior

### Key Entities *(include if feature involves data)*

- **MockHistoricalTask**: Represents pre-populated task history for initial mock experience
  - Attributes: id (mock-task-*), paperId, paperTitle, status (completed/failed), createdAt, completedAt, downloadUrl, progress, errorMessage, retryCount
  - Relationships: References papers from existing paperData.js mock
  - Purpose: Demonstrates various task states (success/failure scenarios) on first app load

- **TaskCreationRecord**: In-memory tracking of when mock tasks were created
  - Attributes: taskId, createdAt (timestamp), paperId, isArxiv
  - Relationships: Maps to tasks in tasks.js store
  - Purpose: Calculates elapsed time to determine current status and progress in mock mode

- **MockTaskTiming**: Configuration for status progression timeline
  - Attributes: QUEUE_DURATION (5 seconds), GENERATE_DURATION (10 seconds), TOTAL_DURATION (15 seconds)
  - Purpose: Defines when status transitions occur and progress percentage calculations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can create PPT tasks in mock mode with 100% success rate (zero API errors when clicking "Generate PPT")
- **SC-002**: Task status automatically progresses from queued to completed within 15 seconds without user intervention, verified by polling mechanism
- **SC-003**: Progress bar smoothly animates from 0% to 100% during generating phase (5-15 seconds), with visible updates at least every 5 seconds (polling interval)
- **SC-004**: Historical tasks persist across page refreshes, with 100% data retention for tasks stored in localStorage (verified by refresh test)
- **SC-005**: Mode switching via environment variable completes in under 30 seconds (time to change .env file + restart dev server), with zero code modifications required
- **SC-006**: System displays 3 historical tasks (2 completed + 1 failed) on first launch in mock mode, providing immediate demonstration of feature capabilities
- **SC-007**: Mock system consumes less than 1MB of localStorage for typical usage (50 tasks or less), ensuring compatibility with browser storage limits

### Assumptions *(document reasonable defaults)*

1. **Network Delay Simulation**: Mock services simulate realistic API latency (500ms for task creation, 300ms for status polling) to replicate production environment timing
2. **Task ID Uniqueness**: Timestamp + random string combination provides sufficient uniqueness for mock task IDs (collision probability < 0.001% for reasonable usage)
3. **Browser Compatibility**: Target browsers support localStorage, ES6 Map/Set, and modern async/await syntax (Chrome 55+, Firefox 52+, Safari 11+, Edge 79+)
4. **Development Environment**: Developers have Node.js 18+ and can restart Vite dev server to apply environment variable changes
5. **Historical Task Content**: Pre-populated mock tasks reference papers from existing paperData.js mock dataset (daily-0001, daily-0002, weekly-0005)
6. **Download Behavior**: Users understand that mock mode download buttons are placeholders and accept info toast as feedback (no actual file generation)
7. **Polling Performance**: 5-second polling interval is acceptable latency for task status updates, matching existing production behavior
8. **Memory Management**: taskCreationTimes Map clears on page refresh, which is acceptable because tasks transition to failed state automatically
9. **LocalStorage Persistence**: Existing useTaskHistory composable correctly implements storage quota management and auto-pruning when limits are exceeded
10. **Production Safety**: Deployment process ensures .env.production has VITE_USE_MOCK_DATA=false to prevent accidental mock mode in production

### Dependencies & Integration Points

- **Existing Mock System**: Extends pattern established by `src/mocks/paperData.js` for consistency
- **API Service Layer**: Integrates with `src/api/taskService.js` by adding conditional mock branches
- **Pinia Store**: Modifies `src/stores/tasks.js` initialization to load historical mock tasks
- **Components**: No modifications required to `TaskHistory.vue` or `TaskItem.vue` (data-driven rendering)
- **Environment Config**: Requires `.env.development` and `.env.production` files with VITE_USE_MOCK_DATA setting

### Constraints

- **Architecture Consistency**: Must follow same mock pattern as paperData.js (export mock data + mock service functions, no inline logic in stores)
- **API Contract Immutability**: Cannot change taskId format, response structure, or polling behavior for backward compatibility
- **Polling Interval**: Must maintain 5-second interval (cannot optimize to faster updates in mock mode)
- **No File Generation**: Mock mode does not generate actual PPTX files, only provides placeholder download URLs
- **Memory Lifecycle**: taskCreationTimes Map is not persisted to localStorage, loses state on page refresh by design

### Out of Scope

- Real PPTX file generation using libraries like PptxGenJS (mock mode only provides download link placeholders)
- Custom status progression timing configuration via environment variables or UI settings
- Advanced task retry logic improvements (uses existing retryTask implementation from tasks.js store)
- Automatic cleanup of tasks older than 24 hours (existing cleanup mechanism in useTaskHistory composable is sufficient)
- Mock mode visual indicators in UI beyond console warning (e.g., persistent badge showing "Mock Mode")
- Detailed analytics or telemetry for mock mode usage tracking
