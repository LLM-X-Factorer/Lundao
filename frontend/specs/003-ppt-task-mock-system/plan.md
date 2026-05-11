# Implementation Plan: PPT Task Mock System

**Branch**: `003-ppt-task-mock` | **Date**: 2025-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ppt-task-mock-system/spec.md`

## Summary

This feature implements a complete mock data system for PPT task generation and history, enabling frontend development independent of backend API availability. The system simulates realistic task lifecycle (creation → queued → generating → completed) with automatic status progression, provides pre-populated historical tasks, and supports seamless environment-based switching between mock and real API modes. This extends the existing mock architecture pattern (established by `paperData.js`) to cover the previously unmocked PPT generation workflow, achieving parity with paper discovery features and enabling complete product demonstrations without backend dependency.

**Primary Requirement**: Frontend developers must be able to create, observe status progression, and view history of PPT generation tasks in mock mode without API errors.

**Technical Approach**: Create `src/mocks/taskData.js` for historical tasks, `src/mocks/taskService.js` for mock API functions (task creation + status polling), modify `src/api/taskService.js` to route calls based on `VITE_USE_MOCK_DATA` environment variable, and enhance `src/stores/tasks.js` to load historical mock tasks on initialization. Status progression is simulated using in-memory timestamp tracking with time-based state calculation (queued 0-5s, generating 5-15s, completed 15s+).

## Technical Context

**Language/Version**: JavaScript/ES6+ (Vue 3 Composition API)
**Primary Dependencies**: Vue 3.5, Vite 5.0, Tailwind CSS 3.4, Headless UI 1.7, Pinia 2.3, Axios 1.12
**Storage**: Browser localStorage (no server-side persistence for MVP), in-memory Map for task creation timestamps
**Testing**: Manual testing (required for status progression timing), Vitest + Vue Test Utils (optional)
**Target Platform**: Modern web browsers (Chrome 55+, Firefox 52+, Safari 11+, Edge 79+), Desktop-first responsive
**Project Type**: Single-page web application (SPA)
**Performance Goals**: <1.5s First Contentful Paint, <100ms interaction response time, <500ms mock API simulation delay
**Constraints**: No authentication required, 5s task polling interval (matches real API), works on 3G networks, mock task IDs must not conflict with real task IDs
**Scale/Scope**: Mock system supports 3 historical tasks + unlimited user-created tasks (localStorage quota ~5MB allows ~50 tasks), status progression tracked for max 100 concurrent tasks (reasonable developer usage)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with `.specify/memory/constitution.md`:

- [x] **Tool-First Philosophy**: ✅ Mock system serves core workflow (PPT generation testing) without adding retention burden. No registration/login/gamification. Enables developer productivity without user-facing changes.

- [x] **Single-Page Minimalism**: ✅ Mock system operates entirely within existing single-page architecture. No new routes or navigation added. TaskHistory and PaperModal components remain unchanged (data-driven rendering).

- [x] **Zero Friction**: ✅ Mock mode requires zero authentication, operates anonymously. State persisted via localStorage. Environment variable switching is developer-facing, not user-facing.

- [x] **Value-First Design**: ✅ Mock data prioritizes demonstrating AI insights and task progression states. Historical tasks showcase completed PPTs with download actions, aligned with value delivery.

- [x] **Aesthetics as Trust**: ✅ No visual changes required. Mock system operates behind existing UI components. Design system compliance maintained through data structure consistency (status, progress, timestamps match real API contract).

- [x] **Technology Stack**: ✅ Uses Vue 3 + Vite + Tailwind + Headless UI + Pinia + Axios. Mock layer integrates with existing Axios API service pattern. No new framework dependencies.

- [x] **Performance**: ✅ Mock services add minimal overhead (<500ms simulated delay). Meets <100ms interaction response (task creation) and <1.5s FCP (no additional assets loaded).

- [x] **Project Structure**: ✅ Follows defined src/ architecture: `src/mocks/` for mock data/services (mirrors existing `paperData.js` pattern), `src/api/` for service layer routing, `src/stores/` for state management.

**Constitution Compliance**: ✅ **PASSED** - No violations. Mock system enhances developer experience without affecting user-facing principles. Architectural pattern consistent with existing mock implementation.

## Project Structure

### Documentation (this feature)

```
specs/003-ppt-task-mock-system/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output - Technical decisions and mock patterns
├── data-model.md        # Phase 1 output - Mock entities and state transitions
├── quickstart.md        # Phase 1 output - Developer setup and testing guide
├── contracts/           # Phase 1 output - Mock API contracts
│   ├── mock-create-task.md       # mockCreatePPTTask contract
│   └── mock-poll-status.md       # mockPollTaskStatus contract
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/
├── api/                # Axios request encapsulation
│   ├── index.js        # Centralized API client config (unchanged)
│   └── taskService.js  # ✨ MODIFIED: Add mock routing logic
├── mocks/              # Mock data and services
│   ├── paperData.js    # Existing paper mock (reference pattern)
│   ├── taskData.js     # ✨ NEW: Historical task mock data
│   ├── taskService.js  # ✨ NEW: Mock task creation and polling functions
│   └── utils.js        # ✨ NEW: Mock helper utilities (ID generation, delays)
├── stores/             # Pinia state management
│   └── tasks.js        # ✨ MODIFIED: Load historical tasks on init
├── components/         # UI components (unchanged - data-driven rendering)
│   ├── common/         # Button, Modal, Toast (unchanged)
│   └── core/           # PaperModal, TaskHistory, TaskItem (unchanged)
├── composables/        # Composition API logic reuse
│   └── useTaskHistory.js  # Existing localStorage logic (unchanged)
├── views/
│   └── HomeView.vue    # Main view (unchanged)
├── App.vue             # Root component (unchanged)
└── main.js             # ✨ MODIFIED: Add mock mode console warning

.env.development        # ✨ MODIFIED: Set VITE_USE_MOCK_DATA=true
.env.production         # ✨ VERIFIED: Ensure VITE_USE_MOCK_DATA=false

tests/ (optional)
└── mocks/              # Mock-specific tests
    └── taskService.spec.js  # Test status progression logic
```

**Structure Decision**: Extends existing `src/mocks/` pattern established by `paperData.js` for architectural consistency. Mock services mirror real API service structure (`src/api/taskService.js`) to enable clean environment-based routing. No changes to UI components required because they consume data reactively from Pinia store. Modified files limited to: `taskService.js` (routing), `tasks.js` store (initialization), `main.js` (warning), and new files in `src/mocks/` directory.

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No constitutional violations | N/A |

**Note**: Mock system introduction is an additive enhancement (developer tooling) that does not modify user-facing behavior or principles. Zero complexity debt incurred.

---

## Phase 0: Outline & Research

### Research Tasks

**RT-001: Mock Data Architecture Pattern**
- **Question**: How should mock task data be structured to match real API contract while enabling status progression simulation?
- **Investigation**: Analyze existing `paperData.js` mock structure, review real API response format from backend contracts, identify minimal data required for task lifecycle simulation.
- **Output**: Document mock data schema in `research.md` with justification for chosen structure.

**RT-002: Time-Based Status Progression Strategy**
- **Question**: What's the best approach to simulate asynchronous task status transitions (queued → generating → completed) in a synchronous mock environment?
- **Investigation**: Evaluate options: (A) setInterval in mock service, (B) in-memory timestamp tracking + calculated state, (C) localStorage-based state persistence. Consider page refresh scenarios, memory leaks, and developer testing experience.
- **Output**: Document chosen strategy with trade-offs analysis in `research.md`.

**RT-003: Mock/Real API Routing Pattern**
- **Question**: How should `taskService.js` conditionally route to mock vs real API to minimize code duplication and maintain clean separation?
- **Investigation**: Review existing `papers.js` store mock implementation, evaluate patterns: (A) inline if-else in service functions, (B) factory pattern with environment-based service selection, (C) wrapper functions with conditional imports.
- **Output**: Document routing pattern with code examples in `research.md`.

**RT-004: LocalStorage Migration Strategy**
- **Question**: How should the system handle localStorage data when switching between mock and real modes (e.g., mock task IDs vs real task IDs coexisting)?
- **Investigation**: Analyze task ID format requirements, evaluate coexistence vs migration strategies, assess risks of data corruption or loss.
- **Output**: Document migration strategy (or no-migration rationale) in `research.md`.

**RT-005: Mock Download Link Handling**
- **Question**: How should mock mode handle download button clicks (no real PPTX file exists)?
- **Investigation**: Evaluate UX options: (A) display toast message, (B) download empty/sample PPTX file, (C) open placeholder page. Consider user confusion vs developer convenience trade-offs.
- **Output**: Document chosen approach with UX rationale in `research.md`.

### Research Deliverable

**Output**: `specs/003-ppt-task-mock-system/research.md` containing:
1. Mock data schema design with field-by-field justification
2. Status progression algorithm description with timing diagrams
3. API routing pattern code examples and integration points
4. LocalStorage coexistence strategy
5. Download handling UX decision and implementation notes

---

## Phase 1: Design & Contracts

*Prerequisites: `research.md` complete*

### Data Model

**Output**: `specs/003-ppt-task-mock-system/data-model.md`

Entities to document:

1. **MockHistoricalTask**
   - Fields: id, paperId, paperTitle, status, createdAt, completedAt, downloadUrl, progress, errorMessage, retryCount
   - Validation rules: id must start with "mock-task-", status enum (queued|generating|completed|failed), progress 0-100 or null
   - Relationships: references paperData.js papers (daily-0001, daily-0002, weekly-0005)

2. **TaskCreationRecord** (in-memory Map)
   - Fields: taskId, createdAt (timestamp), paperId, isArxiv
   - Purpose: tracks task creation time to calculate elapsed time for status progression
   - Lifecycle: cleared on page refresh, no persistence

3. **MockTaskTiming** (configuration object)
   - Fields: QUEUE_DURATION (5s), GENERATE_DURATION (10s), TOTAL_DURATION (15s)
   - Purpose: defines status transition thresholds
   - Rationale: matches real backend processing times for realistic simulation

### API Contracts

**Output**: `specs/003-ppt-task-mock-system/contracts/`

**Contract 1**: `mock-create-task.md`
```
Function: mockCreatePPTTask(paperId, isArxiv)
Input:
  - paperId: string (arxivId or fileId)
  - isArxiv: boolean (default true)
Output:
  - { taskId: string } // Format: "mock-task-{timestamp}-{random}"
Behavior:
  - Generates unique task ID
  - Records creation timestamp in taskCreationTimes Map
  - Simulates 500ms network delay
  - Returns task ID synchronously (wrapped in Promise)
Errors:
  - None (mock always succeeds unless intentional error simulation)
```

**Contract 2**: `mock-poll-status.md`
```
Function: mockPollTaskStatus(taskId)
Input:
  - taskId: string
Output:
  - { status: string, progress: number|null, downloadUrl: string|null, errorMessage: string|null }
Behavior:
  - Lookup taskId in taskCreationTimes Map
  - Calculate elapsed time since creation
  - Return status based on elapsed time:
    * 0-5s: { status: 'queued', progress: null }
    * 5-15s: { status: 'generating', progress: 0-90 (linear) }
    * 15s+: { status: 'completed', progress: 100, downloadUrl: '/mock/downloads/{taskId}.pptx' }
  - Simulates 300ms network delay
  - If taskId not found in Map: { status: 'failed', errorMessage: '任务不存在或已过期' }
Errors:
  - None (mock always succeeds, uses 'failed' status for missing tasks)
```

### Quickstart Guide

**Output**: `specs/003-ppt-task-mock-system/quickstart.md`

Content outline:
1. **Prerequisites**: Node.js 18+, project dependencies installed
2. **Enable Mock Mode**: Set `VITE_USE_MOCK_DATA=true` in `.env.development`
3. **Verify Setup**: Start dev server, check console for "🚧 Mock Mode Enabled 🚧" warning
4. **Test Task Creation**: Click "Generate PPT" on any paper, verify toast and TaskHistory update
5. **Observe Status Progression**: Wait 15 seconds, watch task transition queued → generating → completed
6. **Test Historical Tasks**: Refresh page, verify 3 pre-populated tasks appear
7. **Switch to Real Mode**: Change env var to `false`, restart server, observe API call errors (expected without backend)
8. **Troubleshooting**: Common issues (localStorage quota, task stuck in queued after refresh)

### Agent Context Update

**Not Applicable**: This command is part of the SpecKit workflow but requires PowerShell which is unavailable. Agent context (CLAUDE.md) will be manually updated after implementation to document the mock system architecture and usage patterns.

---

## Phase 2: Task Breakdown

**Not Generated by `/speckit.plan`**: Task breakdown is created by running `/speckit.tasks` command after Phase 1 completion. The tasks.md file will contain granular implementation steps organized by phases, referencing this plan.md and the generated research.md, data-model.md, and contracts/ for technical specifications.

**Expected Task Categories**:
1. Mock Data & Services (T001-T005): Create taskData.js, taskService.js, utils.js
2. API Layer Integration (T006-T007): Modify taskService.js routing logic
3. Store Initialization (T008-T009): Update tasks.js to load historical tasks
4. Environment Config (T010-T011): Update .env files, add console warnings
5. Testing & Validation (T012-T015): Manual testing checklist, edge case verification

**Next Command**: `/speckit.tasks` to generate detailed task breakdown

---

## Re-evaluation: Constitution Check (Post-Design)

*Re-check after Phase 1 design artifacts generated*

- [x] **Tool-First Philosophy**: ✅ Design maintains tool-focused approach. Mock system enables developer workflow testing without user-facing changes.

- [x] **Single-Page Minimalism**: ✅ Design confirmed: zero new routes, all functionality within existing components via data props.

- [x] **Zero Friction**: ✅ Design verified: mock mode operates without authentication, localStorage-based persistence matches existing pattern.

- [x] **Value-First Design**: ✅ Mock data structure prioritizes completed tasks with download URLs, failed tasks with retry options, aligning with value demonstration.

- [x] **Aesthetics as Trust**: ✅ Design confirmed: no UI changes, existing components consume mock data seamlessly. Design system compliance automatic.

- [x] **Technology Stack**: ✅ Design uses only approved stack: Vue 3, Pinia, Axios. Mock layer follows existing architectural patterns.

- [x] **Performance**: ✅ Design analysis: mock API adds <500ms delay, in-memory Map overhead negligible (<1KB for 100 tasks), meets performance targets.

- [x] **Project Structure**: ✅ Design adheres to src/ structure: mocks/ for mock layer, api/ for service routing, stores/ for state initialization.

**Final Compliance**: ✅ **PASSED** - Post-design review confirms zero constitutional violations. Implementation ready to proceed.

---

## Implementation Readiness

**Status**: ✅ Ready for task generation (`/speckit.tasks`)

**Deliverables Generated**:
- [x] plan.md (this file)
- [ ] research.md (Phase 0 - to be generated)
- [ ] data-model.md (Phase 1 - to be generated)
- [ ] contracts/ (Phase 1 - to be generated)
- [ ] quickstart.md (Phase 1 - to be generated)

**Next Steps**:
1. **Phase 0**: Research and document technical decisions (mock patterns, status progression, routing strategy)
2. **Phase 1**: Generate data model, API contracts, and quickstart guide
3. **Phase 2**: Run `/speckit.tasks` to create detailed implementation tasks
4. **Implementation**: Execute tasks following SpecKit methodology
5. **Validation**: Test against Success Criteria from spec.md

**Branch**: `003-ppt-task-mock`
**Implementation Target**: All tasks completable in 3-4 hours (including testing)
