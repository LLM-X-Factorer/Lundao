# Implementation Tasks: 论导Lite MVP Frontend

**Feature**: 论导Lite MVP Frontend Implementation
**Branch**: 001-mvp-frontend-implementation
**Generated**: 2025-10-14
**Total Tasks**: 78

---

## Task Organization

Tasks are organized into **7 phases**:
1. **Setup**: Project initialization and tooling
2. **Foundational**: Blocking prerequisites (stores, API client, composables)
3. **US1 Implementation**: Discover and Analyze Trending Papers (P1)
4. **US2 Implementation**: Upload and Analyze Custom Papers (P2)
5. **US3 Implementation**: Generate and Track PPT (P1)
6. **US4 Implementation**: Navigate Paginated Paper Lists (P3)
7. **Polish**: Animations, error handling, edge cases

**Execution Strategy**: MVP-first approach
- Implement P1 user stories first (US1, US3)
- Then P2 (US2)
- Finally P3 (US4)
- Polish phase runs concurrently with later phases

**Parallelization**: Tasks marked with `[P]` can be executed in parallel with other `[P]` tasks in the same phase.

---

## Phase 1: Setup (Foundation Layer)

### T001 - Initialize Vite Project with Vue 3 Template
**Story**: Setup
**Files**:
- `package.json`
- `vite.config.js`
- `index.html`
- `src/main.js`

**Description**:
Run `npm create vite@latest . -- --template vue` to scaffold the project. Configure project metadata, ensure Vue 3 is used, and verify HMR works.

**Acceptance**:
- `npm run dev` starts development server on port 5173
- Hot module replacement works when editing `.vue` files
- Browser displays default Vite + Vue welcome screen

**Dependencies**: None (entry point)

---

### T002 - Install Core Dependencies
**Story**: Setup
**Files**:
- `package.json`

**Description**:
Install all required npm packages:
```bash
npm install vue@^3.4.0 pinia@^2.1.0 axios@^1.6.0
npm install -D tailwindcss@^3.4.0 postcss@^8.4.0 autoprefixer@^10.4.0
npm install @headlessui/vue@^1.7.0
npm install -D @vitejs/plugin-vue@^5.0.0
npm install -D eslint@^8.56.0 eslint-plugin-vue@^9.20.0
```

**Acceptance**:
- All dependencies installed without errors
- `package.json` contains correct versions
- No peer dependency warnings

**Dependencies**: T001

---

### T003 - Configure Tailwind CSS with Design System
**Story**: Setup
**Files**:
- `tailwind.config.js`
- `postcss.config.js`
- `src/assets/styles/main.css`

**Description**:
Initialize Tailwind with `npx tailwindcss init -p`. Update `tailwind.config.js` with design system tokens (colors, fonts, spacing, border-radius per constitution). Create `src/assets/styles/main.css` with Tailwind directives and custom base styles. Import in `main.js`.

**Acceptance**:
- Tailwind utility classes work in components
- Design system colors applied correctly (e.g., `bg-primary-bg`, `text-accent`)
- Custom font family (Inter, Noto Sans SC) loads from Google Fonts CDN

**Dependencies**: T002

---

### T004 - Configure ESLint and Project Linting
**Story**: Setup
**Files**:
- `.eslintrc.cjs`
- `package.json` (add lint scripts)

**Description**:
Create `.eslintrc.cjs` with Vue 3 and ESLint recommended rules. Add lint scripts to `package.json`: `"lint": "eslint . --ext .vue,.js --fix --ignore-path .gitignore"`. Disable `vue/multi-word-component-names` and `vue/require-default-prop` per project conventions.

**Acceptance**:
- `npm run lint` executes without errors
- ESLint catches common issues (unused vars, missing keys)
- Auto-fix works for formatting issues

**Dependencies**: T002

---

### T005 - Set Up Project Directory Structure
**Story**: Setup
**Files**:
- `src/api/`
- `src/components/common/`
- `src/components/core/`
- `src/composables/`
- `src/stores/`
- `src/views/`
- `src/assets/fonts/`
- `src/assets/images/`

**Description**:
Create directory structure per plan.md:
```bash
mkdir -p src/api
mkdir -p src/components/common
mkdir -p src/components/core
mkdir -p src/composables
mkdir -p src/stores
mkdir -p src/views
mkdir -p src/assets/fonts
mkdir -p src/assets/images
```

**Acceptance**:
- All directories exist
- Structure matches plan.md specification
- Empty `.gitkeep` files added to track empty dirs

**Dependencies**: T001

---

### T006 - Configure Vite Aliases and Dev Server
**Story**: Setup
**Files**:
- `vite.config.js`

**Description**:
Update `vite.config.js` to add `@` alias for `src/`, configure dev server port (5173), enable auto-open, and set up API proxy for `/api` routes to `http://localhost:3000`.

**Acceptance**:
- Imports using `@/` resolve correctly (e.g., `import Button from '@/components/common/Button.vue'`)
- Dev server opens automatically on `npm run dev`
- API proxy forwards `/api/*` requests to backend

**Dependencies**: T001

---

### T007 - Create Environment Configuration Files
**Story**: Setup
**Files**:
- `.env.development`
- `.env.production`
- `.gitignore`

**Description**:
Create `.env.development` with `VITE_API_BASE_URL=http://localhost:3000/api`. Create `.env.production` with `VITE_API_BASE_URL=https://api.lundao.com/api`. Add `.env.local` to `.gitignore`.

**Acceptance**:
- `import.meta.env.VITE_API_BASE_URL` returns correct URL per environment
- `.env.local` ignored by Git (for local overrides)

**Dependencies**: T001

---

### T008 - Update index.html with Fonts and Metadata
**Story**: Setup
**Files**:
- `index.html`

**Description**:
Update `<html lang="zh-CN">`, add Google Fonts preconnect and stylesheet links for Inter and Noto Sans SC. Set page title to "论导Lite - AI助你三分钟搞定组会PPT". Add viewport meta tag.

**Acceptance**:
- Chinese fonts load correctly from CDN
- Page title displays in browser tab
- Font network requests visible in DevTools

**Dependencies**: T001

---

## Phase 2: Foundational (Blocking Prerequisites)

### T009 - Create Axios API Client Base Configuration
**Story**: Foundational
**Files**:
- `src/api/index.js`

**Description**:
Create `src/api/index.js` with axios instance configured:
- `baseURL`: from `VITE_API_BASE_URL`
- `timeout`: 60000ms (60s)
- Request interceptor for logging/loading state
- Response interceptor for global error handling

**Acceptance**:
- `apiClient.get()` and `apiClient.post()` work
- Errors caught and logged in console
- Timeout triggers after 60s on slow requests

**Dependencies**: T002, T007

---

### T010 [P] - Create Paper Service Module
**Story**: Foundational
**Files**:
- `src/api/paperService.js`

**Description**:
Implement paper-related API functions:
- `fetchArxivPapers(period, page, limit)`: GET /api/arxiv_papers
- `analyzePaper(paperId, isArxiv)`: GET /api/analyze_paper

Map parameters correctly per contracts. Handle query string building for arxivId vs fileId.

**Acceptance**:
- Functions return parsed response data
- Errors propagate to caller
- Axios timeout set to 65s for analyze (longer than backend 60s)

**Dependencies**: T009

---

### T011 [P] - Create Upload Service Module
**Story**: Foundational
**Files**:
- `src/api/uploadService.js`

**Description**:
Implement upload function:
- `uploadPDF(file, onProgress)`: POST /api/upload_pdf
- FormData construction with `file` field
- `onUploadProgress` callback support
- `Content-Type: multipart/form-data` header
- 2-minute timeout (120000ms)

**Acceptance**:
- File uploads successfully
- Progress callback invoked with percentage (0-100)
- Large files (up to 20MB) upload without timeout

**Dependencies**: T009

---

### T012 [P] - Create Task Service Module
**Story**: Foundational
**Files**:
- `src/api/taskService.js`

**Description**:
Implement task-related API functions:
- `createPPTTask(paperId, isArxiv)`: POST /api/generate_ppt
- `pollTaskStatus(taskId)`: GET /api/task_status
- Handle arxivId vs fileId parameter mapping
- 10s timeout for polling requests

**Acceptance**:
- Task creation returns taskId
- Polling returns status updates (queued, generating, completed, failed)
- Errors handled gracefully

**Dependencies**: T009

---

### T013 - Initialize Pinia in main.js
**Story**: Foundational
**Files**:
- `src/main.js`

**Description**:
Import `createPinia` from Pinia. Create Pinia instance and register with Vue app using `app.use(pinia)` before `app.mount('#app')`.

**Acceptance**:
- Pinia devtools visible in Vue DevTools
- Stores can be imported and used in components
- State reactivity works

**Dependencies**: T002

---

### T014 [P] - Create Papers Pinia Store
**Story**: Foundational
**Files**:
- `src/stores/papers.js`

**Description**:
Create `papers` store with state:
- `papers: []` - Current paper list
- `loading: false` - Loading state
- `error: null` - Error message
- `selectedPeriod: 'daily'` - Active tab
- `currentPage: 1` - Pagination state
- `totalPages: 1` - Total pages

Actions:
- `fetchPapers(period, page)`: Fetch papers and update state
- `setPeriod(period)`: Switch tab and reset to page 1
- `setPage(page)`: Navigate to specific page

**Acceptance**:
- Store reactive in components
- `fetchPapers()` calls `paperService.fetchArxivPapers()`
- Error state updates on API failures

**Dependencies**: T010, T013

---

### T015 [P] - Create Tasks Pinia Store
**Story**: Foundational
**Files**:
- `src/stores/tasks.js`

**Description**:
Create `tasks` store with state:
- `tasks: []` - Task history array
- `pollingActive: false` - Polling state flag

Computed:
- `activeTasks`: Filter tasks with status 'queued' or 'generating'

Actions:
- `createTask(paperId, paperTitle)`: Create new PPT task
- `startPolling()`: Begin 5-second interval polling
- `stopPolling()`: Clear interval
- `updateTaskStatus(taskId, statusData)`: Update task from poll result
- `saveTasksToLocalStorage()`: Persist to localStorage
- `loadTasksFromLocalStorage()`: Restore on mount

**Acceptance**:
- Tasks persist across page reloads
- Polling auto-starts when active tasks exist
- Polling stops when no active tasks remain

**Dependencies**: T012, T013

---

### T016 [P] - Create UI Pinia Store
**Story**: Foundational
**Files**:
- `src/stores/ui.js`

**Description**:
Create `ui` store with state:
- `modalOpen: false` - Modal visibility
- `currentPaper: null` - Paper being viewed
- `currentAnalysis: null` - Analysis data for modal
- `analysisLoading: false` - Analysis loading state
- `toastVisible: false` - Toast notification state
- `toastMessage: ''` - Toast text
- `toastType: 'info'` - Toast type (success, error, info)

Actions:
- `openModal(paperId)`: Fetch analysis and open modal
- `closeModal()`: Close modal and reset state
- `showToast(message, type)`: Display toast notification
- `hideToast()`: Dismiss toast

**Acceptance**:
- Modal opens with paper analysis
- Toast auto-dismisses after 3 seconds
- Analysis retries on 202 (pending) response

**Dependencies**: T010, T013

---

### T017 [P] - Create useTaskHistory Composable
**Story**: Foundational
**Files**:
- `src/composables/useTaskHistory.js`

**Description**:
Extract localStorage task persistence logic:
- `saveTasksToLocalStorage(tasks)`: Write to localStorage
- `loadTasksFromLocalStorage()`: Read from localStorage
- `clearExpiredTasks()`: Remove tasks >24 hours old
- Handle 5MB localStorage quota (auto-prune oldest completed tasks)

**Acceptance**:
- Tasks persist across sessions
- Expired tasks auto-removed
- Quota exceeded errors handled gracefully

**Dependencies**: T013

---

### T018 [P] - Create useTaskPolling Composable
**Story**: Foundational
**Files**:
- `src/composables/useTaskPolling.js`

**Description**:
Extract polling logic:
- `startPolling(tasks)`: Begin 5-second `setInterval`
- `stopPolling()`: Clear interval
- Poll all active tasks using `Promise.allSettled()`
- Invoke callback on status updates

**Acceptance**:
- Polls every 5 seconds when active tasks exist
- Stops when no active tasks
- Individual poll failures don't crash interval

**Dependencies**: T012, T013

---

### T019 [P] - Create useFileUpload Composable
**Story**: Foundational
**Files**:
- `src/composables/useFileUpload.js`

**Description**:
Extract file upload logic:
- `progress: ref(0)` - Upload percentage
- `uploading: ref(false)` - Upload state
- `error: ref(null)` - Error message
- `uploadFile(file)`: Validate file, call uploadService, track progress

Client-side validations:
- File type must be `application/pdf`
- File size <= 20MB

**Acceptance**:
- Upload progress updates reactively (0-100)
- Validation errors shown before upload starts
- Successful upload returns fileId

**Dependencies**: T011, T013

---

## Phase 3: US1 - Discover and Analyze Trending Papers (P1)

### T020 - Create Button Common Component
**Story**: US1
**Files**:
- `src/components/common/Button.vue`

**Description**:
Reusable button with props:
- `variant`: 'primary' | 'secondary' | 'ghost'
- `size`: 'small' | 'medium' | 'large'
- `disabled`: boolean
- `loading`: boolean (shows spinner)

Styles per design system: 6px border-radius, accent color for primary, hover/active states.

**Acceptance**:
- All variants render correctly
- Disabled state prevents clicks
- Loading state shows spinner icon

**Dependencies**: T003

---

### T021 - Create Badge Common Component
**Story**: US1
**Files**:
- `src/components/common/Badge.vue`

**Description**:
Badge component for status display:
- Props: `status` (queued, generating, completed, failed)
- Colors per constitution: yellow (queued), blue (generating), green (completed), red (failed)
- Text mapping: "排队中", "生成中", "已完成", "失败"

**Acceptance**:
- Correct color applied for each status
- Chinese labels display correctly
- Pill shape with padding

**Dependencies**: T003

---

### T022 - Create Modal Common Component
**Story**: US1
**Files**:
- `src/components/common/Modal.vue`

**Description**:
Full-screen modal using Headless UI `<Dialog>`:
- Backdrop blur and dimming
- Close on ESC key
- Close button (X icon top-right)
- Slot for content
- Focus trap
- 12px border-radius per design system

**Acceptance**:
- Opens/closes smoothly with transition
- Backdrop click closes modal
- ESC key closes modal
- Focus trapped inside modal

**Dependencies**: T002, T003

---

### T023 - Create Tabs Common Component
**Story**: US1
**Files**:
- `src/components/common/Tabs.vue`

**Description**:
Tab navigation using Headless UI `<TabGroup>`:
- Props: `tabs` (array of {key, label} objects), `modelValue` (active tab)
- Emits: `update:modelValue` on tab change
- Active tab styling: accent color underline, bold text
- Inactive tabs: secondary text color

**Acceptance**:
- Tabs switch on click
- Active tab visually distinct
- Keyboard navigation works (arrow keys)

**Dependencies**: T002, T003

---

### T024 - Create Toast Common Component
**Story**: US1
**Files**:
- `src/components/common/Toast.vue`

**Description**:
Toast notification component:
- Props: `visible`, `message`, `type` (success, error, info)
- Auto-dismiss after 3 seconds (configurable)
- Positioned top-center, fixed
- Icon based on type: ✓ (success), ✕ (error), ℹ (info)
- Slide-in/fade-out transition

**Acceptance**:
- Toasts appear at top-center
- Auto-dismiss after 3s
- Multiple toasts stack vertically

**Dependencies**: T003

---

### T025 - Create PaperCard Core Component
**Story**: US1
**Files**:
- `src/components/core/PaperCard.vue`

**Description**:
Display paper in grid layout:
- Props: `paper` (Paper entity)
- Show: title (2-line ellipsis), authors (comma-separated, 1-line ellipsis), field badge, keywords (max 3)
- Click triggers modal open via `uiStore.openModal(paper.id)`
- Hover effect: subtle shadow, scale 1.02

**Acceptance**:
- Text truncation works correctly
- Hover animation smooth
- Click opens modal with paper details

**Dependencies**: T003, T016, T021

---

### T026 - Create PaperModal Core Component
**Story**: US1
**Files**:
- `src/components/core/PaperModal.vue`

**Description**:
Modal content for paper analysis:
- Uses `<Modal>` component
- Displays: paper metadata, Chinese summary (prominent), innovation points (bullet list)
- Skeleton loading state while `analysisLoading === true`
- Button: "一键生成组会PPT" triggers task creation
- Button states: normal, loading ("创建中..."), disabled (when task exists)

**Acceptance**:
- Analysis loads when modal opens
- Skeleton displays during loading
- Generate PPT button creates task and closes modal

**Dependencies**: T012, T016, T020, T022

---

### T027 - Create PaperDiscovery Core Component
**Story**: US1
**Files**:
- `src/components/core/PaperDiscovery.vue`

**Description**:
Main paper discovery section:
- Tab navigation: Daily, Weekly, Monthly (uses `<Tabs>`)
- Paper grid: 4 columns on desktop, 2 on tablet, 1 on mobile
- Loading skeleton: 8 placeholder cards
- Empty state: "No papers found" message
- Error state: Error banner with retry button

**Acceptance**:
- Papers load on mount (default: daily)
- Tab switch fetches new papers
- Grid responsive across breakpoints
- Retry button re-fetches on error

**Dependencies**: T014, T023, T025

---

### T028 - Create HomeView
**Story**: US1
**Files**:
- `src/views/HomeView.vue`

**Description**:
Root view component with layout:
- Fixed header: Logo + title "论导Lite - AI助你三分钟搞定组会PPT"
- Main content area: `<PaperDiscovery>` and `<TaskHistory>` (placeholder)
- Footer: Copyright text
- Padding for fixed header (pt-20)

**Acceptance**:
- Header stays fixed on scroll
- Content doesn't overlap with header
- Footer at bottom of viewport

**Dependencies**: T027

---

### T029 - Update App.vue to Use HomeView
**Story**: US1
**Files**:
- `src/App.vue`

**Description**:
Replace default Vite template with:
```vue
<script setup>
import HomeView from '@/views/HomeView.vue'
</script>

<template>
  <div id="app" class="min-h-screen bg-primary-bg">
    <HomeView />
  </div>
</template>
```

**Acceptance**:
- HomeView renders on app root
- Background color applies correctly
- Min-height ensures footer at bottom

**Dependencies**: T028

---

### T030 - Implement Analysis Loading Retry Logic
**Story**: US1
**Files**:
- `src/stores/ui.js`

**Description**:
Enhance `openModal()` action to handle 202 (pending) responses:
- If `analysisStatus === 'pending'`, wait `retryAfter` seconds (default 15s)
- Recursively retry up to 3 times
- Show error if still pending after 3 retries

**Acceptance**:
- Modal shows skeleton during retries
- Analysis displays after completion
- Error message if 3 retries exhausted

**Dependencies**: T016, T026

---

### T031 [P] - Add Paper Loading Skeleton
**Story**: US1
**Files**:
- `src/components/core/PaperDiscovery.vue`

**Description**:
Add skeleton screen for paper loading:
- 8 placeholder cards with pulse animation
- Skeleton bars for title, authors, keywords
- Displayed when `papersStore.loading === true`

**Acceptance**:
- Skeleton displays immediately on fetch
- Smooth transition to real cards
- Pulse animation visible

**Dependencies**: T027

---

### T032 [P] - Add Analysis Loading Skeleton
**Story**: US1
**Files**:
- `src/components/core/PaperModal.vue`

**Description**:
Add skeleton for analysis loading:
- Skeleton bars for summary (3 lines)
- Skeleton bullets for innovation points (5 items)
- Displayed when `uiStore.analysisLoading === true`

**Acceptance**:
- Skeleton displays during analysis fetch
- Smooth transition to real content
- Layout doesn't shift on content load

**Dependencies**: T026

---

## Phase 4: US2 - Upload and Analyze Custom Papers (P2)

### T033 - Create UploadDropzone Core Component
**Story**: US2
**Files**:
- `src/components/core/UploadDropzone.vue`

**Description**:
Drag-and-drop file upload component:
- Drag-over state: Blue border, "Drop PDF here" text
- File input button: "Choose PDF" for manual selection
- Validation: Show error if non-PDF or >20MB
- Uses `useFileUpload` composable
- Progress bar: 0-100% with percentage label
- Auto-trigger analysis on upload success

**Acceptance**:
- Drag-and-drop works correctly
- File input opens file picker
- Validation errors display before upload
- Progress bar updates during upload
- Analysis modal opens after upload

**Dependencies**: T019, T016

---

### T034 - Integrate UploadDropzone into HomeView
**Story**: US2
**Files**:
- `src/views/HomeView.vue`

**Description**:
Add `<UploadDropzone>` component above `<PaperDiscovery>` in HomeView:
- Section title: "上传自定义论文"
- Descriptive text: "支持PDF格式，最大20MB"
- Spacing: 24px margin below dropzone

**Acceptance**:
- Dropzone visible above paper discovery
- Upload flow works end-to-end
- Modal opens with uploaded paper analysis

**Dependencies**: T028, T033

---

### T035 - Handle Upload Progress UI States
**Story**: US2
**Files**:
- `src/components/core/UploadDropzone.vue`

**Description**:
Enhance UploadDropzone with progress states:
- 0%: Default state, dropzone interactive
- 1-24%: "Preparing upload..."
- 25-74%: "Uploading... {percent}%"
- 75-99%: "Finalizing..."
- 100%: "Upload complete! Analyzing..."
- Disable dropzone during upload

**Acceptance**:
- State transitions smooth
- Progress bar fills correctly
- User cannot upload second file during active upload

**Dependencies**: T033

---

### T036 - Handle Upload Error States
**Story**: US2
**Files**:
- `src/components/core/UploadDropzone.vue`

**Description**:
Add error handling for upload failures:
- Network errors: "Upload failed. Please check your connection."
- File too large (413): "File exceeds 20MB limit."
- Invalid PDF (422): "Unable to process this PDF. It may be corrupted or encrypted."
- Timeout (120s): "Upload timed out. Please try a smaller file."
- Show error message in red text below dropzone
- Reset state after 5 seconds or on new file selection

**Acceptance**:
- Error messages display correctly
- User can retry after error
- Error auto-clears after 5s

**Dependencies**: T033

---

### T037 - Add File Preview in Dropzone
**Story**: US2
**Files**:
- `src/components/core/UploadDropzone.vue`

**Description**:
Show file preview after selection (before upload):
- Display: filename, file size (formatted KB/MB)
- Icon: PDF icon
- Remove button: Clear selection
- Only show preview if file valid (PDF, <=20MB)

**Acceptance**:
- Filename displays correctly
- File size formatted (e.g., "2.4 MB")
- Remove button clears selection and resets UI

**Dependencies**: T033

---

## Phase 5: US3 - Generate and Track PPT (P1)

### T038 - Create TaskItem Core Component
**Story**: US3
**Files**:
- `src/components/core/TaskItem.vue`

**Description**:
Display individual task in history:
- Props: `task` (PPTTask entity)
- Show: paper title, status badge, timestamps (relative time, e.g., "2 minutes ago")
- Conditional content based on status:
  - **Queued**: Queue position, estimated time
  - **Generating**: Progress bar (if available), estimated time
  - **Completed**: Download button, file size, expiration warning
  - **Failed**: Error message, retry button
- Delete button: Remove task from history

**Acceptance**:
- All statuses render correctly
- Download button triggers file download
- Retry button creates new task
- Delete removes task from list

**Dependencies**: T015, T020, T021

---

### T039 - Create TaskHistory Core Component
**Story**: US3
**Files**:
- `src/components/core/TaskHistory.vue`

**Description**:
Task history section in HomeView:
- Section title: "生成历史"
- Task list: `<TaskItem>` for each task, newest first
- Empty state: "No PPT generation tasks yet. Click 'Generate PPT' in any paper modal to start."
- Max height: 600px, scroll overflow

**Acceptance**:
- Tasks display in reverse chronological order
- Empty state shows when no tasks
- Scroll works when >5 tasks

**Dependencies**: T015, T038

---

### T040 - Integrate TaskHistory into HomeView
**Story**: US3
**Files**:
- `src/views/HomeView.vue`

**Description**:
Add `<TaskHistory>` component below `<PaperDiscovery>`:
- Spacing: 48px margin-top
- Full-width container

**Acceptance**:
- Task history visible on page
- Tasks update in real-time during polling

**Dependencies**: T028, T039

---

### T041 - Implement Task Creation from Modal
**Story**: US3
**Files**:
- `src/components/core/PaperModal.vue`
- `src/stores/tasks.js`

**Description**:
Wire "Generate PPT" button to task creation:
- Button click calls `tasksStore.createTask(paperId, paperTitle)`
- Show loading state during request ("创建中...")
- On success: Close modal, show toast "PPT generation task created"
- On error: Show error toast, keep modal open

**Acceptance**:
- Task appears in history after creation
- Modal closes on success
- Toast notification displays
- Polling starts if not already active

**Dependencies**: T012, T015, T016, T026

---

### T042 - Implement Task Polling Logic
**Story**: US3
**Files**:
- `src/stores/tasks.js`

**Description**:
Implement `startPolling()` action:
- Use `setInterval` with 5000ms interval
- On each tick:
  - Filter tasks with status 'queued' or 'generating'
  - Poll each task using `taskService.pollTaskStatus(taskId)`
  - Update task status with `updateTaskStatus(taskId, statusData)`
- Stop polling when `activeTasks.length === 0`
- Use `Promise.allSettled()` to handle individual failures

**Acceptance**:
- Polling starts when first active task created
- Status updates every 5 seconds
- Polling stops when all tasks completed/failed
- Individual poll errors don't crash interval

**Dependencies**: T012, T015, T018

---

### T043 - Implement Task Status Update Handlers
**Story**: US3
**Files**:
- `src/stores/tasks.js`

**Description**:
Implement `updateTaskStatus()` action:
- Find task by ID in `tasks` array
- Update properties: status, completedAt, downloadUrl, errorMessage
- Call `saveTasksToLocalStorage()` after update
- Show toast on status transitions:
  - **Completed**: "PPT for \"{paperTitle}\" is ready!"
  - **Failed**: "PPT generation failed: {errorMessage}"

**Acceptance**:
- Task statuses update correctly
- Toast notifications trigger on completion/failure
- localStorage syncs after each update

**Dependencies**: T015, T016, T017

---

### T044 - Implement Task Deletion
**Story**: US3
**Files**:
- `src/stores/tasks.js`
- `src/components/core/TaskItem.vue`

**Description**:
Add `deleteTask(taskId)` action in tasks store:
- Remove task from `tasks` array
- Call `saveTasksToLocalStorage()`
- Show toast: "Task deleted"

Wire delete button in TaskItem to call `tasksStore.deleteTask(task.id)`.

**Acceptance**:
- Delete button removes task from list
- Deleted tasks removed from localStorage
- Toast confirmation displays

**Dependencies**: T015, T017, T038

---

### T045 - Implement Task Retry
**Story**: US3
**Files**:
- `src/stores/tasks.js`
- `src/components/core/TaskItem.vue`

**Description**:
Add retry button for failed tasks in TaskItem:
- Button calls `tasksStore.createTask(task.paperId, task.paperTitle)`
- Increment `retryCount` on existing failed task
- Create new task (don't modify failed task)
- Show toast: "Retrying PPT generation..."

**Acceptance**:
- Retry button creates new task
- Failed task remains in history
- New task starts with "queued" status

**Dependencies**: T015, T038, T041

---

### T046 - Implement Download Button
**Story**: US3
**Files**:
- `src/components/core/TaskItem.vue`

**Description**:
Wire download button for completed tasks:
- Use `<a :href="task.downloadUrl" download>` element styled as button
- Show file size and expiration time
- Warning if expiring soon (<2 hours): "Expires in X hours"

**Acceptance**:
- Download button triggers file download
- File downloads with correct filename
- Expiration warning displays when <2 hours remaining

**Dependencies**: T038

---

### T047 - Implement localStorage Persistence
**Story**: US3
**Files**:
- `src/stores/tasks.js`
- `src/composables/useTaskHistory.js`

**Description**:
Implement persistence functions:
- `saveTasksToLocalStorage()`: Write `tasks` array to localStorage as JSON
- `loadTasksFromLocalStorage()`: Read and parse JSON on mount
- `clearExpiredTasks()`: Remove tasks where `expiresAt < now()` (24 hours old)
- Handle quota exceeded: Auto-prune oldest completed tasks

**Acceptance**:
- Tasks persist across page reloads
- Expired tasks auto-removed on mount
- Quota errors handled gracefully (prune + retry)

**Dependencies**: T015, T017

---

### T048 - Implement Auto-Start Polling on Mount
**Story**: US3
**Files**:
- `src/stores/tasks.js`

**Description**:
Add lifecycle logic in tasks store:
- On mount: Load tasks from localStorage
- If `activeTasks.length > 0`: Call `startPolling()`
- On unmount: Call `stopPolling()` to clean up interval

Use Vue's `onMounted` and `onUnmounted` hooks in store setup.

**Acceptance**:
- Polling resumes after page reload if active tasks exist
- No polling if only completed/failed tasks in localStorage
- Interval clears on component unmount (no memory leaks)

**Dependencies**: T015, T017, T042

---

### T049 - Add Task Progress Bar (Optional Field)
**Story**: US3
**Files**:
- `src/components/core/TaskItem.vue`

**Description**:
Display progress bar for generating tasks if `task.progress` exists:
- Progress bar: 0-100%, blue color
- Label: "{progress}% complete"
- Fallback: Indeterminate spinner if no progress value

**Acceptance**:
- Progress bar displays when value available
- Indeterminate spinner when no progress
- Smooth progress updates during polling

**Dependencies**: T038

---

### T050 - Handle 409 Conflict on Duplicate Task Creation
**Story**: US3
**Files**:
- `src/stores/tasks.js`

**Description**:
Enhance `createTask()` to handle 409 (task already exists):
- Catch 409 error response
- Extract `existingTaskId` from error details
- Find existing task in history
- Show toast: "PPT generation already in progress for this paper"
- Scroll to existing task in history (if visible)

**Acceptance**:
- Duplicate task creation blocked
- User notified of existing task
- Existing task highlighted/scrolled to

**Dependencies**: T015, T041

---

### T051 - Handle Task Expiration (410 Gone)
**Story**: US3
**Files**:
- `src/stores/tasks.js`

**Description**:
Handle 410 response during polling:
- Mark task status as "expired"
- Show error message: "This task has expired (>24 hours old)"
- Remove from active polling list
- Keep in history for reference

**Acceptance**:
- Expired tasks no longer polled
- Error message displays in TaskItem
- User can delete expired tasks

**Dependencies**: T015, T042, T043

---

## Phase 6: US4 - Navigate Paginated Paper Lists (P3)

### T052 - Create Pagination Common Component
**Story**: US4
**Files**:
- `src/components/common/Pagination.vue`

**Description**:
Pagination controls component:
- Props: `currentPage`, `totalPages`, `onPageChange` callback
- Show: Previous button, page numbers (max 7 visible), Next button
- Disable Previous on page 1, disable Next on last page
- Highlight current page with accent color
- Ellipsis (...) for hidden pages (e.g., "1 ... 5 6 7 ... 10")

**Acceptance**:
- Page numbers displayed correctly
- Buttons trigger page changes
- Disabled states prevent invalid navigation
- Ellipsis shows for large page counts

**Dependencies**: T003, T020

---

### T053 - Integrate Pagination into PaperDiscovery
**Story**: US4
**Files**:
- `src/components/core/PaperDiscovery.vue`

**Description**:
Add `<Pagination>` component below paper grid:
- Bind to `papersStore.currentPage` and `papersStore.totalPages`
- On page change: Call `papersStore.setPage(newPage)`
- Scroll to top of paper grid on page change

**Acceptance**:
- Pagination controls visible when totalPages > 1
- Page changes fetch new papers
- Scroll-to-top on navigation
- Current page persists during tab switch

**Dependencies**: T014, T027, T052

---

### T054 - Implement setPage Action in Papers Store
**Story**: US4
**Files**:
- `src/stores/papers.js`

**Description**:
Add `setPage(page)` action:
- Validate page number (1 <= page <= totalPages)
- Update `currentPage` state
- Call `fetchPapers(selectedPeriod, page)`
- Handle errors (e.g., page out of range)

**Acceptance**:
- Page navigation fetches correct papers
- Invalid page numbers rejected
- Loading state shown during fetch

**Dependencies**: T014

---

### T055 - Handle Page Out of Range Errors
**Story**: US4
**Files**:
- `src/stores/papers.js`

**Description**:
Handle 400 error with `PAGE_OUT_OF_RANGE` code:
- Show error toast: "Invalid page number"
- Reset to page 1
- Re-fetch papers for page 1

**Acceptance**:
- Out-of-range requests don't crash app
- User redirected to page 1
- Error message displayed

**Dependencies**: T014, T054

---

### T056 - Preserve Page State During Tab Switch
**Story**: US4
**Files**:
- `src/stores/papers.js`

**Description**:
Enhance `setPeriod(period)` action:
- When changing period (tab), reset `currentPage` to 1
- Fetch papers for new period starting at page 1
- Clear previous papers during fetch

**Acceptance**:
- Tab switch resets to page 1
- No leftover papers from previous tab
- Loading state during transition

**Dependencies**: T014

---

### T057 - Add Keyboard Navigation for Pagination
**Story**: US4
**Files**:
- `src/components/common/Pagination.vue`

**Description**:
Add keyboard shortcuts:
- Arrow Left: Previous page
- Arrow Right: Next page
- Home: First page
- End: Last page

Only active when pagination controls focused.

**Acceptance**:
- Arrow keys navigate pages
- Home/End jump to first/last page
- Shortcuts work when pagination focused

**Dependencies**: T052

---

## Phase 7: Polish and Edge Cases

### T058 [P] - Add Fade Transitions to Paper Cards
**Story**: Polish
**Files**:
- `src/components/core/PaperDiscovery.vue`

**Description**:
Wrap paper grid in `<TransitionGroup>` with fade animation:
- Fade-in on mount and page change
- Stagger effect: Delay each card by 50ms (index * 50ms)

**Acceptance**:
- Cards fade in smoothly
- Stagger effect visible
- No layout shift during transition

**Dependencies**: T027

---

### T059 [P] - Add Modal Slide-Up Transition
**Story**: Polish
**Files**:
- `src/components/common/Modal.vue`

**Description**:
Enhance modal with slide-up transition:
- Backdrop: Fade-in 200ms
- Modal content: Slide-up from bottom + fade-in 300ms
- Exit: Reverse animation

**Acceptance**:
- Modal opens with smooth slide-up
- Backdrop fades independently
- Close animation smooth

**Dependencies**: T022

---

### T060 [P] - Add Toast Slide-In Animation
**Story**: Polish
**Files**:
- `src/components/common/Toast.vue`

**Description**:
Add slide-in animation from top:
- Enter: Slide-down + fade-in 300ms
- Exit: Slide-up + fade-out 200ms

**Acceptance**:
- Toasts slide in from above viewport
- Exit animation smooth
- Multiple toasts animate independently

**Dependencies**: T024

---

### T061 [P] - Add Loading Spinner for Buttons
**Story**: Polish
**Files**:
- `src/components/common/Button.vue`

**Description**:
Add spinner icon for `loading` prop:
- Show animated spinner (rotate 360deg loop)
- Hide button text during loading
- Disable button during loading

**Acceptance**:
- Spinner visible when loading=true
- Spinner rotates smoothly
- Button disabled during loading

**Dependencies**: T020

---

### T062 [P] - Add Hover Effects to Paper Cards
**Story**: Polish
**Files**:
- `src/components/core/PaperCard.vue`

**Description**:
Enhance hover effect:
- Scale: 1.02
- Shadow: Increase from subtle to medium
- Transition: 200ms ease-out
- Cursor: Pointer

**Acceptance**:
- Hover effect smooth
- Shadow transition visible
- Scale doesn't cause layout shift

**Dependencies**: T025

---

### T063 [P] - Add Empty State Illustrations
**Story**: Polish
**Files**:
- `src/components/core/PaperDiscovery.vue`
- `src/components/core/TaskHistory.vue`

**Description**:
Replace text-only empty states with illustrations:
- Paper discovery: SVG illustration of empty folder
- Task history: SVG illustration of checklist
- Text below illustration with clear call-to-action

**Acceptance**:
- Illustrations display correctly
- Text provides clear next steps
- SVGs responsive to viewport size

**Dependencies**: T027, T039

---

### T064 - Handle Network Offline State
**Story**: Polish
**Files**:
- `src/api/index.js`

**Description**:
Detect offline state in Axios interceptor:
- Check `navigator.onLine` before request
- If offline: Reject with custom error "You are offline. Please check your connection."
- Show toast notification for offline errors

**Acceptance**:
- Offline errors caught before request sent
- User notified via toast
- Requests retry when back online

**Dependencies**: T009

---

### T065 - Handle API Timeout Errors
**Story**: Polish
**Files**:
- `src/api/index.js`

**Description**:
Enhance response interceptor to detect timeout:
- Check `error.code === 'ECONNABORTED'`
- Show toast: "Request timed out. Please try again."
- Provide retry button in toast (optional)

**Acceptance**:
- Timeout errors display clearly
- User can retry manually
- Timeout value configurable per request

**Dependencies**: T009

---

### T066 - Handle 503 Service Unavailable
**Story**: Polish
**Files**:
- `src/api/index.js`

**Description**:
Handle 503 errors globally:
- Check `response.status === 503`
- Extract `retryAfter` from response (seconds)
- Show toast: "Service temporarily unavailable. Retrying in {retryAfter}s..."
- Auto-retry after delay (if user hasn't navigated away)

**Acceptance**:
- 503 errors handled gracefully
- Auto-retry after specified delay
- User can cancel retry

**Dependencies**: T009

---

### T067 - Handle 404 Paper Not Found
**Story**: Polish
**Files**:
- `src/stores/ui.js`

**Description**:
Handle 404 during `openModal()`:
- Show error in modal: "Paper not found. It may have been removed."
- Disable "Generate PPT" button
- Provide "Close" button

**Acceptance**:
- 404 errors display in modal
- User can close modal and try different paper
- Error message clear

**Dependencies**: T016, T026

---

### T068 - Handle 422 Analysis Failed
**Story**: Polish
**Files**:
- `src/stores/ui.js`

**Description**:
Handle 422 during `openModal()`:
- Show error: "Unable to analyze this paper. The PDF may be corrupted or in an unsupported format."
- Disable "Generate PPT" button
- Show paper metadata (title, authors) but no analysis

**Acceptance**:
- 422 errors display clearly
- User understands why analysis failed
- PPT generation blocked for invalid papers

**Dependencies**: T016, T026

---

### T069 - Add Analysis Timeout Handling
**Story**: Polish
**Files**:
- `src/stores/ui.js`

**Description**:
Handle 504 timeout during analysis:
- Show error: "Analysis took too long. Please try again or contact support if this persists."
- Provide "Retry" button in modal
- Retry button re-fetches analysis

**Acceptance**:
- 504 errors handled gracefully
- User can retry from modal
- Retry button works correctly

**Dependencies**: T016, T026, T030

---

### T070 - Add File Size Formatting Utility
**Story**: Polish
**Files**:
- `src/utils/formatters.js`

**Description**:
Create utility function `formatFileSize(bytes)`:
- Returns formatted string: "2.4 MB", "150 KB", "1.2 GB"
- Handles edge cases: 0 bytes → "0 Bytes", negative → "Invalid"

**Acceptance**:
- File sizes display correctly throughout app
- Formatting accurate to 1 decimal place
- Handles all size ranges (bytes to GB)

**Dependencies**: None

---

### T071 - Add Relative Time Formatting Utility
**Story**: Polish
**Files**:
- `src/utils/formatters.js`

**Description**:
Create utility function `formatRelativeTime(timestamp)`:
- Returns: "just now", "2 minutes ago", "3 hours ago", "yesterday", "5 days ago"
- Uses native `Intl.RelativeTimeFormat` or fallback

**Acceptance**:
- Timestamps formatted correctly
- Updates in real-time (e.g., "2 minutes ago" → "3 minutes ago")
- Supports Chinese locale

**Dependencies**: None

---

### T072 - Add Loading State for Paper Discovery on Mount
**Story**: Polish
**Files**:
- `src/components/core/PaperDiscovery.vue`

**Description**:
Ensure loading skeleton displays immediately on component mount:
- On `onMounted()`: Set `papersStore.loading = true`
- Call `papersStore.fetchPapers('daily', 1)`
- Skeleton displays until fetch completes

**Acceptance**:
- No blank screen on mount
- Skeleton displays immediately
- Smooth transition to paper cards

**Dependencies**: T027, T031

---

### T073 - Handle Very Long Paper Titles
**Story**: Polish
**Files**:
- `src/components/core/PaperCard.vue`

**Description**:
Ensure title truncation works correctly:
- Max 2 lines with ellipsis (`line-clamp-2`)
- Tooltip on hover shows full title
- Title doesn't break layout

**Acceptance**:
- Long titles truncate correctly
- Tooltip displays full title
- Layout stable with varying title lengths

**Dependencies**: T025

---

### T074 - Handle Empty Keywords Array
**Story**: Polish
**Files**:
- `src/components/core/PaperCard.vue`

**Description**:
Handle papers with no keywords:
- If `paper.keywords.length === 0`: Show placeholder text "No keywords"
- Style: Secondary text color, italic

**Acceptance**:
- Empty keywords don't break layout
- Placeholder text displays correctly
- No errors when keywords missing

**Dependencies**: T025

---

### T075 - Add Focus Trap for Modal
**Story**: Polish
**Files**:
- `src/components/common/Modal.vue`

**Description**:
Ensure focus trap works correctly (Headless UI default):
- Tab key cycles through focusable elements in modal
- Shift+Tab reverses direction
- Focus returns to trigger element on close

**Acceptance**:
- Tab key doesn't leave modal
- Focus order logical (top to bottom)
- Focus restores correctly on close

**Dependencies**: T022

---

### T076 - Add Scroll Lock When Modal Open
**Story**: Polish
**Files**:
- `src/components/common/Modal.vue`

**Description**:
Prevent body scroll when modal open:
- Add `overflow: hidden` to body on modal open
- Remove on modal close
- Handle multiple modals (stack count)

**Acceptance**:
- Body scroll locked when modal open
- Scroll works inside modal content
- Body scroll restores on close

**Dependencies**: T022

---

### T077 - Add localStorage Quota Exceeded Handling
**Story**: Polish
**Files**:
- `src/composables/useTaskHistory.js`

**Description**:
Handle `QuotaExceededError` during `saveTasksToLocalStorage()`:
- Catch error
- Prune oldest completed tasks (keep max 50 most recent)
- Retry save
- If still fails: Show toast warning "Storage limit reached. Oldest tasks removed."

**Acceptance**:
- Quota errors don't crash app
- Oldest tasks auto-pruned
- User notified of pruning

**Dependencies**: T017, T047

---

### T078 - Add Manual Test Checklist
**Story**: Polish
**Files**:
- `specs/001-mvp-frontend-implementation/test-checklist.md`

**Description**:
Create manual testing checklist document with test cases for:
- Paper discovery (all tabs, pagination)
- Paper analysis (modal, loading, errors)
- File upload (drag-drop, validation, progress)
- PPT generation (task creation, polling, download)
- Edge cases (offline, timeouts, errors)
- Responsive design (mobile, tablet, desktop)

**Acceptance**:
- Checklist covers all user stories
- Each test case has clear steps and expected results
- Checklist ready for QA handoff

**Dependencies**: None (documentation task)

---

## Execution Order

### Critical Path (Sequential)
1. **Phase 1 (T001-T008)**: Must complete in order
2. **Phase 2 (T009-T019)**: T009 blocks all services; T013 blocks all stores/composables
3. **Phase 3 (T020-T032)**: Build US1 components; T020-T024 (common components) can run parallel
4. **Phase 4 (T033-T037)**: US2 depends on T019 (upload composable) and T016 (ui store)
5. **Phase 5 (T038-T051)**: US3 depends on T015 (tasks store) and T012 (task service)
6. **Phase 6 (T052-T057)**: US4 depends on T014 (papers store)
7. **Phase 7 (T058-T078)**: Polish tasks mostly independent, can run in parallel

### Parallel Opportunities
- **T010, T011, T012**: All service modules can be built in parallel after T009
- **T014, T015, T016**: All stores can be built in parallel after T013
- **T017, T018, T019**: All composables can be built in parallel after T013
- **T020, T021, T022, T023, T024**: All common components can be built in parallel
- **T031, T032**: Skeleton components can be added in parallel
- **T058-T063**: All animation tasks can run in parallel
- **T064-T069**: All error handling tasks can run in parallel

### Dependency Graph (High-Level)
```
Setup (T001-T008)
  ↓
API Client (T009) ────┬──→ Services (T010, T011, T012) [P]
  ↓                   │
Pinia Init (T013) ────┴──→ Stores (T014, T015, T016) [P]
  ↓                        Composables (T017, T018, T019) [P]
  ↓
Common Components (T020-T024) [P]
  ↓
US1 Core Components (T025-T027)
  ↓
HomeView + App (T028-T029)
  ↓
US1 Polish (T030-T032)
  ↓
US2 Upload (T033-T037) ──┬──→ [Can run parallel with US3 after foundational]
  ↓                      │
US3 Tasks (T038-T051) ───┘
  ↓
US4 Pagination (T052-T057)
  ↓
Polish + Edge Cases (T058-T078) [Many parallel]
```

---

## Implementation Notes

### MVP-First Approach
- Focus on happy path first (T001-T051)
- Add error handling and edge cases later (T064-T069)
- Polish animations after core functionality works (T058-T063)

### Component Isolation Strategy
- Build and test common components (Button, Modal, etc.) in isolation first
- Use mock data during development
- Integrate with stores/API only after components work standalone

### Testing Strategy
- Manual testing checklist (T078) guides QA
- Test each user story independently before integration
- Test edge cases systematically after core features work

### localStorage Management
- Implement quota handling early (T047, T077)
- Test with large task histories (100+ tasks)
- Verify pruning logic works correctly

### Polling Optimization
- Test polling with multiple tabs open (shared localStorage)
- Verify polling stops when all tasks complete
- Check for memory leaks (interval cleanup)

---

## Success Criteria Mapping

### US1 Success Criteria → Tasks
- ✅ Papers display within 2s: T027, T031 (loading state)
- ✅ Modal opens within 500ms: T026, T059 (modal transition)
- ✅ Analysis displays within 5-10s: T030 (retry logic)

### US2 Success Criteria → Tasks
- ✅ Upload progress visible: T035 (progress UI)
- ✅ Validation feedback <200ms: T036 (error states)

### US3 Success Criteria → Tasks
- ✅ Task appears in history <500ms: T041 (task creation)
- ✅ Status updates every 5-10s: T042 (polling interval)
- ✅ Download works after completion: T046 (download button)

### US4 Success Criteria → Tasks
- ✅ Page changes <2s: T054 (page fetch)
- ✅ Page state preserved: T056 (state management)

---

## Constitution Alignment

All tasks adhere to constitutional principles:

1. **Tool-First Philosophy**: No user accounts (T013-T016 stores have no auth)
2. **Single-Page Minimalism**: All features on HomeView (T028-T040)
3. **Zero Friction**: No login gates (all tasks accessible immediately)
4. **Value-First Design**: AI analysis prominently displayed (T026, T032)
5. **Aesthetics as Trust**: Strict design system adherence (T003, T020-T024)

---

**End of Task Breakdown**
**Ready for implementation**: Yes
**Next step**: Begin with T001 (Initialize Vite Project)
