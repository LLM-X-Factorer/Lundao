<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- This is the initial constitution ratification
- Principles derived from: Docs/PRD.md and Docs/BluePrint.md
- Templates status:
  ✅ plan-template.md - reviewed and compatible
  ✅ spec-template.md - reviewed and compatible
  ✅ tasks-template.md - reviewed and compatible
- Follow-up TODOs: None
-->

# 论导Lite Frontend Constitution

## Core Principles

### I. Tool-First Philosophy (工具化，非平台化)

All features MUST serve the core "use-and-leave" workflow without adding user retention burdens. The application is a tool, not a platform.

**Non-negotiable rules**:
- NO user account management features (registration, login, profiles)
- NO features that require users to "manage" or "organize" content
- NO gamification, badges, or engagement mechanics
- EVERY feature must directly support: discover paper → understand paper → create presentation

**Rationale**: Academic users need efficiency, not engagement. Time spent on the tool is time NOT spent on research. Value delivery must be immediate and friction-free.

### II. Single-Page Minimalism (单页极简)

Core functionality MUST reside on a single page. Navigation beyond the root route (`/`) is prohibited for primary workflows.

**Non-negotiable rules**:
- All primary features accessible from root route (`/`)
- NO multi-page flows for core tasks
- Modals and overlays permitted for contextual detail
- Secondary content (terms, about) may use separate routes but must not interrupt workflow

**Rationale**: Every page transition adds cognitive load and time. For a tool designed around speed ("3 minutes to presentation"), eliminating navigation is critical to user experience.

### III. Zero Friction (零摩擦体验)

Users MUST access all core functionality without authentication or account creation.

**Non-negotiable rules**:
- NO login/registration gates for: paper discovery, PDF upload, AI analysis, PPT generation
- State persistence via `localStorage` only
- Anonymous usage is the default and primary experience
- Future authentication (if added) must be OPTIONAL and non-blocking

**Rationale**: Academic users experiment with tools before committing. Registration friction causes 40-60% abandonment. Value must be delivered before asking for commitment.

### IV. Value-First Design (价值前置)

AI-generated insights (Chinese summary, innovation points) MUST be prominently displayed immediately upon analysis completion.

**Non-negotiable rules**:
- Chinese summary and innovation points are primary content, not secondary
- Skeleton screens or elegant loading states required during analysis
- Original paper metadata is secondary to AI insights
- Download/external links are tertiary actions

**Rationale**: Users seek understanding, not raw papers. Prioritizing AI analysis output aligns with the core value proposition and differentiates from paper aggregators.

### V. Aesthetics as Trust (美学优先)

Visual design quality directly impacts perceived product reliability and user trust. Modern, minimalist design is non-negotiable.

**Non-negotiable rules**:
- Adhere strictly to defined Design System (colors, typography, spacing)
- All interactions MUST have smooth transitions (no jarring state changes)
- 8px grid system for all spacing (8, 16, 24, 32px)
- Empty states and error states require thoughtful, helpful design
- Inter (English) + Noto Sans SC (Chinese) fonts required

**Rationale**: Academic users associate visual quality with technical competence. A polished interface increases conversion by signaling reliability and professionalism.

## Technical Standards

### Technology Stack

The following stack is REQUIRED for consistency and optimal developer experience:

- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **CSS Framework**: Tailwind CSS (for design system implementation)
- **Component Logic**: Headless UI (for accessible, unstyled component primitives)
- **State Management**: Pinia (for task polling and global state)
- **HTTP Client**: Axios (with centralized configuration)

**Rationale**: This stack enables 1:1 design implementation without fighting framework defaults, provides excellent DX, and ensures accessibility compliance.

### Design System Enforcement

All visual implementations MUST adhere to the defined Design System:

**Color Palette**:
- Primary Background: `#FFFFFF` or `#FDFDFD`
- Secondary Background: `#F8F9FA`
- Borders: `#E9ECEF`
- Primary Text: `#212529`
- Secondary Text: `#6C757D`
- Accent/Brand: `#3A57E8`
- Success: `#198754`
- Error: `#DC3545`

**Typography Scale**:
- H1: 28px, H2: 22px, H3/Card Title: 18px, Body: 16px, Secondary: 14px

**Component Specifications**:
- Button border-radius: 6px
- Card border: 1px solid #E9ECEF, hover shadow permitted
- Modal border-radius: 12px
- All spacing: multiples of 8px

**Enforcement**: Code reviews MUST verify design system compliance. Deviations require explicit justification.

### Performance Requirements

- **First Contentful Paint**: < 1.5s on 3G connection
- **Interaction Response**: Visual feedback within 100ms for all user actions
- **Task Polling Interval**: 5 seconds (configurable for performance tuning)
- **Code Splitting**: Dynamic imports for modal components and secondary features
- **Asset Optimization**: Images compressed, fonts subset for Chinese characters

**Rationale**: Academic users often work in institutional networks with variable bandwidth. Fast loading ensures accessibility across network conditions.

## Development Workflow

### Project Structure

MUST follow the defined architecture:

```
src/
├── api/               # Axios request encapsulation
├── assets/            # Static resources
├── components/
│   ├── common/        # Reusable UI primitives
│   └── core/          # Business logic components
├── composables/       # Composition API logic reuse
├── stores/            # Pinia state management
├── views/             # Page-level components
├── App.vue
└── main.js
```

**Rationale**: Clear separation of concerns enables parallel development and reduces merge conflicts.

### Component Development Standards

- **Composition API**: MUST use `<script setup>` syntax for all components
- **Props**: Use TypeScript-style prop definitions with validation
- **Emits**: Explicitly declare all emitted events
- **Composables**: Extract reusable logic to `composables/` directory
- **Naming**: PascalCase for components, camelCase for composables/utilities

### State Management Rules

- **localStorage** for task history persistence
- **Pinia stores** for reactive polling state and cross-component coordination
- **Props/emits** for parent-child communication
- **Provide/inject** ONLY when prop drilling exceeds 2 levels

**Rationale**: Clear state ownership prevents bugs and makes data flow traceable.

### API Integration

All backend communication MUST follow these patterns:

- Centralized API client configuration in `api/index.js`
- Service modules per feature domain (e.g., `api/taskService.js`)
- Request/response interceptors for global error handling
- Loading states managed at component level
- Error states displayed with user-friendly messages

**Backend API Contract** (from PRD):
- GET `/api/arxiv_papers` - paper discovery
- POST `/api/upload_pdf` - file upload
- GET `/api/analyze_paper` - AI analysis
- POST `/api/generate_ppt` - task creation
- GET `/api/task_status` - polling endpoint

### Testing Strategy (Optional but Recommended)

- **Component Tests**: Vitest + Vue Test Utils for business logic components
- **Integration Tests**: E2E tests for critical user flows (upload → analyze → generate)
- **Visual Regression**: Chromatic or Percy for design system consistency
- **Manual Testing**: Required for all interaction states and animations

## Governance

### Amendment Procedure

1. Proposed changes MUST be documented in a GitHub issue or PR description
2. Changes affecting core principles (I-V) require explicit justification
3. Technical standard updates require validation against existing codebase
4. Version bumping follows semantic versioning:
   - **MAJOR**: Principle removal or backward-incompatible changes
   - **MINOR**: New principles or expanded technical standards
   - **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance Verification

- All PRs MUST verify compliance with relevant constitution sections
- Design reviews MUST check Design System adherence
- Architecture decisions MUST align with Technology Stack requirements
- Feature proposals MUST validate against Core Principles (especially I-IV)

### Living Document Status

This constitution reflects the MVP phase requirements. As the project evolves:
- User feedback may inform principle refinements
- Performance data may adjust technical standards
- New features must pass constitutional review before implementation

**Version**: 1.0.0 | **Ratified**: 2025-10-14 | **Last Amended**: 2025-10-14
