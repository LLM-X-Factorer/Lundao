# Component Reference

Complete API reference for all Vue components in the project.

---

## Common Components

Reusable UI primitives with no business logic.

### Button.vue

**Location**: `src/components/common/Button.vue`

**Props**:
- `variant`: `'primary' | 'secondary' | 'danger'` (default: `'primary'`)
- `size`: `'small' | 'medium' | 'large'` (default: `'medium'`)
- `disabled`: `boolean` (default: `false`)
- `loading`: `boolean` (default: `false`)

**Slots**:
- `default`: Button content (text + icons)

**Usage**:
```vue
<Button variant="primary" size="medium" @click="handleClick">
  Submit
</Button>

<Button variant="secondary" :loading="uploading">
  <svg>...</svg>
  Upload
</Button>
```

**Styles**:
- Primary: Blue background (`bg-accent`)
- Secondary: White background with border
- Danger: Red background (`bg-error`)
- Loading: Shows spinner, disables interaction

---

### Modal.vue

**Location**: `src/components/common/Modal.vue`

**Props**:
- `open`: `boolean` (required) - Controls modal visibility
- `title`: `string` - Modal header title
- `maxWidth`: `string` (default: `'max-w-4xl'`) - Tailwind max-width class

**Emits**:
- `close`: Emitted when user closes modal (ESC key or backdrop click)

**Slots**:
- `default`: Modal body content

**Features**:
- Backdrop blur (`backdrop-blur-sm`)
- ESC key to close
- Focus trap (Headless UI)
- Smooth transitions (fade + scale)

**Usage**:
```vue
<Modal :open="isOpen" title="Paper Details" @close="isOpen = false">
  <p>Modal content here</p>
</Modal>
```

---

### Toast.vue

**Location**: `src/components/common/Toast.vue`

**Props**:
- `visible`: `boolean` (required) - Show/hide toast
- `message`: `string` (required) - Toast message text
- `type`: `'success' | 'error' | 'info'` (default: `'info'`)

**Emits**:
- `close`: Emitted after 3 seconds or when user clicks close

**Styles**:
- Success: Green background (`bg-success`)
- Error: Red background (`bg-error`)
- Info: Blue background (`bg-accent`)

**Features**:
- Auto-dismiss after 3 seconds
- Slide-in animation from top
- Fixed positioning (top-center)

**Usage**:
```vue
<Toast
  :visible="uiStore.toastVisible"
  :message="uiStore.toastMessage"
  :type="uiStore.toastType"
  @close="uiStore.hideToast"
/>
```

---

### Badge.vue

**Location**: `src/components/common/Badge.vue`

**Props**:
- `status`: `'queued' | 'generating' | 'completed' | 'failed'` (required)

**Slots**:
- `default`: Badge text content

**Styles**:
- `queued`: Yellow background
- `generating`: Blue background
- `completed`: Green background
- `failed`: Red background

**Usage**:
```vue
<Badge :status="task.status">
  {{ task.status === 'queued' ? '排队中' : '生成中' }}
</Badge>
```

---

### Tabs.vue

**Location**: `src/components/common/Tabs.vue`

**Props**:
- `tabs`: `Array<{key: string, label: string}>` (required)
- `activeTab`: `string` (required) - Key of active tab

**Emits**:
- `update:activeTab`: Emitted when tab is clicked

**Features**:
- Keyboard navigation (Arrow keys)
- Active indicator (blue underline)
- Headless UI TabGroup

**Usage**:
```vue
<Tabs
  :tabs="[
    {key: 'daily', label: 'Daily'},
    {key: 'weekly', label: 'Weekly'}
  ]"
  :activeTab="period"
  @update:activeTab="period = $event"
/>
```

---

### Pagination.vue

**Location**: `src/components/common/Pagination.vue`

**Props**:
- `currentPage`: `number` (required)
- `totalPages`: `number` (required)

**Emits**:
- `page-change`: Emitted with new page number

**Features**:
- Previous/Next buttons
- Disabled state for first/last page
- Page number display

**Usage**:
```vue
<Pagination
  :currentPage="papersStore.currentPage"
  :totalPages="papersStore.totalPages"
  @page-change="papersStore.setPage($event)"
/>
```

---

### Watermark.vue

**Location**: `src/components/common/Watermark.vue`

**Props**:
- `text`: `string` (required) - Watermark text
- `opacity`: `number` (default: `0.1`) - Opacity 0-1
- `fontSize`: `string` (default: `'16px'`)
- `color`: `string` (default: `'#000000'`)

**Features**:
- 9-grid distribution (3×3 positions)
- -30° rotation for diagonal aesthetic
- `pointer-events: none` (non-intrusive)
- `user-select: none` (no text selection)

**Usage**:
```vue
<Watermark
  :text="watermarkConfig.text"
  :opacity="watermarkConfig.opacity"
/>
```

---

## Core Components

Business logic components tied to specific features.

### PaperCard.vue

**Location**: `src/components/core/PaperCard.vue`

**Props**:
- `paper`: `Object` (required)
  - `id`: `string`
  - `title`: `string`
  - `authors`: `string[]`
  - `abstract`: `string`
  - `field`: `string`
  - `publicationDate`: `string`

**Events**:
- `@click`: Opens paper modal via `uiStore.openModal(paper.id)`

**Features**:
- Hover lift effect (`hover:-translate-y-1`)
- Truncated abstract (3 lines max)
- Author list (max 3, "et al." for more)

**Usage**:
```vue
<PaperCard :paper="paper" />
```

---

### PaperDiscovery.vue

**Location**: `src/components/core/PaperDiscovery.vue`

**Props**: None (uses `papersStore` directly)

**Features**:
- Tab navigation (Daily/Weekly/Monthly)
- Paper grid (responsive: 1/2/3 columns)
- Pagination
- Loading skeleton (8 cards)
- Empty state

**Store Integration**:
- `papersStore.selectedPeriod` - Current period
- `papersStore.papers` - Filtered papers
- `papersStore.fetchPapers()` - Load papers

---

### PaperModal.vue

**Location**: `src/components/core/PaperModal.vue`

**Props**: None (uses `uiStore` directly)

**Features**:
- Academic layout (title + metadata subtitle)
- Chinese summary (gradient background)
- Two-column innovation grid
- "一键生成PPT" button
- "下载PDF" button
- Loading skeleton
- Stagger animation for innovation cards

**Store Integration**:
- `uiStore.modalOpen` - Modal visibility
- `uiStore.currentPaper` - Paper data
- `uiStore.currentAnalysis` - AI analysis
- `uiStore.analysisLoading` - Loading state

**Layout**:
```
┌─────────────────────────┐
│ Title (20/24px bold)    │
│ Author | Field | Date   │ ← Metadata subtitle
├─────────────────────────┤
│ 📝 Chinese Summary      │ ← Gradient bg
├─────────────────────────┤
│ 💡 Innovation Points    │
│  [Card] [Card]          │ ← 2-column grid
│  [Card] [Card]          │
├─────────────────────────┤
│ [一键生成PPT] [下载PDF] │ ← Actions
└─────────────────────────┘
```

---

### UploadDropzone.vue

**Location**: `src/components/core/UploadDropzone.vue`

**Props**: None (self-contained)

**Features**:
- Drag-and-drop upload
- Click to select file
- File type validation (PDF only)
- File size validation (≤20MB)
- Upload progress (0-100%)
- Error messages
- Auto-create PPT task after upload

**Composables**:
- `useFileUpload()` - Upload state + validation
- `useTasksStore()` - Task creation
- `useUiStore()` - Toast notifications

**Important Fix** (Feature #006):
- File input hidden after file selection (`v-if="!selectedFile"`)
- Prevents transparent input from blocking "Upload" button clicks

**Usage**:
```vue
<UploadDropzone />
```

---

### TaskItem.vue

**Location**: `src/components/core/TaskItem.vue`

**Props**:
- `task`: `Object` (required)
  - `id`: `string`
  - `paperTitle`: `string`
  - `status`: `'queued' | 'generating' | 'completed' | 'failed'`
  - `progress`: `number | null`
  - `downloadUrl`: `string | null`
  - `errorMessage`: `string | null`

**Emits**:
- `retry`: Emitted when retry button clicked (failed tasks)
- `delete`: Emitted when delete button clicked

**Features**:
- Status-based rendering
- Progress bar (generating status)
- Preview button (completed tasks)
- Download button (completed tasks)
- Retry button (failed tasks)

**Usage**:
```vue
<TaskItem
  :task="task"
  @retry="tasksStore.createTask(...)"
  @delete="tasksStore.deleteTask(task.id)"
/>
```

---

### TaskHistory.vue

**Location**: `src/components/core/TaskHistory.vue`

**Props**: None (uses `tasksStore` directly)

**Features**:
- Scrollable task list
- Empty state ("暂无任务")
- Reverse chronological order
- Auto-loading from localStorage

**Store Integration**:
- `tasksStore.tasks` - Task array
- `tasksStore.deleteTask()` - Remove task

---

### PPTPreviewModal.vue

**Location**: `src/components/core/PPTPreviewModal.vue`

**Props**: None (uses `uiStore` directly)

**Features**:
- Image-based slide carousel
- Left/Right navigation buttons
- Keyboard shortcuts (← → Home End Esc)
- Watermark overlay
- Fixed-height layout (600px)
- Page counter (第 X / Y 张)
- Loading states
- Error handling with retry

**Store Integration**:
- `uiStore.pptPreviewOpen` - Modal visibility
- `uiStore.currentPPTContent` - PPT metadata
- `uiStore.openPPTPreview(taskId)` - Load content

**Keyboard Shortcuts**:
- `→`: Next slide
- `←`: Previous slide
- `Home`: First slide
- `End`: Last slide
- `Esc`: Close modal

**Layout**:
```
┌────────────────────────────┐
│ Header: Paper Title + Close│
├────────────────────────────┤
│ Slide Container (600px)    │
│  ┌──────────────────────┐  │
│  │  Slide Image         │  │
│  │  (fit within)        │  │
│  └──────────────────────┘  │
│  Watermark Overlay         │
├────────────────────────────┤
│ Footer: [<] 第 3/14 张 [>] │
└────────────────────────────┘
```

---

## Component Usage Patterns

### Modal Pattern
```vue
<!-- In component -->
<script setup>
import { useUiStore } from '@/stores/ui'
const uiStore = useUiStore()

const openPaperDetails = (paperId) => {
  uiStore.openModal(paperId)  // Triggers API call + opens modal
}
</script>

<template>
  <!-- Trigger -->
  <button @click="openPaperDetails(paper.id)">View Details</button>

  <!-- Modal (in App.vue or HomeView.vue) -->
  <PaperModal />  <!-- Controlled by uiStore.modalOpen -->
</template>
```

### Task Workflow
```vue
<script setup>
import { useTasksStore } from '@/stores/tasks'
const tasksStore = useTasksStore()

const generatePPT = async (paperId, title) => {
  await tasksStore.createTask(paperId, title, true)
  // Task appears in TaskHistory
  // Polling starts automatically if not already active
}
</script>
```

### Upload + Task Creation
```vue
<!-- UploadDropzone.vue (simplified) -->
<script setup>
const handleUpload = async () => {
  const response = await uploadFile(selectedFile.value)
  
  // Create task after upload
  await tasksStore.createTask(
    response.paperId,  // or response.fileId
    `上传论文: ${fileName}`,
    false  // isArxiv = false for uploads
  )
  
  // Show success toast
  uiStore.showToast('上传成功！正在生成PPT...', 'success')
}
</script>
```

---

**Last Updated**: 2025-11-17  
**See Also**: [State Management](./state-management.md), [Design System](./design-system.md)
