# State Management Reference

Complete guide to Pinia stores and composables.

---

## Pinia Stores

### papers.js

**Location**: `src/stores/papers.js`

**State**:
```javascript
{
  papers: [],              // Array of paper objects
  loading: false,          // Loading state for API calls
  error: null,             // Error message (string | null)
  selectedPeriod: 'daily', // 'daily' | 'weekly' | 'monthly'
  currentPage: 1,          // Current pagination page
  totalPages: 1            // Total number of pages
}
```

**Actions**:
- `fetchPapers(period, page)` - Fetch papers from API/mock
- `setPeriod(period)` - Change time period + reset to page 1
- `setPage(page)` - Change page number

**Usage**:
```javascript
import { usePapersStore } from '@/stores/papers'

const papersStore = usePapersStore()

// Fetch daily papers, page 1
await papersStore.fetchPapers('daily', 1)

// Change period
papersStore.setPeriod('weekly')

// Navigate to page 2
papersStore.setPage(2)
```

---

### tasks.js

**Location**: `src/stores/tasks.js`

**State**:
```javascript
{
  tasks: [],           // Array of PPTTask objects
  pollingActive: false // Whether polling is active
}
```

**Computed**:
- `activeTasks` - Filters tasks with status `queued` or `generating`

**Actions**:
- `createTask(paperId, paperTitle, isArxiv)` - Create new PPT task
- `updateTaskStatus(taskId, statusData)` - Update task with polling data
- `startPolling()` - Start 5-second polling interval
- `stopPolling()` - Stop polling interval
- `deleteTask(taskId)` - Remove task from list
- `retryTask(taskId)` - Retry failed task

**Lifecycle**:
- `onMounted`: Load from localStorage, start polling if active tasks exist
- `onUnmounted`: Clear polling interval

**Task Object Structure**:
```javascript
{
  id: string,                    // Task ID (UUID or mock-task-xxx)
  paperId: string,               // Paper ID
  paperTitle: string,            // Paper title for display
  status: 'queued' | 'generating' | 'completed' | 'failed',
  createdAt: string,             // ISO timestamp
  completedAt: string | null,    // ISO timestamp
  downloadUrl: string | null,    // .pptx file URL
  errorMessage: string | null,   // Error message if failed
  progress: number | null,       // 0-100 during generating
  retryCount: number             // Number of retry attempts
}
```

**Usage**:
```javascript
import { useTasksStore } from '@/stores/tasks'

const tasksStore = useTasksStore()

// Create task
await tasksStore.createTask('2301.00000', 'Paper Title', true)

// Delete task
tasksStore.deleteTask('task-id')

// Check active tasks
console.log(tasksStore.activeTasks)  // [task1, task2]
```

**Polling Mechanism**:
- Interval: 5 seconds
- Polls all tasks with status `queued` or `generating`
- Auto-starts when active tasks exist
- Auto-stops when no active tasks remain

---

### ui.js

**Location**: `src/stores/ui.js`

**State**:
```javascript
{
  // Paper Modal
  modalOpen: false,
  currentPaper: null,
  currentAnalysis: null,
  analysisLoading: false,
  analysisError: null,

  // PPT Preview Modal
  pptPreviewOpen: false,
  currentPPTContent: null,
  pptContentLoading: false,
  pptContentError: null,

  // Toast Notifications
  toastVisible: false,
  toastMessage: '',
  toastType: 'info'  // 'success' | 'error' | 'info'
}
```

**Actions**:

**Paper Modal**:
- `openModal(paperId)` - Fetch paper + analysis, open modal
- `closeModal()` - Close modal, reset state

**PPT Preview Modal**:
- `openPPTPreview(taskId)` - Fetch PPT content, open preview
- `closePPTPreview()` - Close preview, reset state

**Toast**:
- `showToast(message, type)` - Show toast notification
- `hideToast()` - Hide toast

**Usage**:
```javascript
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()

// Open paper modal
await uiStore.openModal('paper-id')

// Open PPT preview
await uiStore.openPPTPreview('task-id')

// Show toast
uiStore.showToast('Upload successful!', 'success')

// Close modals
uiStore.closeModal()
uiStore.closePPTPreview()
```

**Analysis Retry Logic** (202 Pending):
```javascript
// openModal() handles 202 responses automatically
// Retries up to 3 times with exponential backoff
// Uses retryAfter header if provided
```

---

## Composables

### useTaskHistory.js

**Location**: `src/composables/useTaskHistory.js`

**Exports**:
- `saveTasksToLocalStorage(tasks)` - Save tasks array to localStorage
- `loadTasksFromLocalStorage()` - Load tasks from localStorage
- `clearTaskHistory()` - Clear all tasks from localStorage

**Features**:
- localStorage versioning (v2 format)
- Backward compatibility (v1 → v2 migration)
- Quota handling (auto-prune on QuotaExceededError)
- Auto-expiration (removes tasks >24 hours old)

**localStorage Format**:
```javascript
{
  version: 2,
  tasks: [
    { id, paperId, paperTitle, status, ... },
    ...
  ]
}
```

**Usage**:
```javascript
import { useTaskHistory } from '@/composables/useTaskHistory'

const { saveTasksToLocalStorage, loadTasksFromLocalStorage } = useTaskHistory()

// Load tasks
const tasks = loadTasksFromLocalStorage()

// Save tasks
saveTasksToLocalStorage(tasks)
```

---

### useTaskPolling.js

**Location**: `src/composables/useTaskPolling.js`

**Exports**:
- `startPolling(pollFn, interval)` - Start polling with callback
- `stopPolling()` - Stop polling and clear interval

**Features**:
- Configurable interval (default: 5000ms)
- Auto-cleanup on component unmount
- Promise.allSettled for individual task failures

**Usage**:
```javascript
import { useTaskPolling } from '@/composables/useTaskPolling'

const { startPolling, stopPolling } = useTaskPolling()

// Start polling
startPolling(async () => {
  // Poll logic here
  await pollTaskStatus()
}, 5000)

// Stop polling
stopPolling()
```

---

### useFileUpload.js

**Location**: `src/composables/useFileUpload.js`

**Exports**:
- `progress` - Upload progress (ref: 0-100)
- `uploading` - Upload active state (ref: boolean)
- `error` - Error message (ref: string | null)
- `fileId` - Uploaded file ID (ref: string | null)
- `validateFile(file)` - Validate PDF file
- `uploadFile(file)` - Upload file with progress
- `reset()` - Reset state

**Validation**:
- File type: PDF only (`application/pdf`)
- File size: ≤20MB

**Usage**:
```javascript
import { useFileUpload } from '@/composables/useFileUpload'

const { progress, uploading, error, uploadFile } = useFileUpload()

const handleUpload = async (file) => {
  try {
    const response = await uploadFile(file)
    console.log('File ID:', response.fileId)
  } catch (err) {
    console.error('Upload failed:', error.value)
  }
}
```

---

## Store Communication Patterns

### Cross-Store Communication
```javascript
// Task creation from PaperModal
// ui.js → tasks.js
const generatePPT = async (paperId, title) => {
  const tasksStore = useTasksStore()
  const uiStore = useUiStore()

  await tasksStore.createTask(paperId, title, true)
  uiStore.showToast('PPT generation started', 'success')
  uiStore.closeModal()
}
```

### Store + Composable Pattern
```javascript
// tasks.js uses useTaskHistory composable
import { useTaskHistory } from '@/composables/useTaskHistory'

const { saveTasksToLocalStorage } = useTaskHistory()

// Save after every task update
const createTask = async (paperId, title, isArxiv) => {
  // ... create task logic
  tasks.value.unshift(newTask)
  saveTasksToLocalStorage(tasks.value)  // Persist
}
```

---

**Last Updated**: 2025-11-17  
**See Also**: [Components](./components.md), [API Services](./api-services.md)
