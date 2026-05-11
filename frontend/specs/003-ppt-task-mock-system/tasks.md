# Tasks: PPT Task Mock System

**Input**: Design documents from `/specs/003-ppt-task-mock-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md
**Branch**: `003-ppt-task-mock`
**Tests**: Manual testing only (no automated test tasks - validated via quickstart.md test scenarios)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `.env` files at repository root
- Paths shown below follow project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create mock system foundation files and utilities

**Timeline**: 30-45 minutes

- [X] **T001** [P] Create `src/mocks/utils.js` with mock helper utilities
  - **Description**: Implement `generateMockTaskId()` function (format: `mock-task-{timestamp}-{random6chars}`)
  - **Description**: Implement `delay(ms)` function for simulating network latency
  - **File**: `src/mocks/utils.js`
  - **Validation**: Export both functions, test in console: `generateMockTaskId()` returns unique IDs

- [X] **T002** [P] Create `src/mocks/taskData.js` with historical mock tasks
  - **Description**: Export `mockHistoricalTasks` array with 3 pre-populated tasks:
    - Task 1: id='mock-task-001', paperId='daily-0001', status='completed', downloadUrl='/mock/downloads/mock-task-001.pptx'
    - Task 2: id='mock-task-002', paperId='daily-0002', status='completed', downloadUrl='/mock/downloads/mock-task-002.pptx'
    - Task 3: id='mock-task-003', paperId='weekly-0005', status='failed', progress=45, errorMessage='PPT生成超时,请重试'
  - **File**: `src/mocks/taskData.js`
  - **Validation**: Import and log `mockHistoricalTasks` in console, verify 3 tasks with correct structure

- [X] **T003** Create `src/mocks/taskService.js` with timing configuration
  - **Description**: Export `MOCK_TASK_TIMING` constant object: `{ QUEUE_DURATION: 5, GENERATE_DURATION: 10, TOTAL_DURATION: 15 }`
  - **Description**: Create module-scoped `taskCreationTimes` Map for tracking task creation timestamps
  - **File**: `src/mocks/taskService.js`
  - **Validation**: Import config in console, verify timing values are correct
  - **Dependencies**: None (foundational setup)

**Checkpoint**: Mock data foundation ready - all 3 base files created and validated

---

## Phase 2: User Story 1 - Mock Mode Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable PPT task creation in mock mode without API errors

**Independent Test**: Click "Generate PPT" in mock mode → Task appears in TaskHistory with queued status, no console errors

**Timeline**: 45-60 minutes

### Implementation for User Story 1

- [X]** [US1] Implement `mockCreatePPTTask` function in `src/mocks/taskService.js`
  - **Description**: Function signature: `async mockCreatePPTTask(paperId, isArxiv = true)`
  - **Description**: Generate taskId via `generateMockTaskId()` from utils
  - **Description**: Record `{ createdAt: Date.now(), paperId, isArxiv }` in `taskCreationTimes` Map
  - **Description**: Simulate 500ms network delay using `delay(500)`
  - **Description**: Return `{ taskId }`
  - **Description**: Add console.log: `[Mock] PPT task created: ${taskId}`
  - **File**: `src/mocks/taskService.js`
  - **Reference**: Contract: `contracts/mock-create-task.md`
  - **Dependencies**: T001 (utils), T003 (taskService base)

- [X]** [US1] Add mock routing logic to `src/api/taskService.js`
  - **Description**: Import `mockCreatePPTTask` from `@/mocks/taskService`
  - **Description**: Add `const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'` at top
  - **Description**: Modify `createPPTTask` function: Add `if (USE_MOCK_DATA) return mockCreatePPTTask(paperId, isArxiv)` before real API call
  - **Description**: Existing real API logic remains unchanged (after if block)
  - **File**: `src/api/taskService.js` (lines 1-15 approx)
  - **Reference**: Research: RT-003 (API routing pattern)
  - **Dependencies**: T004 (mockCreatePPTTask exists)

- [X]** [US1] Update `.env.development` to enable mock mode
  - **Description**: Set `VITE_USE_MOCK_DATA=true`
  - **Description**: Add comment: `# Enable mock data for PPT tasks and paper analysis`
  - **File**: `.env.development`
  - **Dependencies**: None (can be done anytime)

- [X]** [US1] Verify `.env.production` has mock mode disabled
  - **Description**: Ensure `VITE_USE_MOCK_DATA=false` (or omitted, defaults to false)
  - **Description**: Add comment: `# IMPORTANT: Never enable mock mode in production`
  - **File**: `.env.production`
  - **Dependencies**: None (can be done anytime)

- [X]** [US1] Add mock mode console warning in `src/main.js`
  - **Description**: After app mount, add:
    ```javascript
    if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
      console.warn('%c🚧 Mock Mode Enabled 🚧', 'color: orange; font-size: 20px; font-weight: bold')
      console.warn('PPT任务和分析数据使用mock,非真实后端数据')
    }
    ```
  - **File**: `src/main.js` (after `app.mount('#app')`)
  - **Dependencies**: None (independent enhancement)

**Checkpoint US1**: Task creation in mock mode works - Test via quickstart.md Test 2

---

## Phase 3: User Story 2 - Automatic Task Status Progression (Priority: P1)

**Goal**: Simulate realistic task status transitions (queued → generating → completed)

**Independent Test**: Create task → Wait 15s → Observe status progression without manual intervention

**Timeline**: 30-45 minutes

### Implementation for User Story 2

- [X]** [US2] Implement `mockPollTaskStatus` function in `src/mocks/taskService.js`
  - **Description**: Function signature: `async mockPollTaskStatus(taskId)`
  - **Description**: Simulate 300ms network delay using `delay(300)`
  - **Description**: Lookup taskId in `taskCreationTimes` Map
  - **Description**: If not found: return `{ status: 'failed', progress: 0, downloadUrl: null, errorMessage: '任务不存在或已过期' }`
  - **Description**: Calculate `elapsedSeconds = (Date.now() - task.createdAt) / 1000`
  - **Description**: Determine status based on elapsed time:
    - `< 5s`: return `{ status: 'queued', progress: null, downloadUrl: null, errorMessage: null }`
    - `5-15s`: return `{ status: 'generating', progress: Math.min(90, Math.floor((elapsedSeconds - 5) * 9)), downloadUrl: null, errorMessage: null }`
    - `>= 15s`: return `{ status: 'completed', progress: 100, downloadUrl: `/mock/downloads/${taskId}.pptx`, errorMessage: null }`
  - **File**: `src/mocks/taskService.js`
  - **Reference**: Contract: `contracts/mock-poll-status.md`, Research: RT-002
  - **Dependencies**: T003 (taskCreationTimes Map), T001 (delay util)

- [X]** [US2] Add mock routing logic for polling to `src/api/taskService.js`
  - **Description**: Import `mockPollTaskStatus` from `@/mocks/taskService`
  - **Description**: Modify `pollTaskStatus` function: Add `if (USE_MOCK_DATA) return mockPollTaskStatus(taskId)` before real API call
  - **Description**: Existing real API logic remains unchanged (after if block)
  - **File**: `src/api/taskService.js` (lines 20-30 approx)
  - **Dependencies**: T009 (mockPollTaskStatus exists)

**Checkpoint US2**: Status progression works - Test via quickstart.md Test 3

---

## Phase 4: User Story 3 - Historical Task Display (Priority: P2)

**Goal**: Show pre-populated task history on first app launch in mock mode

**Independent Test**: Clear localStorage → Refresh page in mock mode → See 3 historical tasks

**Timeline**: 30-40 minutes

### Implementation for User Story 3

- [X]** [US3] Update `src/stores/tasks.js` store initialization
  - **Description**: Import `mockHistoricalTasks` from `@/mocks/taskData`
  - **Description**: Add `const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'` at top
  - **Description**: After `const storedTasks = loadTasksFromLocalStorage()` line, add:
    ```javascript
    if (USE_MOCK_DATA && storedTasks.length === 0) {
      // First time in mock mode: load historical tasks
      tasks.value = [...mockHistoricalTasks]
      saveTasksToLocalStorage(tasks.value)
    } else {
      tasks.value = storedTasks
    }
    ```
  - **File**: `src/stores/tasks.js` (lines 15-25 approx, initialization section)
  - **Reference**: Research: RT-001 (mock data architecture)
  - **Dependencies**: T002 (mockHistoricalTasks exists)

- [X]** [US3] Add page refresh handling for orphaned tasks
  - **Description**: In same initialization block (after loading tasks), add logic to mark orphaned tasks as failed:
    ```javascript
    if (USE_MOCK_DATA) {
      tasks.value = tasks.value.map(task => {
        if (task.id.startsWith('mock-task-') &&
            ['queued', 'generating'].includes(task.status)) {
          return {
            ...task,
            status: 'failed',
            errorMessage: '页面刷新导致任务中断 (Mock模式)'
          }
        }
        return task
      })
      saveTasksToLocalStorage(tasks.value)
    }
    ```
  - **File**: `src/stores/tasks.js` (same initialization section)
  - **Reference**: Data Model: State Transitions section
  - **Dependencies**: T011 (initialization logic exists)

**Checkpoint US3**: Historical tasks appear - Test via quickstart.md Test 1 and Test 5

---

## Phase 5: User Story 4 - Environment-Based Mode Switching (Priority: P2)

**Goal**: Support seamless switching between mock and real API modes via environment variable

**Independent Test**: Toggle VITE_USE_MOCK_DATA → Restart server → Verify mode change (console warning presence/absence)

**Timeline**: 20-30 minutes

### Implementation for User Story 4

- [X]** [P] [US4] Add README documentation for mock mode usage
  - **Description**: Update `src/mocks/README.md` (if exists) or create new section in project README
  - **Description**: Document: How to enable/disable mock mode, what gets mocked (PPT tasks + paper analysis), environment variable settings
  - **Description**: Add warning about production deployment (must have VITE_USE_MOCK_DATA=false)
  - **File**: `src/mocks/README.md` or `README.md`
  - **Dependencies**: None (documentation task, can run anytime)

- [X]** [P] [US4] Update CLAUDE.md with mock system documentation
  - **Description**: Add section under "Mock Data System (Development)" heading
  - **Description**: Document PPT task mock system architecture (taskData.js, taskService.js, utils.js)
  - **Description**: Explain status progression mechanism (in-memory Map + elapsed time calculation)
  - **Description**: Note environment variable control and localStorage coexistence strategy
  - **File**: `CLAUDE.md` (Mock Data System section, ~line 150)
  - **Dependencies**: None (documentation task, can run anytime)

**Checkpoint US4**: Mode switching documented and tested - Test via quickstart.md Test 6

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Download handling, cleanup utilities, final validation

**Timeline**: 30-40 minutes

- [X]** [Polish] Add mock download toast handling to `src/components/core/TaskItem.vue`
  - **Description**: Locate `handleDownload` function (or create if doesn't exist)
  - **Description**: Add check before download:
    ```javascript
    const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'
    if (USE_MOCK_DATA && props.task.downloadUrl?.startsWith('/mock/downloads/')) {
      uiStore.showToast('Mock模式: 实际部署后可下载真实PPT文件', 'info')
      return
    }
    // Real download logic
    window.open(props.task.downloadUrl, '_blank')
    ```
  - **File**: `src/components/core/TaskItem.vue` (handleDownload function)
  - **Reference**: Research: RT-005 (download handling)
  - **Dependencies**: None (component already exists)

- [X]** [P] [Polish] Add optional cleanup utility function to `src/mocks/taskService.js`
  - **Description**: Export `cleanupExpiredTasks()` function:
    ```javascript
    export const cleanupExpiredTasks = () => {
      const now = Date.now()
      const EXPIRY_TIME = 24 * 60 * 60 * 1000 // 24 hours
      for (const [taskId, taskInfo] of taskCreationTimes.entries()) {
        if (now - taskInfo.createdAt > EXPIRY_TIME) {
          taskCreationTimes.delete(taskId)
        }
      }
    }
    ```
  - **Description**: This function is optional - can be called manually or on unmount
  - **File**: `src/mocks/taskService.js`
  - **Dependencies**: T003 (taskCreationTimes Map exists)

- [X]** Validate all quickstart.md test scenarios
  - **Description**: Run all 6 test scenarios from `quickstart.md`:
    - Test 1: View historical tasks (3 tasks appear)
    - Test 2: Create new task (toast + queued status)
    - Test 3: Observe status progression (queued → generating → completed in 15s)
    - Test 4: Test download button (toast appears, no download)
    - Test 5: Page refresh persistence (completed tasks persist, active tasks fail)
    - Test 6: Switch to real API mode (console warning disappears, API calls fail as expected)
  - **Description**: Document any issues found in task notes
  - **Validation**: All 6 scenarios pass successfully
  - **Reference**: `quickstart.md` Testing the Mock System section
  - **Dependencies**: All previous tasks complete

- [X]** Run final code review and cleanup
  - **Description**: Check all modified files for code quality:
    - `src/mocks/` - Verify exports, comments, console.logs
    - `src/api/taskService.js` - Verify if-else logic is clean
    - `src/stores/tasks.js` - Verify initialization logic
    - `.env` files - Verify settings are correct
  - **Description**: Remove any debug console.logs (except the intended mock mode warning)
  - **Description**: Ensure all files follow project ESLint rules
  - **Validation**: `npm run lint` passes with zero errors
  - **Dependencies**: All implementation tasks complete

**Checkpoint Final**: All tasks complete - Mock system ready for production use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - creates foundation files
- **User Story 1 (Phase 2)**: Depends on T001, T003 from Setup
- **User Story 2 (Phase 3)**: Depends on T001, T003 from Setup, T004 from US1
- **User Story 3 (Phase 4)**: Depends on T002 from Setup (historical tasks)
- **User Story 4 (Phase 5)**: Depends on all previous stories (documents complete system)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (T001-T003) - No dependencies on other stories ✅ Independent
- **User Story 2 (P1)**: Can start after Setup (T001-T003) - Needs US1's mockCreatePPTTask (T004) to exist but doesn't modify it ✅ Mostly independent
- **User Story 3 (P2)**: Can start after Setup (T002) - No dependencies on US1/US2 ✅ Independent
- **User Story 4 (P2)**: Can start after US1-US3 complete - Documents complete system ⚠️ Depends on all stories

### Within Each User Story

**User Story 1 (Task Creation)**:
1. T001 (utils), T003 (taskService base) → T004 (mockCreatePPTTask)
2. T004 complete → T005 (API routing)
3. T006, T007, T008 can run in parallel anytime

**User Story 2 (Status Progression)**:
1. T001 (utils), T003 (taskService base) → T009 (mockPollTaskStatus)
2. T009 complete → T010 (API routing)

**User Story 3 (Historical Tasks)**:
1. T002 (taskData) → T011 (store init)
2. T011 complete → T012 (refresh handling)

**User Story 4 (Mode Switching)**:
1. All US1-US3 complete → T013, T014 can run in parallel (documentation)

**Polish**:
1. T015, T016 can run anytime after component/service files exist
2. T017 depends on all implementation tasks
3. T018 depends on T017

### Parallel Opportunities

**Setup Phase (T001-T003)**:
```bash
# All 3 tasks can run in parallel (different files):
Task T001: src/mocks/utils.js
Task T002: src/mocks/taskData.js
Task T003: src/mocks/taskService.js (just the config part)
```

**After Setup**:
```bash
# US1, US2, US3 can theoretically start in parallel if dependencies are met:
# BUT: US2 needs T004 from US1, so realistic parallel execution:

# Batch 1: US1 foundation + US3 (independent)
Task T004: mockCreatePPTTask (US1)
Task T011: store initialization (US3)

# Batch 2: After T004 completes
Task T005: API routing US1
Task T009: mockPollTaskStatus (US2)
Task T012: refresh handling (US3)

# Batch 3: After batch 2
Task T010: API routing US2
Task T006-T008: Environment files (US1)
```

**Documentation (T013-T014)**:
```bash
# Can run in parallel:
Task T013: README update
Task T014: CLAUDE.md update
```

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together (different files, no dependencies):
Task T001: "Create src/mocks/utils.js with mock helper utilities"
Task T002: "Create src/mocks/taskData.js with historical mock tasks"
Task T003: "Create src/mocks/taskService.js with timing configuration"

# All 3 complete → Setup phase done (30-45 min if parallel)
```

---

## Implementation Strategy

### MVP First (US1 + US2 Only - Core Functionality)

1. **Complete Phase 1: Setup** (T001-T003) - 30-45 min
   - Creates all mock foundation files

2. **Complete Phase 2: User Story 1** (T004-T008) - 45-60 min
   - Enables task creation in mock mode
   - **VALIDATE**: Click "Generate PPT" → Task appears, no errors

3. **Complete Phase 3: User Story 2** (T009-T010) - 30-45 min
   - Enables status progression
   - **VALIDATE**: Task progresses queued → generating → completed in 15s

4. **STOP and VALIDATE MVP**:
   - Test creating multiple tasks
   - Observe all tasks progressing independently
   - Verify no console errors
   - **MVP COMPLETE**: Core mock functionality working

5. **Optional**: Deploy/demo MVP before continuing to US3-US4

### Incremental Delivery (Add US3-US4 After MVP)

6. **Add User Story 3: Historical Tasks** (T011-T012) - 30-40 min
   - Clear localStorage → Refresh → See 3 pre-populated tasks
   - **VALIDATE**: Historical tasks appear on first load

7. **Add User Story 4: Documentation** (T013-T014) - 20-30 min
   - Document mock system for developers
   - **VALIDATE**: README and CLAUDE.md updated

8. **Complete Polish Phase** (T015-T018) - 30-40 min
   - Download handling, cleanup, final validation
   - **VALIDATE**: All quickstart.md tests pass

### Full Feature (All User Stories)

**Total Estimated Time**: 3-4 hours

1. Setup: 30-45 min
2. US1: 45-60 min
3. US2: 30-45 min
4. US3: 30-40 min
5. US4: 20-30 min
6. Polish: 30-40 min

**Checkpoints**:
- After Setup → Foundation ready
- After US1 → Task creation works
- After US2 → Status progression works (MVP ready!)
- After US3 → Historical tasks work
- After US4 → Documentation complete
- After Polish → Production ready

### Parallel Team Strategy

With 2-3 developers after Setup completes:

**Developer A**:
- T004-T005 (US1 mock functions + routing)
- T009-T010 (US2 mock polling + routing)
- T015-T016 (Polish: download + cleanup)

**Developer B**:
- T002 (historical tasks data - needed by US3)
- T011-T012 (US3 store initialization)
- T006-T008 (US1 environment files)

**Developer C**:
- T013-T014 (US4 documentation)
- T017-T018 (Testing + final review)

**Timeline with 3 developers**: 2-2.5 hours (vs 3-4 hours solo)

---

## Notes

- **[P] tasks**: Different files, can run in parallel
- **[Story] labels**: Map tasks to user stories for traceability
- **No automated tests**: Validation via manual testing (quickstart.md scenarios)
- **Mock mode console warning**: Expected behavior, not an error
- **Page refresh**: Orphaned tasks (queued/generating) → failed status (by design)
- **LocalStorage**: Auto-pruning handled by existing useTaskHistory composable
- **Commit strategy**: Commit after each phase checkpoint for safety
- **Validation**: Use quickstart.md test scenarios to validate each story independently

### Critical Success Factors

✅ **T003 must complete first** - All mock functions depend on taskCreationTimes Map
✅ **T004 before T009** - Status polling references creation Map populated by T004
✅ **Environment files (T006-T007)** - Critical for production safety
✅ **T017 validation** - Do not skip - ensures all scenarios work end-to-end

### Common Pitfalls to Avoid

❌ Forgetting to restart dev server after .env changes
❌ Not clearing localStorage when testing historical tasks
❌ Modifying same file (taskService.js) concurrently in T005 and T010
❌ Skipping page refresh test (T017 Test 5) - catches Map clearing bug

---

## Success Criteria Validation

After all tasks complete, verify these outcomes from spec.md:

- **SC-001**: ✅ Developers can create PPT tasks in mock mode with 100% success rate (T004-T005)
- **SC-002**: ✅ Task status progresses queued → completed within 15 seconds (T009-T010)
- **SC-003**: ✅ Progress bar animates 0-100% with 5s polling updates (T009)
- **SC-004**: ✅ Historical tasks persist across page refreshes (T011-T012)
- **SC-005**: ✅ Mode switching completes in <30s via environment variable (T006-T007)
- **SC-006**: ✅ System displays 3 historical tasks on first launch (T002, T011)
- **SC-007**: ✅ Mock system consumes <1MB localStorage (verified via T017)

**All 7 success criteria met = Feature complete!** 🎉
