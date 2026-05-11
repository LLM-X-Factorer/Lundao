# System Architecture

## Overview

Lundao-Lite is a single-page Vue 3 application for academic researchers to discover papers, get AI analysis in Chinese, and generate presentation slides.

### Key Characteristics
- **Single-Page Application**: No router, all features on root route `/`
- **Mock-First Development**: Complete frontend testing without backend
- **Component-Based**: Reusable common + domain-specific core components
- **Centralized State**: Pinia stores for papers, tasks, and UI
- **API Abstraction**: Service layer with environment-based routing

---

## Tech Stack

### Core Framework
- **Vue 3.5**: Composition API with `<script setup>` syntax
- **Vite 5.4**: Build tool with HMR (Hot Module Replacement)
- **Pinia 2.3**: State management (Vuex successor)

### UI & Styling  
- **Tailwind CSS 3.4**: Utility-first CSS with design system tokens
- **Headless UI 1.7**: Accessible unstyled components (Dialog, Tabs, etc.)
- **Google Fonts**: Inter (English) + Noto Sans SC (Chinese)

### HTTP & Data
- **Axios 1.12**: HTTP client with interceptors
- **localStorage**: Task history persistence (v2 format with versioning)

### PPT Preview Stack
- **marked 11.0**: Markdown→HTML parser
- **marked-katex-extension 5.0**: LaTeX math formulas
- **KaTeX 0.16.9**: Math rendering (340KB + fonts)
- **highlight.js 11.9.0**: Code syntax highlighting (7 languages)
- **DOMPurify 3.0.6**: XSS protection

### Development Tools
- **ESLint**: Code quality (0 errors, 0 warnings)
- **Prettier**: Code formatting (implied via ESLint --fix)
- **Node.js**: v18.x+ or v20.x+
- **npm**: v9.x+

---

## Architecture Patterns

### 1. Component Hierarchy

```
App.vue
└── HomeView.vue
    ├── Header (inline)
    ├── Main Content
    │   ├── UploadDropzone
    │   ├── PaperDiscovery
    │   │   ├── Tabs (period selection)
    │   │   ├── PaperCard[] (grid)
    │   │   └── Pagination
    │   └── TaskHistory
    │       └── TaskItem[]
    ├── Footer (inline)
    └── Modals (overlay)
        ├── PaperModal
        ├── PPTPreviewModal
        └── Toast
```

### 2. State Management Pattern

```
┌──────────────────────────────────────┐
│  View Components (HomeView.vue)      │
│  - UploadDropzone                    │
│  - PaperDiscovery                    │
│  - TaskHistory                       │
└──────────────┬───────────────────────┘
               │ import stores
               ▼
┌──────────────────────────────────────┐
│  Pinia Stores                        │
│  ┌──────────┐ ┌────────┐ ┌─────────┐│
│  │ papers   │ │ tasks  │ │   ui    ││
│  │ (papers) │ │(tasks) │ │(modals) ││
│  └────┬─────┘ └───┬────┘ └────┬────┘│
└───────┼───────────┼──────────── ┼────┘
        │           │             │
        │ call      │ call        │ call
        ▼           ▼             ▼
┌──────────────────────────────────────┐
│  API Services                        │
│  ┌──────────┐ ┌────────┐ ┌─────────┐│
│  │paperSvc  │ │taskSvc │ │uploadSvc││
│  └────┬─────┘ └───┬────┘ └────┬────┘│
└───────┼───────────┼──────────── ┼────┘
        │           │             │
        ▼           ▼             ▼
    ┌───────────────────────────────┐
    │  Mock Router (if enabled)     │
    │  VITE_USE_MOCK_DATA=true      │
    └───────────────────────────────┘
            │                  │
    ┌───────┴───────┐   ┌──────┴────────┐
    │ Mock Services │   │  Real Backend │
    │ (delay + data)│   │  (Axios HTTP) │
    └───────────────┘   └───────────────┘
```

### 3. File Structure Convention

```
src/
├── api/                     # API service layer
│   ├── index.js             # Axios client + interceptors
│   ├── paperService.js      # Paper discovery & analysis
│   ├── uploadService.js     # File upload with progress
│   ├── taskService.js       # PPT task creation & polling
│   └── pptContentService.js # PPT content fetching
│
├── components/
│   ├── common/              # Reusable UI primitives
│   │   ├── Button.vue       # Variant-based button
│   │   ├── Modal.vue        # Headless UI Dialog wrapper
│   │   ├── Toast.vue        # Auto-dismiss notifications
│   │   ├── Badge.vue        # Status badges (queued/generating/completed/failed)
│   │   ├── Tabs.vue         # Headless UI TabGroup wrapper
│   │   ├── Pagination.vue   # Previous/Next navigation
│   │   └── Watermark.vue    # 9-grid watermark overlay
│   │
│   └── core/                # Business logic components
│       ├── PaperCard.vue        # Paper preview card
│       ├── PaperDiscovery.vue   # Paper grid + tabs + pagination
│       ├── PaperModal.vue       # Paper detail modal
│       ├── UploadDropzone.vue   # Drag-drop PDF upload
│       ├── TaskItem.vue         # Single task display
│       ├── TaskHistory.vue      # Task list container
│       └── PPTPreviewModal.vue  # Full PPT preview
│
├── stores/                  # Pinia state management
│   ├── papers.js            # Paper discovery state
│   ├── tasks.js             # Task history + polling
│   └── ui.js                # Modal + toast state
│
├── composables/             # Reusable composition functions
│   ├── useTaskHistory.js    # localStorage CRUD
│   ├── useTaskPolling.js    # 5s polling interval
│   └── useFileUpload.js     # Upload state + validation
│
├── mocks/                   # Mock data & services
│   ├── paperData.js         # 24 papers (Daily/Weekly/Monthly)
│   ├── taskData.js          # Historical tasks (3 tasks)
│   ├── pptContentData.js    # PPT metadata (8 papers)
│   ├── taskService.js       # Mock task creation + polling
│   └── utils.js             # Mock helpers (delay, ID generation)
│
├── utils/                   # General utilities
│   └── pptRenderer.js       # Markdown→HTML pipeline (marked + KaTeX + highlight.js)
│
├── config/                  # Configuration files
│   ├── pptImages.js         # PPT image URL generation
│   └── watermark.js         # Watermark settings (env-based)
│
├── assets/
│   └── styles/
│       └── main.css         # Tailwind directives + global styles
│
├── views/
│   └── HomeView.vue         # Main (only) view
│
├── App.vue                  # Root component
└── main.js                  # App entry point
```

---

## Build Configuration

### Vite Config (`vite.config.js`)
```javascript
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Automatic code splitting by Rollup
        }
      }
    }
  }
})
```

### Tailwind Config (`tailwind.config.js`)
- Custom color palette (primary-bg, accent, error, etc.)
- Custom gradient: `bg-gradient-summary` (blue-purple 45deg)
- Font family: Inter, Noto Sans SC
- 8px grid spacing system

### ESLint Config
```javascript
rules: {
  'vue/multi-word-component-names': 'off',
  'vue/require-default-prop': 'off'
}
```

---

## Environment Variables

### Development (`.env.development`)
```env
VITE_API_BASE_URL=http://localhost:3000/api
VITE_USE_MOCK_DATA=true
VITE_WATERMARK_ENABLED=true
VITE_WATERMARK_TEXT="论导Lite 预览版 - lundao.com"
VITE_WATERMARK_OPACITY=0.08
```

### Production (`.env.production`)
```env
VITE_API_BASE_URL=https://api.lundao.com/api
VITE_USE_MOCK_DATA=false
VITE_WATERMARK_ENABLED=true
VITE_WATERMARK_TEXT="论导Lite - lundao.com"
VITE_WATERMARK_OPACITY=0.1
```

---

## Build Output

### Production Build Stats
```
dist/
├── index.html          0.84 KB  →  0.51 KB (gzip)
├── assets/
│   ├── index.js      240.80 KB → 88.50 KB (gzip)
│   └── index.css      25.57 KB →  5.34 KB (gzip)
├── ppt-images/        55 MB   (120+ PNG screenshots)
└── ppt-files/        191 MB   (8 .pptx files)

Total: 245 MB
Build Time: 2.42s
```

### Bundle Composition
- **Vue 3 + Pinia**: ~50 KB (gzip)
- **Axios**: ~15 KB (gzip)
- **Tailwind CSS**: 5.34 KB (gzip, purged)
- **marked + KaTeX + highlight.js**: ~20 KB (gzip)
- **App code**: ~3 KB (gzip)

---

## Performance Characteristics

### Load Time (Estimated @ 4G)
- **First Contentful Paint**: < 1s
- **Time to Interactive**: < 2s
- **JS Execution**: ~200ms (88.50 KB gzip)
- **CSS Parse**: ~20ms (5.34 KB gzip)

### Runtime Performance
- **Task Polling**: 5s interval (Promise.allSettled)
- **localStorage Size**: ~5 MB quota (auto-prune on overflow)
- **Watermark Rendering**: CSS-based (GPU-accelerated)

---

## Security Considerations

### XSS Protection
- **DOMPurify**: Sanitizes all HTML content
- **KaTeX MathML Whitelist**: Allows safe math tags only
- **Content Security Policy**: Recommended for production

### Data Persistence
- **localStorage Versioning**: Version 2 format (backward compat fallback)
- **Auto-expiration**: Tasks >24 hours removed on mount
- **Quota Handling**: Auto-prune oldest tasks on QuotaExceededError

---

## Deployment Architecture

### Static Hosting (Recommended)
```
┌─────────────┐
│   CDN       │ ← ppt-images/, ppt-files/
└─────────────┘
       │
       ▼
┌─────────────┐
│  Nginx /    │ ← dist/ (SPA)
│  Vercel     │   ├── index.html
│  Netlify    │   └── assets/
└─────────────┘
       │
       ▼
┌─────────────┐
│  Backend    │ ← VITE_API_BASE_URL
│  API Server │   (when VITE_USE_MOCK_DATA=false)
└─────────────┘
```

### SPA Routing Config (Nginx)
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

---

**Last Updated**: 2025-11-17  
**See Also**: [Components](./components.md), [State Management](./state-management.md), [Design System](./design-system.md)
