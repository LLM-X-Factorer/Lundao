# Technology Research & Decisions

**Feature**: 论导Lite MVP Frontend
**Date**: 2025-10-14
**Phase**: 0 - Research

## Overview

This document consolidates research findings and technology decisions for implementing the 论导Lite MVP frontend. All decisions align with the project constitution and prioritize development velocity, maintainability, and adherence to the design system.

## 1. Vue 3 + Vite Project Initialization

### Decision
Use `npm create vite@latest` with the official Vue template as the project foundation.

###Rationale
- **Official tooling**: Vite is the officially recommended build tool for Vue 3
- **Fast HMR**: Sub-50ms hot module replacement improves developer experience
- **Optimized builds**: Native ES modules in dev, optimized chunks in production
- **Zero config**: Sensible defaults align with our simple SPA requirements
- **Tree shaking**: Automatic dead code elimination helps meet <1.5s FCP target

### Alternatives Considered
- **Vue CLI**: Rejected - Webpack-based, slower, being phased out by Vue team
- **Nuxt 3**: Rejected - SSR overhead unnecessary for client-side-only SPA
- **Custom Vite config**: Rejected - Template provides everything needed

### Implementation Notes
```bash
npm create vite@latest lundao-lite-frontend -- --template vue
cd lundao-lite-frontend
npm install
```

## 2. Tailwind CSS Integration

### Decision
Install Tailwind CSS via PostCSS with custom configuration file containing design system tokens.

### Rationale
- **Constitution mandate**: Required by Technical Standards section
- **Design system tokens**: Can directly encode color palette, typography scale, spacing values
- **Utility-first**: Enables rapid UI development without CSS conflicts
- **PurgeCSS**: Automatically removes unused styles for optimal bundle size
- **JIT mode**: Just-in-Time compilation generates only needed utilities

### Implementation Strategy
1. Install dependencies: `tailwindcss`, `postcss`, `autoprefixer`
2. Generate config: `npx tailwindcss init -p`
3. Customize `tailwind.config.js` with design system tokens:
   ```javascript
   module.exports = {
     theme: {
       extend: {
         colors: {
           primary: '#FFFFFF',
           secondary: '#F8F9FA',
           border: '#E9ECEF',
           'text-primary': '#212529',
           'text-secondary': '#6C757D',
           accent: '#3A57E8',
           success: '#198754',
           error: '#DC3545'
         },
         fontFamily: {
           sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif']
         },
         fontSize: {
           h1: '28px',
           h2: '22px',
           h3: '18px',
           body: '16px',
           secondary: '14px'
         },
         spacing: {
           // 8px grid system
         },
         borderRadius: {
           button: '6px',
           card: '1px',
           modal: '12px'
         }
       }
     }
   }
   ```
4. Import in `src/main.js` or `src/assets/styles/main.css`

### Alternatives Considered
- **CSS Modules**: Rejected - More boilerplate, harder to enforce design system
- **Styled Components**: Rejected - Runtime overhead, not idiomatic for Vue
- **Plain CSS/SCSS**: Rejected - Design system drift risk, manual class management

## 3. Headless UI Setup

### Decision
Install `@headlessui/vue` for Tab, Dialog (Modal), and Transition components.

### Rationale
- **Constitution mandate**: Required by Technical Standards
- **Accessibility**: WCAG AA compliant out-of-the-box (keyboard nav, ARIA, focus management)
- **Unstyled**: Complete control over visual design with Tailwind
- **Vue 3 native**: Built specifically for Vue 3 Composition API
- **Transition support**: Built-in animation primitives for smooth interactions

### Components Needed
- **TabGroup/TabList/Tab/TabPanels/TabPanel**: For time period tabs (Daily/Weekly/Monthly)
- **Dialog/DialogPanel/DialogTitle**: For paper detail modal
- **TransitionRoot/TransitionChild**: For modal fade-in/out, toast animations
- **Menu** (optional): For future dropdown actions if needed

### Implementation Notes
```bash
npm install @headlessui/vue
```

Usage pattern:
```vue
<script setup>
import { Dialog, DialogPanel, TransitionRoot } from '@headlessui/vue'
</script>
```

### Alternatives Considered
- **Element Plus**: Rejected - Opinionated styles conflict with design system
- **Naive UI**: Rejected - Same styling conflicts
- **Custom components**: Rejected - Accessibility implementation complexity

## 4. Pinia Store Architecture

### Decision
Create three separate Pinia stores: `papers.js`, `tasks.js`, and `ui.js`.

### Rationale
- **Constitution mandate**: Required state management solution
- **Composition API native**: Perfect fit for Vue 3 `<script setup>` syntax
- **Lightweight**: No mutations, simpler than Vuex
- **DevTools**: Vue DevTools integration for debugging
- **TypeScript-friendly**: Better type inference than Vuex (even without TS)
- **Domain separation**: Independent stores prevent tight coupling

### Store Responsibilities

**papers.js**:
- Fetched arXiv papers by time period
- Current pagination state (page, limit)
- Loading/error states for paper fetching

**tasks.js**:
- PPT generation task list (from localStorage + API)
- Polling interval management
- Task CRUD operations
- Status update logic

**ui.js**:
- Active modal state (open/closed, current paper)
- Toast notifications queue
- Global loading states
- Active tab selection

### Implementation Pattern
```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  const pollingInterval = ref(null)

  const activeTasks = computed(() =>
    tasks.value.filter(t => t.status !== 'completed')
  )

  function startPolling() { /* ... */ }
  function stopPolling() { /* ... */ }

  return { tasks, activeTasks, startPolling, stopPolling }
})
```

### Alternatives Considered
- **Vuex**: Rejected - More verbose, mutations add boilerplate
- **Provide/Inject**: Rejected - No DevTools, manual reactivity management
- **Global refs**: Rejected - No organization, testing difficulties

## 5. Axios Configuration

### Decision
Create centralized Axios instance in `src/api/index.js` with request/response interceptors.

### Rationale
- **Constitution mandate**: Required HTTP client
- **Interceptors**: Global error handling, loading state management
- **Progress tracking**: Built-in support for upload progress (onUploadProgress)
- **Cancellation**: AbortController support for polling cleanup
- **Widely adopted**: Extensive Vue community experience/examples

### Configuration Strategy
```javascript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 60000, // 60s for AI analysis
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor: add loading state
apiClient.interceptors.request.use(config => {
  // Could dispatch to store or emit event
  return config
})

// Response interceptor: handle errors globally
apiClient.interceptors.response.use(
  response => response,
  error => {
    // Show toast, log error, etc.
    return Promise.reject(error)
  }
)

export default apiClient
```

### Service Module Pattern
Separate files per domain:
- `paperService.js`: `fetchArxivPapers()`, `analyzePaper()`
- `uploadService.js`: `uploadPDF(file, onProgress)`
- `taskService.js`: `createTask()`, `pollTaskStatus()`, `downloadPPT()`

### Alternatives Considered
- **Fetch API**: Rejected - No interceptors, manual timeout, progress tracking complex
- **ky**: Rejected - Smaller API surface but less Vue ecosystem examples

## 6. localStorage Strategy

### Decision
JSON serialization with 5MB capacity management and automatic cleanup of oldest completed tasks.

### Rationale
- **Constitution mandate**: Required for zero-friction (no server-side user state)
- **Persistence**: Tasks survive browser close/reopen
- **Synchronous**: Immediate writes, no async complexity
- **Universal**: Works in all target browsers

### Data Structure
```javascript
{
  "lundao_tasks": [
    {
      "id": "task-uuid-1",
      "paperId": "arxiv-2301.00000",
      "paperTitle": "Paper Title",
      "status": "completed",
      "createdAt": "2025-10-14T10:30:00Z",
      "downloadUrl": "https://...",
      "errorMessage": null
    }
  ],
  "lundao_meta": {
    "version": "1.0",
    "lastCleanup": "2025-10-14T10:00:00Z"
  }
}
```

### Capacity Management
- Monitor total size: `JSON.stringify(data).length * 2` (UTF-16 bytes)
- Trigger cleanup at 4MB (80% of 5MB limit)
- Remove oldest "completed" tasks first
- Keep failed/generating tasks (user may want to retry/monitor)

### Implementation (Composable)
```javascript
// composables/useTaskHistory.js
export function useTaskHistory() {
  const STORAGE_KEY = 'lundao_tasks'
  const MAX_SIZE_MB = 4

  const getTasks = () => {
    const data = localStorage.getItem(STORAGE_KEY)
    return data ? JSON.parse(data) : []
  }

  const saveTasks = (tasks) => {
    // Check size, cleanup if needed
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks))
  }

  const addTask = (task) => { /* ... */ }
  const updateTask = (id, updates) => { /* ... */ }
  const deleteTask = (id) => { /* ... */ }

  return { getTasks, saveTasks, addTask, updateTask, deleteTask }
}
```

### Alternatives Considered
- **IndexedDB**: Rejected - Async API overkill for simple key-value needs
- **SessionStorage**: Rejected - Clears on tab close, breaks persistence requirement
- **Cookies**: Rejected - 4KB limit too restrictive

## 7. Polling Pattern

### Decision
Use `setInterval` with cleanup on component unmount, managed by Pinia store action.

### Rationale
- **Simple**: Native JS, no external dependencies
- **Predictable**: Fires every 5 seconds regardless of request duration
- **Controllable**: Easy to start/stop based on active tasks
- **Testable**: Can mock/spy on setInterval in tests

### Implementation Strategy
```javascript
// stores/tasks.js
export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  let pollingIntervalId = null

  const startPolling = () => {
    if (pollingIntervalId) return // Already polling

    pollingIntervalId = setInterval(async () => {
      const activeTasks = tasks.value.filter(
        t => t.status === 'queued' || t.status === 'generating'
      )

      if (activeTasks.length === 0) {
        stopPolling()
        return
      }

      for (const task of activeTasks) {
        const status = await taskService.pollTaskStatus(task.id)
        updateTaskStatus(task.id, status)
      }
    }, 5000) // 5 seconds
  }

  const stopPolling = () => {
    if (pollingIntervalId) {
      clearInterval(pollingIntervalId)
      pollingIntervalId = null
    }
  }

  return { startPolling, stopPolling }
})
```

### Lifecycle Management
- Start polling: When task created OR when component mounts with existing active tasks
- Stop polling: When no active tasks remain OR component unmounts
- Cleanup: Use Vue's `onUnmounted` hook to ensure interval cleared

### Alternatives Considered
- **setTimeout recursive**: Rejected - More complex, same result
- **WebSockets**: Rejected - Out of scope (constitution: "using polling instead")
- **Long polling**: Rejected - Server-side complexity, same client experience

## 8. File Upload Pattern

### Decision
Use FormData with Axios progress tracking via `onUploadProgress` config option.

### Rationale
- **Browser native**: FormData handles multipart/form-data encoding
- **Progress events**: Axios exposes XMLHttpRequest.upload.onprogress
- **Validation**: Can check file.type === 'application/pdf' before upload
- **Size limits**: Can enforce 20MB limit client-side

### Implementation Pattern
```javascript
// api/uploadService.js
export async function uploadPDF(file, onProgress) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/upload_pdf', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      )
      onProgress(percentCompleted)
    }
  })

  return response.data
}
```

### Validation
```javascript
// composables/useFileUpload.js
export function useFileUpload() {
  const uploadFile = async (file) => {
    // Validate type
    if (file.type !== 'application/pdf') {
      throw new Error('Only PDF files are allowed')
    }

    // Validate size
    const maxSize = 20 * 1024 * 1024 // 20MB
    if (file.size > maxSize) {
      throw new Error('File size exceeds 20MB limit')
    }

    // Upload with progress
    const progress = ref(0)
    const data = await uploadPDF(file, (percent) => {
      progress.value = percent
    })

    return { data, progress }
  }

  return { uploadFile }
}
```

### Alternatives Considered
- **Base64 encoding**: Rejected - 33% overhead, no progress tracking
- **Chunked upload**: Rejected - Unnecessary complexity for <20MB files
- **Direct S3 upload**: Rejected - Requires presigned URLs, more moving parts

## 9. Chinese Font Loading

### Decision
Load Inter and Noto Sans SC from Google Fonts CDN with font-display: swap.

### Rationale
- **Constitution mandate**: Inter (English) + Noto Sans SC (Chinese) required
- **CDN benefits**: Browser caching, global edge network, automatic subsetting
- **font-display swap**: Shows fallback font immediately, swaps when custom loads
- **Subset support**: Google Fonts auto-serves Chinese subset based on Accept-Language

### Implementation
```html
<!-- index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600&display=swap" rel="stylesheet">
```

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif']
      }
    }
  }
}
```

### Font Weights
- Regular (400): Body text
- Medium (500): Buttons, labels
- Semibold (600): Headings

### Alternatives Considered
- **Self-hosted fonts**: Rejected - CDN caching benefits outweigh control
- **System fonts only**: Rejected - Constitution explicitly requires Inter + Noto Sans SC
- **Variable fonts**: Rejected - Larger file size for minimal weight flexibility

## 10. Animation Strategy

### Decision
Use Tailwind transition utilities for simple state changes, HeadlessUI Transition component for complex animations.

### Rationale
- **Constitution requirement**: "Smooth transitions (no jarring state changes)"
- **Performance**: CSS transitions are GPU-accelerated
- **Consistency**: Tailwind utilities enforce uniform timing functions
- **Accessibility**: HeadlessUI respects prefers-reduced-motion

### Tailwind Utilities
```vue
<!-- Button hover -->
<button class="transition-all duration-150 hover:shadow-lg">

<!-- Loading spinner -->
<div class="animate-spin">

<!-- Fade in -->
<div class="transition-opacity duration-300 opacity-100">
```

### HeadlessUI Transitions
```vue
<!-- Modal enter/leave -->
<TransitionRoot :show="isOpen">
  <Dialog>
    <TransitionChild
      enter="duration-300 ease-out"
      enter-from="opacity-0"
      enter-to="opacity-100"
      leave="duration-200 ease-in"
      leave-from="opacity-100"
      leave-to="opacity-0"
    >
      <div class="fixed inset-0 bg-black bg-opacity-25" />
    </TransitionChild>
  </Dialog>
</TransitionRoot>
```

### Target Frame Rate
- **60fps**: Constitution requirement for "smooth" animations
- CSS transitions/transforms achieve this automatically
- Avoid JavaScript-driven animations (requestAnimationFrame overhead)

### Alternatives Considered
- **GSAP**: Rejected - Overkill for simple state transitions
- **Framer Motion**: Rejected - React-only
- **Vue Transition component**: Considered but HeadlessUI provides better abstraction

## Summary

All technology decisions prioritize:
1. **Constitutional compliance**: Mandatory tech stack (Vue 3, Vite, Tailwind, Headless UI, Pinia, Axios)
2. **Performance**: <1.5s FCP, <100ms interaction response
3. **Developer experience**: Fast HMR, minimal config, excellent tooling
4. **Maintainability**: Clear separation of concerns, established patterns
5. **Design system fidelity**: 1:1 implementation of specified colors/typography/spacing

## Next Phase

Proceed to Phase 1: Design & Contracts
- Define data models for Paper, AIAnalysis, PPTTask entities
- Specify API contracts for all 5 backend endpoints
- Create quickstart guide for local development setup
