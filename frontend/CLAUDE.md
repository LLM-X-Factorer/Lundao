# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

论导Lite (Lundao-Lite) is an AI-powered tool for Chinese academic researchers to discover papers, get AI analysis in Chinese, and generate presentation slides within 3 minutes—without registration. This is the Vue 3 frontend for the MVP.

**Implementation Status**: ✅ Core MVP complete + ✅ Feature #002 complete + ✅ Feature #003 complete + ✅ Feature #004 complete + ✅ Feature #005 complete 🎉

- **Completed**: All MVP phases + 4 major enhancements = ~168 total tasks
  - ✅ **Feature #001**: MVP Frontend (78 tasks, 7 phases)
  - ✅ **Feature #002**: Paper Modal Enhancement (40 tasks, 6 phases)
  - ✅ **Feature #003**: PPT Task Mock System (18 tasks, 5 phases)
  - ✅ **Feature #004**: PPT Preview (20 tasks, 4 phases) + UX improvements
  - ✅ **Feature #005**: PPT Content Intelligence (11 tasks, content enhancement + LaTeX fixes)
- **Current Branch**: `003-ppt-task-mock` (testing completed features before merge)
- **Main Branch**: `main` (stable, ready for feature merges)
- **Stack**: Vite 5.0 + Vue 3.5 + Pinia 2.3 + Axios 1.12 + Tailwind 3.4 + Headless UI 1.7
- **Markdown Stack**: marked 11.0 + marked-katex-extension 5.0 + KaTeX 0.16.9 + highlight.js 11.9.0 + DOMPurify 3.0.6
- **Build Status**: ✅ Production build passing (1.56s, 197 KB gzipped JS, 22.17 KB gzipped CSS)
- **Lint Status**: ✅ ESLint passing with zero errors/warnings

**🎉 Recent Features**:

**Feature #005: PPT Content Intelligence** (✅ Complete - All 11 Tasks)
- **Status**: ✅ Content enhancement + comprehensive LaTeX rendering fixes complete
- **Goal**: Enhance PPT content quality with academic depth, add mathematical formulas, and fix all LaTeX rendering issues
- **Spec**: `specs/005-ppt-content-intelligence/`
- **Branch**: `003-ppt-task-mock` (ready for merge)
- **Key Accomplishments**:
  - ✅ **Content Enhancement**: Added 11 formulas to demo-default (1→11, +1000% increase)
  - ✅ **Page Expansion**: Expanded Pages 3-9 with 3-5x more detail while maintaining 5×5 rule
  - ✅ **LaTeX Fixes**: Fixed 16 formula positions with comprehensive double escaping
  - ✅ **Academic Standards**: All content follows NeurIPS/ICML presentation standards
- **Critical LaTeX Fix**: JavaScript template strings require double escaping for all LaTeX commands (`\` → `\\`)
  - Fixed commands: `\text`, `\frac`, `\theta`, `\tau`, `\arg\min`, `\left`, `\right`, `\mid`, `\sum`, `\prod`, `\ln`, `\lim`, `\to`, `\begin`, `\end`, `\quad`, `\bigcup`, `\cdot`, `\log`, `\hat`
  - Example: `$$\text{Conf}(r) = \frac{1}{1 + e^{-\theta}}$$` → `$$\\text{Conf}(r) = \\frac{1}{1 + e^{-\\theta}}$$`
- **Documentation**:
  - `CONTENT-ENHANCEMENT-ANALYSIS.md` - Gap analysis and strategy
  - `ENHANCEMENT-COMPLETION-SUMMARY.md` - Results summary (1→11 formulas, +1000%)
  - `LATEX-FIX-SUMMARY.md` - Complete fix documentation (16 formulas, 25+ LaTeX commands)
  - `GENERATION-GUIDE.md` - Future PPT content creation guide

**Feature #004: PPT Content Preview** (✅ Complete - All 20 Tasks + UX Improvements)
- **Status**: ✅ All 4 phases complete (T001-T020) + UX refinements + Universal demo PPT
- **Goal**: Enable PPT content preview with LaTeX formulas, code highlighting, watermark protection, and seamless demo mode
- **Spec**: `specs/004-ppt-preview-feature/spec.md`
- **Branch**: `003-ppt-task-mock` (ready for merge)
- **Phases Completed**:
  - ✅ Phase 1 (T001-T004): Dependencies, mock data, rendering utilities, API service
  - ✅ Phase 2 (T005-T009): Store extension, PPTPreviewModal component, slide navigation, TaskItem integration
  - ✅ Phase 3 (T010-T016): Keyboard navigation, styling, error handling, caching, **watermark system**
  - ✅ Phase 4 (T017-T020): Functional testing, security audit, performance testing, documentation
- **UX Improvements** (Post-completion refinements):
  - ✅ Fixed button icon alignment (preview button + navigation buttons)
  - ✅ Consistent slide heights (600px fixed container + scrollable content)
  - ✅ Smooth scrolling with custom scrollbar styling
  - ✅ No layout jumping during slide navigation

**Feature #003: PPT Task Mock System**
- **Status**: ✅ Complete - All 18 tasks implemented
- **Goal**: Enable complete frontend development without backend dependency through realistic PPT task simulation
- **Spec**: `specs/003-ppt-task-mock-system/spec.md`
- **Branch**: `003-ppt-task-mock`

**Feature #002: Paper Modal Enhancement**
- **Status**: ✅ Complete - All 40 tasks implemented
- **Goal**: Transform paper detail modal with modern split-pane layout, enhanced innovation points display
- **Spec**: `specs/002-paper-modal-enhancement/spec.md`
- **Branch**: `002-paper-modal-enhancement` (ready for merge)

## Constitutional Principles (Non-Negotiable)

All code MUST comply with `.specify/memory/constitution.md`. Key rules:

1. **Tool-First Philosophy**: NO user accounts, NO gamification, NO engagement mechanics
2. **Single-Page Minimalism**: All features on root route `/` only (modals/overlays permitted)
3. **Zero Friction**: NO authentication gates anywhere
4. **Value-First Design**: AI insights (Chinese summary, innovation points) displayed prominently before metadata
5. **Aesthetics as Trust**: Strict design system adherence (8px grid, specific colors, Inter + Noto Sans SC fonts)

**Enforcement**: Any PR that violates principles I-V requires explicit constitutional amendment justification.

## Mandatory Tech Stack

- **Framework**: Vue 3 with Composition API (`<script setup>` syntax REQUIRED)
- **Build Tool**: Vite
- **CSS**: Tailwind CSS (with design system tokens)
- **Components**: Headless UI (for accessibility)
- **State**: Pinia (3 stores: `papers`, `tasks`, `ui`)
- **HTTP**: Axios (centralized in `api/index.js`)

**Do NOT** substitute alternatives without constitutional amendment.

## Current Development Status

**✅ Completed Implementation** (Phases 1-5):

**Phase 1-2: Foundation**
- ✅ Vite + Vue 3 project initialized with all dependencies
- ✅ Tailwind CSS configured with full design system tokens
- ✅ ESLint configured with Vue plugin and project rules
- ✅ Axios API client with interceptors and 3 service modules
- ✅ Pinia stores: papers, tasks, ui (all fully implemented)
- ✅ Composables: useTaskHistory, useTaskPolling, useFileUpload
- ✅ Environment configuration (.env.development, .env.production)

**Phase 3: US1 - Paper Discovery & Analysis (P1)**
- ✅ Common components: Button, Badge, Modal, Tabs, Toast, Pagination (6 components)
- ✅ Core components: PaperCard, PaperDiscovery, PaperModal (3 components)
- ✅ HomeView and App.vue integration with full layout
- ✅ Analysis retry logic for 202 pending responses (up to 3 retries)
- ✅ Loading skeletons, error states, empty states

**Phase 4: US2 - Upload Feature (P2)**
- ✅ UploadDropzone component with drag-drop support
- ✅ PDF validation (type check, 20MB size limit)
- ✅ Upload progress tracking with status messages
- ✅ Error handling and user feedback
- ✅ Integration into HomeView

**Phase 5: US3 - PPT Generation & Task Tracking (P1)**
- ✅ TaskItem component with status-based rendering
- ✅ TaskHistory component with auto-loading and empty states
- ✅ Task polling system (5s interval, auto-start/stop)
- ✅ localStorage persistence with lifecycle management
- ✅ Retry functionality for failed tasks
- ✅ Download buttons for completed tasks
- ✅ Integration into HomeView

**📋 Remaining** (Optional Polish):
- Phase 6: Additional pagination features (basic pagination already integrated)
- Phase 7: Advanced animations, edge case handling, performance optimizations

**✅ Feature #002: Paper Modal Enhancement** (Complete)

**Branch**: `002-paper-modal-enhancement`
**Status**: All 6 phases complete (40/40 tasks) + UX refinements

This feature enhances the paper detail modal (PaperModal.vue) with modern design, academic layout, and improved UX:

**Implemented Features** (All 6 Phases + Refinements):
- ✅ **Phase 1**: Foundation
  - Custom Tailwind gradient (`bg-gradient-summary`: blue-purple 45deg)
  - Reduced motion detection for accessibility (`prefersReducedMotion`)
  - Enhanced mock data structure for innovation points (emoji icons + titles + descriptions)
  - Backward compatibility for old (string) and new (object) innovation point formats

- ✅ **Phase 2**: Layout Refactoring
  - Full-width single-column layout with academic paper structure
  - Title + metadata group at top (traditional academic style)
  - Content area with two-column innovation points grid
  - Bottom action buttons (centered, symmetric)

- ✅ **Phase 3**: Visual Enhancements
  - Applied gradient background to Chinese summary section
  - Optimized title typography: `text-xl lg:text-2xl` (20px→24px) for readability
  - Enhanced summary text: `text-base` with `leading-relaxed`
  - Reduced padding and spacing for compact layout

- ✅ **Phase 4**: Innovation Point Cards
  - Two-column grid layout (`grid-cols-1 lg:grid-cols-2`)
  - Compact micro-cards with icon (text-2xl) + title (text-sm) + description (text-xs)
  - Hover lift effect (`-translate-y-1`) with shadow transition
  - Stagger animation using Vue's TransitionGroup (50ms delay per card)
  - All hover effects wrapped in `@media (hover: hover)` for touch device compatibility

- ✅ **Phase 5**: Mock Data Enhancement
  - All 24 papers now have targeted innovation points (72 total innovation points)
  - Daily papers (8): ML reasoning, time series, reinforcement learning, multimodal systems
  - Weekly papers (8): Federated learning, quantum ML, edge computing, explainable AI
  - Monthly papers (8): Neural architecture search, privacy-preserving ML, graph neural networks
  - Each innovation point includes quantitative metrics and domain-specific terminology

- ✅ **Phase 6**: Polish & Testing
  - Updated loading skeleton to match two-column card layout (6 card skeletons)
  - Fine-tuned spacing for 8px grid compliance (all gaps use multiples of 8px)
  - Verified WCAG AA contrast ratio (10.5:1 on gradient backgrounds)
  - Cross-browser compatibility verified (Chrome, Firefox, Safari, Edge)

- ✅ **UX Refinements** (User-driven iterations):
  - **Modal height control**: Added `max-h-[90vh]` with internal scrolling to prevent overflow
  - **Modal width**: Increased to `max-w-5xl` (1024px) for better content display
  - **Academic layout**: Metadata (author, field, date) moved to title subtitle for traditional academic style
  - **Symmetric footer**: Centered action buttons with consistent `min-w-[160px]`

**Key Files Modified**:
- `src/components/core/PaperModal.vue`: Complete refactoring with academic layout, two-column innovation grid, metadata subtitle (282 lines)
- `src/components/common/Modal.vue`: Added max-height constraint and flex layout for internal scrolling
- `src/mocks/paperData.js`: Added 680+ lines of targeted innovation points for all 24 papers (3 points × 24 papers)
- `tailwind.config.js`: Custom gradient configuration
- `specs/002-paper-modal-enhancement/tasks.md`: All 40 tasks marked complete

**Final Layout Structure**:
```
┌────────────────────────────────────────┐
│  [论文标题 - 20/24px bold]             │
│  作者 | 领域 | 日期 (14px gray)         │  ← Title Group
│                                        │
│  📝 中文摘要 (gradient background)     │
│  💡 创新点 (two-column grid)           │  ← Content Area
│      [Card] [Card]                    │
│      [Card] [Card]                    │
│      [Card] [Card]                    │
│                                        │
│  ─────────────────────────────────     │
│     [一键生成PPT] [下载PDF]            │  ← Action Area
└────────────────────────────────────────┘
```

**Technical Highlights**:
- **Academic layout**: Title + metadata subtitle mimics traditional academic paper style
- **Innovation point structure**: `{ icon, iconLabel, title, description }` with backward compatibility
- **Responsive design**: Mobile-first with `lg:` breakpoint (1024px) for two-column grid
- **Accessibility**: `prefers-reduced-motion` detection, ARIA labels, semantic HTML (`<article>`, `role="article"`)
- **Performance**: GPU-accelerated animations using `transform`, max-height prevents layout thrashing
- **Design system compliance**: 8px grid spacing, custom color palette, Inter + Noto Sans SC fonts
- **Visual balance**: Symmetric centered layout, no asymmetric elements

**Ready for**: Backend integration, user testing, and merge to main branch

To continue development, simply run:
```bash
npm install  # Install dependencies (if not already done)
npm run dev  # Start dev server on port 5173
```

## Development Commands

```bash
# Development
npm run dev              # Start dev server (port 5173, auto-opens browser)
npm run build            # Production build
npm run preview          # Preview production build
npm run lint             # ESLint with auto-fix

# Testing (optional, not configured by default)
npm run test             # Vitest unit tests
npm run test:coverage    # Coverage report
```

## Architecture: State Management Pattern

This project uses a **specific 3-store Pinia architecture** with strict responsibilities:

### papers.js Store
- **State**: `papers[]`, `loading`, `error`, `selectedPeriod`, `currentPage`, `totalPages`
- **Actions**: `fetchPapers(period, page)`, `setPeriod(period)`, `setPage(page)`
- **Purpose**: Paper discovery and pagination state
- **API**: Calls `paperService.fetchArxivPapers()` and `paperService.analyzePaper()`

### tasks.js Store
- **State**: `tasks[]`, `pollingActive`
- **Computed**: `activeTasks` (filters `queued|generating` tasks)
- **Actions**: `createTask()`, `startPolling()`, `stopPolling()`, `updateTaskStatus()`, `deleteTask()`
- **Purpose**: PPT task history with 5-second polling loop
- **Persistence**: Auto-saves to localStorage after every task update
- **Lifecycle**: `onMounted` loads from localStorage and auto-starts polling if active tasks exist; `onUnmounted` clears polling interval

### ui.js Store
- **State**:
  - Paper modal: `modalOpen`, `currentPaper`, `currentAnalysis`, `analysisLoading`
  - PPT preview: `pptPreviewOpen`, `currentPPTContent`, `pptContentLoading`, `pptContentError`
  - Toast: `toastVisible`, `toastMessage`, `toastType`
- **Actions**:
  - Paper: `openModal(paperId)`, `closeModal()`
  - PPT Preview: `openPPTPreview(taskId)`, `closePPTPreview()`
  - Toast: `showToast(message, type)`, `hideToast()`
- **Purpose**: Global UI state (modals, toast notifications)
- **Special Behavior**:
  - `openModal()` handles 202 (pending) responses with recursive retry up to 3 times
  - `openPPTPreview()` fetches PPT content via `getPPTContent(taskId)` with error handling

**Critical Pattern**: The `tasks` store manages the **5-second polling interval** for task status updates. Polling auto-starts when tasks with status `queued` or `generating` exist and auto-stops when `activeTasks.length === 0`.

## Architecture: API Service Layer

Centralized Axios client in `api/index.js` with:
- Base URL from `VITE_API_BASE_URL` env var
- 60-second default timeout
- Request/response interceptors for global error handling

Service modules:
- `api/paperService.js`: `fetchArxivPapers()`, `analyzePaper()`
- `api/uploadService.js`: `uploadPDF()` with progress callback
- `api/taskService.js`: `createPPTTask()`, `pollTaskStatus()`
- `api/pptContentService.js`: `getPPTContent(taskId)` - fetches PPT markdown content (supports Mock/Real API toggle)

**Pattern**: All service functions return `response.data` directly, not full Axios response.

## Architecture: Composables Pattern

Extract reusable logic into composables:

- `composables/useTaskHistory.js`: localStorage CRUD operations, handles 5MB quota exceeded with auto-pruning
- `composables/useTaskPolling.js`: Polling interval management with cleanup
- `composables/useFileUpload.js`: File validation (PDF, <=20MB), upload progress tracking

**Usage**: Composables return reactive `ref()` objects and functions, not stores.

## Design System Tokens (Tailwind Config)

**MUST** use these exact values in `tailwind.config.js`:

```javascript
colors: {
  'primary-bg': '#FFFFFF',
  'secondary-bg': '#F8F9FA',
  'border-color': '#E9ECEF',
  'text-primary': '#212529',
  'text-secondary': '#6C757D',
  'accent': '#3A57E8',
  'success': '#198754',
  'error': '#DC3545',
}
```

**Typography**: H1: 28px, H2: 22px, H3: 18px, Body: 16px, Secondary: 14px
**Spacing**: 8px grid (use multiples: 8, 16, 24, 32, 40, 48)
**Border Radius**: Button: 6px, Card: 1px, Modal: 12px
**Fonts**: Inter (English) + Noto Sans SC (Chinese) from Google Fonts CDN

## Component Structure Rules

### Common Components (`components/common/`)
Reusable UI primitives, design-system-compliant, no business logic:
- `Button.vue`: Props: `variant`, `size`, `disabled`, `loading` (shows spinner) - **Updated**: Fixed icon alignment with direct slot rendering
- `Modal.vue`: Uses Headless UI `<Dialog>`, backdrop blur, ESC to close, focus trap
- `Toast.vue`: Auto-dismiss after 3s, top-center fixed, slide-in animation
- `Badge.vue`: Status colors: yellow (queued), blue (generating), green (completed), red (failed)
- `Tabs.vue`: Uses Headless UI `<TabGroup>`, keyboard navigation
- `Pagination.vue`: Previous/Next, ellipsis for large page counts
- `Watermark.vue`: 9-grid watermark overlay, environment-configurable (text, opacity, color), non-intrusive (pointer-events: none) - **New**

### Core Components (`components/core/`)
Business logic components tied to stores:
- `PaperCard.vue`: Displays paper, click opens modal via `uiStore.openModal(paperId)`
- `PaperDiscovery.vue`: Tab navigation (Daily/Weekly/Monthly), paper grid, loading skeleton
- `PaperModal.vue`: Displays AI analysis, "Generate PPT" button, skeleton during loading - **Enhanced**: Academic layout, two-column innovation grid
- `PPTPreviewModal.vue`: Full PPT preview with LaTeX + code + watermark, fixed-height slide container (600px), keyboard navigation, smooth scrolling - **Complete** (516 lines)
- `UploadDropzone.vue`: Drag-drop, progress bar, client-side validation (PDF, 20MB)
- `TaskItem.vue`: Conditional rendering per status (queued/generating/completed/failed), **preview button for completed tasks** - **Enhanced**
- `TaskHistory.vue`: Scrollable list, empty state, reverse chronological order

**Naming Convention**: PascalCase for components, camelCase for composables/utilities.

## Backend API Contracts

Full specifications in `specs/001-mvp-frontend-implementation/contracts/`. Key endpoints:

- `GET /api/arxiv_papers?period={daily|weekly|monthly}&page=1&limit=20` - Trending papers
- `POST /api/upload_pdf` - Multipart form-data, returns `fileId`
- `GET /api/analyze_paper?arxivId=2301.00000` OR `?fileId={uuid}` - AI analysis (may return 202 for pending)
- `POST /api/generate_ppt` - Body: `{arxivId}` OR `{fileId}`, returns `taskId`
- `GET /api/task_status?taskId={uuid}` - Poll every 5 seconds for status updates
- `GET /api/ppt_content?taskId={uuid}` - Fetch PPT content in Markdown format (returns `{taskId, markdown, metadata}`)

**Critical**:
- Analysis endpoint returns 202 (pending) when not ready. Frontend MUST retry after `retryAfter` seconds (up to 3 retries).
- PPT content endpoint returns Markdown with `---` slide separators for preview rendering.

## localStorage Strategy

**Key**: `lundao-tasks` (or similar)
**Format**: JSON array of `PPTTask` objects
**Capacity**: 5MB limit (typical browser)
**Quota Handling**: When `QuotaExceededError`, auto-prune oldest completed tasks (keep max 50 recent), show toast warning
**Expiration**: Auto-remove tasks >24 hours old on mount

**Implementation Location**: `composables/useTaskHistory.js`

## Performance Requirements

- **First Contentful Paint**: <1.5s on 3G
- **Interaction Response**: <100ms visual feedback for non-network operations (network ops show loading states immediately)
- **Task Polling**: 5 seconds interval, uses `Promise.allSettled()` to handle individual failures
- **Asset Optimization**: Images compressed, Chinese fonts subset (post-MVP)

## SpecKit Workflow Commands

This project uses a structured planning workflow. Key slash commands:

- `/speckit.specify` - Generate feature specification
- `/speckit.plan` - Generate implementation plan with contracts
- `/speckit.tasks` - Generate task breakdown (78 tasks for MVP)
- `/speckit.analyze` - Cross-artifact consistency analysis

**Implementation Sequence**: Follow `specs/001-mvp-frontend-implementation/tasks.md` (Phases 1-7, T001-T078).

## ESLint Configuration

**Rules to Disable** (per project conventions):
```javascript
rules: {
  'vue/multi-word-component-names': 'off',
  'vue/require-default-prop': 'off',
}
```

## Environment Variables

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:3000/api
VITE_USE_MOCK_DATA=true  # Enable mock data when backend unavailable

# .env.production
VITE_API_BASE_URL=https://api.lundao.com/api
VITE_USE_MOCK_DATA=false  # Use real API in production
```

**Note**: Add `.env.local` to `.gitignore` for local overrides.

## Mock Data System (Development)

**Location**: `src/mocks/`

The project includes a production-ready mock data system for frontend development when backend is unavailable.

### Paper Discovery Mock (Feature #001)
- ✅ 24 high-quality papers based on real 2025 arXiv research topics
- ✅ Three time periods: daily (8 papers), weekly (8 papers), monthly (8 papers)
- ✅ Automatic Chinese analysis generation (summary + 3 innovation points)
- ✅ Simulated network delays (500ms papers, 800ms analysis)
- ✅ Full pagination support (8 papers per page)
- ✅ Zero-modification toggle via environment variable

### PPT Task Mock System (Feature #003)

**Status**: ✅ Implemented (all 18 tasks complete)
**Branch**: `003-ppt-task-mock`
**Spec**: `specs/003-ppt-task-mock-system/`

Extends the mock system to cover PPT generation and task history, enabling complete frontend development without backend dependency. The system provides realistic task lifecycle simulation, historical task data, and seamless environment-based switching between mock and real API modes.

**Architecture**:
- `src/mocks/taskData.js` - Historical task mock data (3 pre-populated tasks: 2 completed + 1 failed)
- `src/mocks/taskService.js` - Mock task creation and status polling functions
- `src/mocks/utils.js` - Mock helper utilities (ID generation, network delay simulation)
- `src/api/taskService.js` - Environment-based routing (mock vs real API)
- `src/stores/tasks.js` - Enhanced initialization to load historical tasks in mock mode

**Status Progression Mechanism**:
- Uses in-memory Map (`taskCreationTimes`) to track task creation timestamps
- Status calculated on each poll based on elapsed time:
  - 0-5 seconds: `queued` (no progress)
  - 5-15 seconds: `generating` (progress 0-90%, linear interpolation)
  - 15+ seconds: `completed` (progress 100%, download URL provided)
- Page refresh clears Map → orphaned tasks automatically marked as `failed` with error message

**Mock Task ID Format**: `mock-task-{timestamp}-{random6chars}`
- Example: `mock-task-1705300123456-a3f8e9`
- Prefix distinguishes from real UUIDs, enables coexistence in localStorage

**Download Handling**: Mock downloads show toast "Mock模式: 实际部署后可下载真实PPT文件" instead of downloading files

**Implementation Tasks**: 18 tasks (T001-T018) organized by user story
- Setup: 3 tasks (foundation files)
- US1 (Task Creation): 5 tasks (mock creation + API routing)
- US2 (Status Progression): 2 tasks (mock polling + API routing)
- US3 (Historical Tasks): 2 tasks (store initialization + page refresh handling)
- US4 (Mode Switching): 2 tasks (documentation)
- Polish: 4 tasks (download handling + final validation)

### Mock System Usage
```bash
# Enable mock mode (default in development)
VITE_USE_MOCK_DATA=true

# Disable mock mode (use real API)
VITE_USE_MOCK_DATA=false
```

**Important**: Mock mode is controlled at the store/service level (`papers.js`, `ui.js`, `taskService.js`). When backend is ready, simply change the environment variable—no code changes needed.

### Research Topics Covered
Mock data includes real 2025 research trends:
- Hierarchical Reasoning Models (small-scale recursive reasoning)
- OpenTSLM (time series language models)
- RLVR (reinforcement learning with verifiable rewards)
- Multi-agent collaborative reasoning
- Federated learning for healthcare
- Quantum machine learning
- AI ethics and cultural understanding

See `src/mocks/README.md` for complete documentation and maintenance guide.

### PPT Content Mock (Feature #004)

**Status**: ✅ Complete (All 4 phases + UX improvements + Universal demo PPT)
**Branch**: `003-ppt-task-mock` (ready for merge)
**Spec**: `specs/004-ppt-preview-feature/`

Provides comprehensive PPT content preview with LaTeX formulas, code syntax highlighting, watermark protection, and universal demo PPT for seamless demonstration.

**Architecture**:
- `src/mocks/pptContentData.js` - Mock PPT content in Markdown format (specific tasks + universal demo)
- `src/utils/pptRenderer.js` - Rendering pipeline: marked + KaTeX + highlight.js + DOMPurify
- `src/api/pptContentService.js` - Environment-based API routing (mock vs real)
- `src/components/core/PPTPreviewModal.vue` - Full-featured preview modal with fixed-height layout (516 lines)
- `src/components/common/Watermark.vue` - 9-grid watermark component (139 lines)
- `src/config/watermark.js` - Environment-configurable watermark settings

**Dependencies Added**:
- `marked@11.0.0` - Markdown parser (32 KB)
- `marked-katex-extension@5.0.0` - KaTeX integration (8 KB)
- `katex@0.16.9` - LaTeX math formula rendering (340 KB with fonts)
- `highlight.js@11.9.0` - Code syntax highlighting (80 KB for 7 languages)
- `dompurify@3.0.6` - XSS protection (13 KB)

**Features Implemented** (All 4 Phases):
- ✅ **Phase 1**: Foundation - Dependencies, mock data, rendering utilities, API service
- ✅ **Phase 2**: Core Components - Store extension, modal component, slide navigation, TaskItem integration
- ✅ **Phase 3**: Enhancements - Keyboard navigation, styling (LaTeX + code), error handling, caching, **watermark system**
- ✅ **Phase 4**: Testing & Documentation - Functional testing, security audit, performance testing, comprehensive docs
- ✅ **Post-completion**: UX improvements - Button alignment, fixed slide heights (600px), smooth scrolling

**Universal Demo PPT** (NEW):
- **Fallback Logic**: Any taskId not found → automatic fallback to `demo-default` (11-slide comprehensive demo)
- **Purpose**: Enable seamless product demonstration and testing without pre-configuring every taskId
- **Content**: Complete showcase of all features (LaTeX, code, tables, ASCII art, nested lists, blockquotes)
- **Coverage**: All 7 supported code languages, inline + block formulas, performance tables
- **Documentation**: `src/mocks/README-PPT-PREVIEW.md` (342 lines)

**Mock PPT Content**:
- **demo-default** (universal): 11 comprehensive slides showcasing all features
- **mock-task-001**: 10 slides with LaTeX formulas and Python code examples (Hierarchical Reasoning)
- **mock-task-002**: 4 slides about time series language models (OpenTSLM)
- **mock-task-003**: `null` (failed task for error handling testing)
- **Any other taskId**: Automatically uses `demo-default` (no configuration needed)

**Watermark System**:
- **Layout**: 9-grid distribution (3×3 positions across slide)
- **Rotation**: -30 degrees for diagonal aesthetic
- **Environment Control**: `VITE_WATERMARK_ENABLED`, `VITE_WATERMARK_TEXT`, `VITE_WATERMARK_OPACITY`
- **Non-intrusive**: `pointer-events: none`, `user-select: none`
- **Protection Level**: MVP baseline (visible deterrent, removable via DevTools - acceptable for beta)

**Bundle Impact**:
- **JS**: 75 KB → 197 KB gzipped (+122 KB) - includes KaTeX, highlight.js, marked, DOMPurify
- **CSS**: 5.27 KB → 22.17 KB gzipped (+16.9 KB) - includes KaTeX styles, highlight.js theme
- **KaTeX Fonts**: ~500 KB (12 font files, cached after first load, CDN-ready)
- **Build Time**: 1.56s (optimized from 2.22s via Rollup chunk splitting)

**Rendering Pipeline**:
```javascript
Markdown → parseSlides() → marked.parse() → KaTeX extension → highlight.js → DOMPurify → Safe HTML → v-html
                ↓                                                                    ↓
         Split by ---                                                        Whitelist: KaTeX MathML
```

**Keyboard Shortcuts**:
- `Arrow Right` / `Arrow Left`: Navigate slides
- `Home` / `End`: Jump to first/last slide
- `Escape`: Close modal

**Security**:
- ✅ XSS protection via DOMPurify with KaTeX MathML whitelist
- ✅ All test cases passed: `<script>`, `<iframe>`, `onerror` attributes stripped
- ✅ LaTeX formula injection attempts safely escaped

**UX Quality**:
- ✅ Consistent slide height (600px fixed container)
- ✅ Smooth scrolling for long content (`scroll-behavior: smooth`)
- ✅ Custom scrollbar styling (8px width, rounded, hover transitions)
- ✅ Button icon alignment fixed (flex `items-center` direct slot rendering)
- ✅ Loading skeleton, error retry UI, accessibility (ARIA labels)

## Key Gotchas

1. **Project IS Fully Implemented**: ✅ Core MVP complete + 4 major enhancements (168 tasks total). Ready for backend integration, user testing, and production deployment.
2. **Composition API Only**: ALL components MUST use `<script setup>`, not Options API.
3. **No Router**: This is a true single-page app. HomeView is the only view, rendered directly in App.vue.
4. **Polling Cleanup**: MUST call `stopPolling()` in `onUnmounted` to prevent memory leaks.
5. **Modal Focus Trap**: Headless UI handles this automatically; don't add custom focus management.
6. **localStorage Quota**: ALWAYS wrap `localStorage.setItem()` in try-catch for `QuotaExceededError`.
7. **Analysis Retry Logic**: The 202 pending response is EXPECTED behavior, not an error. Retry up to 3 times.
8. **Design System**: Deviations from color palette, spacing, or typography require constitutional amendment.
9. **PPT Preview Universal Demo**: Any taskId without specific mock data automatically uses `demo-default` (11 slides). No error thrown for unknown taskIds.
10. **Button Icon Alignment**: Use direct `<slot>` rendering without wrappers. Extra `<span>` breaks flex `items-center` alignment.
11. **Slide Height Consistency**: PPTPreviewModal uses fixed 600px container with scrollable content. Do NOT use dynamic height based on content.
12. **Watermark Environment**: Watermark text/opacity controlled via `.env` files. MVP watermark is visible but removable (acceptable for beta).
13. **LaTeX Double Escaping**: In JavaScript template strings (backticks), ALL LaTeX commands MUST use double backslashes. JavaScript interprets `\` first, so `\text` becomes `text` before reaching LaTeX renderer. Always use `\\text`, `\\frac`, `\\theta`, etc. See `specs/005-ppt-content-intelligence/LATEX-FIX-SUMMARY.md` for complete reference.

## Reference Documentation

**📚 Comprehensive reference docs available in `/ref/` directory**:

- **[/ref/README.md](ref/README.md)** - Documentation index and navigation guide
- **[/ref/architecture.md](ref/architecture.md)** - System architecture, tech stack, patterns, build config
- **[/ref/design-system.md](ref/design-system.md)** - Color palette, typography, spacing (8px grid), accessibility
- **[/ref/components.md](ref/components.md)** - 14 components (7 common + 7 core) with props, emits, usage
- **[/ref/state-management.md](ref/state-management.md)** - 3 Pinia stores (papers, tasks, ui) + composables
- **[/ref/api-services.md](ref/api-services.md)** - API services, mock system, environment switching
- **[/ref/utilities.md](ref/utilities.md)** - PPT renderer, watermark config, file validation, helpers
- **[/ref/deployment.md](ref/deployment.md)** - Docker, Aliyun ECS, and static hosting deployment guides

**Quick Reference by Topic**:
- **Architecture & Patterns**: `/ref/architecture.md`
- **Visual Design Standards**: `/ref/design-system.md`
- **Component API**: `/ref/components.md` (search by component name)
- **State Management**: `/ref/state-management.md` (papers, tasks, ui stores)
- **API Integration**: `/ref/api-services.md` (service modules + mocks)
- **Utilities & Helpers**: `/ref/utilities.md` (PPT rendering, watermark, validation)
- **Deployment**: `/ref/deployment.md` (Docker, Aliyun ECS, Netlify)

## Deployment Documentation

**🐳 Docker Containerization** (Feature #006):
- **Status**: ✅ Complete - Full Docker deployment solution
- **Docker Guide**: [DOCKER-DEPLOYMENT.md](DOCKER-DEPLOYMENT.md) (370+ lines, complete deployment guide)
- **Implementation Summary**: [DOCKER-IMPLEMENTATION-SUMMARY.md](DOCKER-IMPLEMENTATION-SUMMARY.md)
- **Key Files**:
  - `Dockerfile` - Multi-stage build (Node.js + Nginx)
  - `docker-compose.yml` - Dual environment orchestration (prod + demo)
  - `.dockerignore` - Build context optimization
  - `nginx.conf` - Production Nginx configuration
- **npm scripts**: 10 Docker convenience commands
- **Image Size**: ~255 MB (final), Build time: 2-5 minutes
- **Features**: Health checks, auto-restart, dual environment support

**☁️ Aliyun ECS Deployment** (Feature #007):
- **Status**: ✅ Complete - Production-ready deployment scripts
- **Aliyun Guide**: [ALIYUN-DEPLOYMENT.md](ALIYUN-DEPLOYMENT.md) (520+ lines, comprehensive guide)
- **Quick Start**: [deploy/QUICKSTART.md](deploy/QUICKSTART.md) (5-minute deployment)
- **Deployment Summary**: [ALIYUN-DEPLOYMENT-SUMMARY.md](ALIYUN-DEPLOYMENT-SUMMARY.md)
- **Deployment Scripts**:
  - `deploy/deploy.sh` (200+ lines) - One-click deployment with environment checks
  - `deploy/update.sh` (100+ lines) - Smart update with automatic rollback
  - `deploy/nginx.conf` - Nginx reverse proxy configuration with HTTPS template
  - `deploy/README.md` (350+ lines) - Detailed script documentation
- **Port Configuration**: Docker container (8082), Nginx proxy (80/443)
- **Features**: Automated deployment, health checks, backup/rollback, HTTPS support

**🌐 Static Hosting Deployment**:
- **General Guide**: [DEPLOYMENT.md](DEPLOYMENT.md) (Netlify, GitHub Pages)
- **Netlify Drop**: 30-second deployment (no registration)
- **Netlify Git**: Automatic CI/CD with PR previews
- **Environment**: `.env.production.local` for frontend-only deployment

**Quick Commands**:
```bash
# Docker local development
docker-compose up -d                    # Production mode (port 8080)
npm run docker:compose:demo             # Demo mode (port 8081)

# Aliyun ECS deployment
./deploy/deploy.sh demo                 # Deploy to ECS (demo mode)
./deploy/update.sh prod                 # Update deployment (production)

# Static hosting
npm run build && netlify deploy         # Netlify deployment
```

## Original Documentation

- **Constitution**: `.specify/memory/constitution.md` (governance, non-negotiable rules)
- **Quickstart**: `specs/001-mvp-frontend-implementation/quickstart.md` (14-step setup)
- **Tasks**: `specs/001-mvp-frontend-implementation/tasks.md` (78 implementation tasks)
- **API Contracts**: `specs/001-mvp-frontend-implementation/contracts/*.md` (5 endpoint specs)
- **Data Model**: `specs/001-mvp-frontend-implementation/data-model.md` (entities: Paper, AIAnalysis, PPTTask, TaskHistory)
- **PPT Content Intelligence**: `specs/005-ppt-content-intelligence/` (content enhancement strategy, LaTeX fix documentation, generation guide)

## Recommended VS Code Extensions

- Volar (Vue Language Features)
- ESLint
- Tailwind CSS IntelliSense
- Prettier

## Node Version Requirements

- **Node.js**: v18.x or later (v20.x recommended)
- **npm**: v9.x or later

Verify with:
```bash
node --version  # >= v18.0.0
npm --version   # >= v9.0.0
```

## Reference Documentation

**📚 Comprehensive reference docs available in `/ref/` directory**:

- **[/ref/README.md](ref/README.md)** - Documentation index and navigation guide
- **[/ref/architecture.md](ref/architecture.md)** - System architecture, tech stack, patterns, build config
- **[/ref/design-system.md](ref/design-system.md)** - Color palette, typography, spacing (8px grid), accessibility
- **[/ref/components.md](ref/components.md)** - 14 components (7 common + 7 core) with props, emits, usage
- **[/ref/state-management.md](ref/state-management.md)** - 3 Pinia stores (papers, tasks, ui) + composables
- **[/ref/api-services.md](ref/api-services.md)** - API services, mock system, environment switching
- **[/ref/utilities.md](ref/utilities.md)** - PPT renderer, watermark config, file validation, helpers
- **[/ref/deployment.md](ref/deployment.md)** - Docker, Aliyun ECS, and static hosting deployment guides

**Quick Reference by Topic**:
- **Architecture & Patterns**: `/ref/architecture.md`
- **Visual Design Standards**: `/ref/design-system.md`
- **Component API**: `/ref/components.md` (search by component name)
- **State Management**: `/ref/state-management.md` (papers, tasks, ui stores)
- **API Integration**: `/ref/api-services.md` (service modules + mocks)
- **Utilities & Helpers**: `/ref/utilities.md` (PPT rendering, watermark, validation)
- **Deployment**: `/ref/deployment.md` (Docker, Aliyun ECS, Netlify)

## Deployment Documentation

**🐳 Docker Containerization** (Feature #006):
- **Status**: ✅ Complete - Full Docker deployment solution
- **Docker Guide**: [DOCKER-DEPLOYMENT.md](DOCKER-DEPLOYMENT.md) (370+ lines, complete deployment guide)
- **Implementation Summary**: [DOCKER-IMPLEMENTATION-SUMMARY.md](DOCKER-IMPLEMENTATION-SUMMARY.md)
- **Key Files**:
  - `Dockerfile` - Multi-stage build (Node.js + Nginx)
  - `docker-compose.yml` - Dual environment orchestration (prod + demo)
  - `.dockerignore` - Build context optimization
  - `nginx.conf` - Production Nginx configuration
- **npm scripts**: 10 Docker convenience commands
- **Image Size**: ~255 MB (final), Build time: 2-5 minutes
- **Features**: Health checks, auto-restart, dual environment support

**☁️ Aliyun ECS Deployment** (Feature #007):
- **Status**: ✅ Complete - Production-ready deployment scripts
- **Aliyun Guide**: [ALIYUN-DEPLOYMENT.md](ALIYUN-DEPLOYMENT.md) (520+ lines, comprehensive guide)
- **Quick Start**: [deploy/QUICKSTART.md](deploy/QUICKSTART.md) (5-minute deployment)
- **Deployment Summary**: [ALIYUN-DEPLOYMENT-SUMMARY.md](ALIYUN-DEPLOYMENT-SUMMARY.md)
- **Deployment Scripts**:
  - `deploy/deploy.sh` (200+ lines) - One-click deployment with environment checks
  - `deploy/update.sh` (100+ lines) - Smart update with automatic rollback
  - `deploy/nginx.conf` - Nginx reverse proxy configuration with HTTPS template
  - `deploy/README.md` (350+ lines) - Detailed script documentation
- **Port Configuration**: Docker container (8082), Nginx proxy (80/443)
- **Features**: Automated deployment, health checks, backup/rollback, HTTPS support

**🌐 Static Hosting Deployment**:
- **General Guide**: [DEPLOYMENT.md](DEPLOYMENT.md) (Netlify, GitHub Pages)
- **Netlify Drop**: 30-second deployment (no registration)
- **Netlify Git**: Automatic CI/CD with PR previews
- **Environment**: `.env.production.local` for frontend-only deployment

**Quick Commands**:
```bash
# Docker local development
docker-compose up -d                    # Production mode (port 8080)
npm run docker:compose:demo             # Demo mode (port 8081)

# Aliyun ECS deployment
./deploy/deploy.sh demo                 # Deploy to ECS (demo mode)
./deploy/update.sh prod                 # Update deployment (production)

# Static hosting
npm run build && netlify deploy         # Netlify deployment
```

## Original Documentation

- **Constitution**: `.specify/memory/constitution.md` (governance, non-negotiable rules)
- **Quickstart**: `specs/001-mvp-frontend-implementation/quickstart.md` (14-step setup)
- **Tasks**: `specs/001-mvp-frontend-implementation/tasks.md` (78 implementation tasks)
- **API Contracts**: `specs/001-mvp-frontend-implementation/contracts/*.md` (5 endpoint specs)
- **Data Model**: `specs/001-mvp-frontend-implementation/data-model.md` (entities: Paper, AIAnalysis, PPTTask, TaskHistory)
- **PPT Content Intelligence**: `specs/005-ppt-content-intelligence/` (content enhancement strategy, LaTeX fix documentation, generation guide)

## Recommended VS Code Extensions

- Volar (Vue Language Features)
- ESLint
- Tailwind CSS IntelliSense
- Prettier

## Node Version Requirements

- **Node.js**: v18.x or later (v20.x recommended)
- **npm**: v9.x or later

Verify with:
```bash
node --version  # >= v18.0.0
npm --version   # >= v9.0.0
```

