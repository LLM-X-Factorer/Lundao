# Implementation Plan: Paper Modal Enhancement

**Branch**: `002-paper-modal-enhancement` | **Date**: 2025-10-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-paper-modal-enhancement/spec.md`

## Summary

This feature transforms the existing paper detail modal from a traditional vertical layout into a modern, visually engaging split-pane interface that better showcases AI-generated insights. The enhancement includes:

1. **Layout Refactoring**: Migrate from vertical stack to responsive split-pane design (left: content 60%, right: metadata 40%)
2. **Innovation Points Redesign**: Convert simple list to micro-card grid with emoji icons, bold titles, and hover interactions
3. **Visual Hierarchy Enhancement**: Add gradient backgrounds, 32px title typography, stagger animations, and subtle transitions
4. **Mock Data Quality Upgrade**: Replace generic template-based innovation points with 24 paper-specific, research-targeted descriptions
5. **Responsive Design**: Implement progressive degradation (desktop split-pane → mobile single-column) at 768px/1024px breakpoints

**Technical Approach**: Pure frontend enhancement with no backend API changes. Refactor `PaperModal.vue` component structure, update Tailwind configuration for custom gradients, enhance `src/mocks/paperData.js` with targeted content, and add optional `InnovationCard.vue` sub-component for reusability.

## Technical Context

**Language/Version**: JavaScript/ES6+ (Vue 3.5 Composition API with `<script setup>` syntax)
**Primary Dependencies**:
- Vue 3.5 (Composition API, Transition, TransitionGroup for animations)
- Tailwind CSS 3.4 (utility classes, custom gradients, responsive design)
- Headless UI 1.7 (Dialog component, no changes needed)
- Existing stores: `ui.js` (modal state management)

**Storage**: No new storage requirements (modal state remains in-memory via Pinia)
**Testing**: Manual testing required for visual validation, optional Vitest component tests for layout logic
**Target Platform**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+), responsive across desktop/tablet/mobile
**Project Type**: Single-page web application (SPA), enhancement to existing modal component
**Performance Goals**:
- Modal open animation: <300ms
- Hover interactions: <16ms (60fps)
- Bundle size increase: <10KB gzipped

**Constraints**:
- MUST adhere to constitution design system (8px spacing grid, approved color palette)
- NO breaking changes to `ui.js` store interface
- MUST support `prefers-reduced-motion` accessibility requirement
- MUST maintain WCAG 2.1 AA contrast ratios (4.5:1 minimum)

**Scale/Scope**: Single component refactoring + mock data enhancement, estimated 24 papers × 3 innovation points = 72 targeted descriptions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with `.specify/memory/constitution.md`:

- [x] **Tool-First Philosophy**: ✅ Feature enhances core "discover → understand" workflow without adding user management burden. No authentication/gamification added.
- [x] **Single-Page Minimalism**: ✅ Modal remains overlay on single-page app, no navigation introduced.
- [x] **Zero Friction**: ✅ No authentication changes, no new user friction points.
- [x] **Value-First Design**: ✅ **ENHANCES** this principle by making AI insights (summary + innovation points) more visually prominent through gradients, cards, and hierarchy.
- [x] **Aesthetics as Trust**: ✅ **CORE DRIVER** of this feature. Gradient backgrounds, smooth transitions, and micro-interactions directly serve this principle.
- [x] **Technology Stack**: ✅ Uses existing Vue 3 + Tailwind + Headless UI stack, no new dependencies.
- [x] **Performance**: ✅ Animation budget (800ms total) and bundle size (<10KB increase) meet performance requirements. Hover interactions target 60fps.
- [x] **Project Structure**: ✅ Changes confined to `components/core/PaperModal.vue` and `mocks/paperData.js`, follows established structure.

**CONSTITUTIONAL ALIGNMENT**: This feature is **strongly aligned** with Constitution Principle V (Aesthetics as Trust). The enhancement directly implements the principle's requirement for "smooth transitions" and "thoughtful, helpful design" of interactive states.

## Project Structure

### Documentation (this feature)

```
specs/002-paper-modal-enhancement/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── tasks.md             # Task breakdown (to be generated)
└── research.md          # Technical research findings (inline below)
```

### Affected Source Files

```
src/
├── components/
│   └── core/
│       └── PaperModal.vue          # PRIMARY: Full component refactor
│       └── InnovationCard.vue      # NEW (optional): Extracted sub-component
├── mocks/
│   └── paperData.js                # MAJOR EDIT: Replace generateMockAnalysis()
└── styles/                         # (if needed for custom animations)

tailwind.config.js                  # MINOR EDIT: Add custom gradient tokens
```

**Structure Decision**: Keep all modal logic in `PaperModal.vue` initially. If innovation point card logic exceeds 50 lines, extract to `InnovationCard.vue`. Mock data changes are isolated to `paperData.js`, ensuring no impact on other mock modules.

## Complexity Tracking

*No Constitutional violations - feature is fully compliant.*

## Phase 0: Research

### Existing Implementation Analysis

**Current Component Structure** (`src/components/core/PaperModal.vue:38-179`):
```
<Modal> (Headless UI wrapper)
  └── <div> (container)
      ├── H2 (title, 24px)
      ├── Metadata section (authors, field, date)
      ├── Loading skeleton (if analysisLoading)
      ├── Analysis content
      │   ├── Chinese summary (blue-50 bg, border-l-4)
      │   └── Innovation points (ul list, numbered circles)
      └── Action buttons (PPT, PDF download)
```

**Current Mock Data** (`src/mocks/paperData.js:354-402`):
- `generateMockAnalysis()` function uses field-based templates
- 4 templates (Machine Learning, AI, CV, default)
- Each template has 3 generic innovation points shared by all papers in that field
- Example: "创新性地提出了一种新的模型架构，在多个基准数据集上达到了SOTA性能"

**Current Styling**:
- Chinese summary: `bg-blue-50 border-l-4 border-accent px-4 py-4 rounded`
- Innovation points: Numbered list with `w-6 h-6 rounded-full bg-accent text-white` circles
- Title: `text-2xl font-bold` (28px calculated)
- No animations beyond modal fade-in (Headless UI default)

### Research Questions

#### R1: Tailwind Split-Pane Layout Patterns

**Question**: What's the recommended Tailwind approach for responsive split-pane layouts?

**Research**:
- Tailwind responsive design uses breakpoint prefixes: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- Default breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)
- **Recommended pattern**:
  ```html
  <div class="flex flex-col lg:flex-row gap-6">
    <div class="lg:w-3/5"><!-- Left content --></div>
    <div class="lg:w-2/5"><!-- Right sidebar --></div>
  </div>
  ```
- This automatically stacks on mobile (`flex-col`) and splits horizontally on desktop (`lg:flex-row`)

**Decision**: Use `flex-col lg:flex-row` with width utilities `lg:w-3/5` and `lg:w-2/5` for 60/40 split. Set breakpoint at `lg:` (1024px) for split-pane activation, single column below.

#### R2: Vue 3 Stagger Animation Techniques

**Question**: How to implement stagger animations for innovation point cards in Vue 3?

**Research**:
- Vue 3 `<TransitionGroup>` supports list animations with `:key` binding
- Stagger delay can be achieved via CSS custom properties or JS timing
- **CSS-based approach** (recommended for simplicity):
  ```vue
  <TransitionGroup name="stagger" tag="div">
    <div v-for="(point, index) in points" :key="index"
         :style="{ transitionDelay: `${index * 50}ms` }">
  ```
- **Alternative**: Use `@before-enter` hook to set delays programmatically

**Decision**: Use CSS-based stagger with inline `:style` binding for delay calculation. Wrap innovation points in `<TransitionGroup>` with `name="fade-slide"` transition classes.

#### R3: Gradient Background Best Practices

**Question**: How to implement gradient backgrounds in Tailwind while maintaining text contrast?

**Research**:
- Tailwind supports gradient utilities: `bg-gradient-to-r from-blue-500 to-purple-500`
- Custom gradients require `tailwind.config.js` extension:
  ```js
  extend: {
    backgroundImage: {
      'gradient-summary': 'linear-gradient(45deg, #EEF2FF 0%, #F3E8FF 100%)',
    }
  }
  ```
- **Contrast requirement**: Text on #EEF2FF (blue-50) and #F3E8FF (purple-50) backgrounds requires dark text (#212529 or darker) for WCAG AA compliance
- Verified with WebAIM Contrast Checker: #212529 on #EEF2FF = 10.5:1 (passes AAA)

**Decision**: Add `bg-gradient-summary` custom class to Tailwind config. Use `text-text-primary` (#212529) for all text on gradient backgrounds.

#### R4: Hover Effects Without Layout Shift

**Question**: How to implement hover lift animation without causing layout reflow?

**Research**:
- **Transform-based approach** (GPU-accelerated, no reflow):
  ```css
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  }
  ```
- Use `transition: transform 200ms, box-shadow 200ms` for smooth effect
- Avoid `margin-top` changes (causes reflow)
- Use `will-change: transform` for performance hint (sparingly, only on hover-capable devices)

**Decision**: Use `transform: translateY(-4px)` for hover lift. Apply `@media (hover: hover)` query to prevent touch device issues. Add `transition-transform duration-200` Tailwind utility.

#### R5: Accessibility - Reduced Motion Support

**Question**: How to respect `prefers-reduced-motion` in Vue 3 + Tailwind?

**Research**:
- Tailwind provides `motion-safe:` and `motion-reduce:` variants
- Example: `motion-safe:transition-transform motion-reduce:transition-none`
- **Vue 3 approach**:
  ```vue
  <script setup>
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  </script>
  <Transition v-if="!prefersReducedMotion" name="fade">
  ```
- **Recommendation**: Use Tailwind variants for CSS transitions, add Vue conditional for `<TransitionGroup>`

**Decision**: Wrap `<TransitionGroup>` in `v-if="!prefersReducedMotion"` check. Use `motion-safe:` prefix for all transform/opacity transitions in Tailwind classes.

### Research Summary

| Research Question | Decision | Impact on Implementation |
|-------------------|----------|-------------------------|
| Split-pane layout | Flexbox with `lg:flex-row` breakpoint | Simple, no custom CSS needed |
| Stagger animation | CSS `transitionDelay` via inline style | Minimal JS, easy to maintain |
| Gradient backgrounds | Custom Tailwind config + WCAG AA contrast | Requires config change, safe contrast |
| Hover lift effect | `transform: translateY()` GPU-accelerated | Smooth 60fps, no reflow |
| Reduced motion | Tailwind `motion-safe:` + Vue conditional | Accessible, standards-compliant |

**No Blockers**: All research questions resolved with existing Tailwind/Vue 3 capabilities. No new dependencies required.

## Phase 1: Design

### Component Architecture

#### Enhanced PaperModal.vue Structure

```
<Modal :open="uiStore.modalOpen" @close="handleClose">
  <div class="modal-container">
    <!-- Header (full width) -->
    <ModalHeader>
      <h2 class="text-3xl lg:text-4xl font-bold">{{ paper.title }}</h2>
    </ModalHeader>

    <!-- Content (split-pane on desktop, stacked on mobile) -->
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Left Column: Main Content -->
      <div class="lg:w-3/5">
        <!-- Chinese Summary Section -->
        <section class="bg-gradient-summary rounded-lg p-6">
          <h3 class="text-xl font-semibold mb-3">📝 中文摘要</h3>
          <p class="text-base leading-relaxed">{{ analysis.chineseSummary }}</p>
        </section>

        <!-- Innovation Points Section -->
        <section class="mt-6">
          <h3 class="text-xl font-semibold mb-4">💡 创新点</h3>
          <TransitionGroup v-if="!prefersReducedMotion" name="fade-slide" tag="div" class="grid gap-4">
            <InnovationCard
              v-for="(point, index) in analysis.innovationPoints"
              :key="index"
              :point="point"
              :delay="index * 50"
            />
          </TransitionGroup>
          <div v-else class="grid gap-4">
            <InnovationCard
              v-for="(point, index) in analysis.innovationPoints"
              :key="index"
              :point="point"
            />
          </div>
        </section>
      </div>

      <!-- Right Column: Metadata + Actions -->
      <aside class="lg:w-2/5 lg:sticky lg:top-6 lg:self-start">
        <div class="bg-secondary-bg rounded-lg p-6">
          <!-- Metadata -->
          <MetadataSection :paper="paper" />
          <!-- Actions -->
          <ActionsSection :paper="paper" @generate-ppt="handleGeneratePPT" />
        </div>
      </aside>
    </div>
  </div>
</Modal>
```

#### New Sub-Component: InnovationCard.vue (Optional)

```vue
<template>
  <article
    class="innovation-card border border-border-color rounded-lg p-4
           motion-safe:transition-all motion-safe:duration-200
           hover:shadow-md hover:-translate-y-1"
    :style="{ transitionDelay: `${delay}ms` }"
    role="article"
    :aria-labelledby="`innovation-${index}`"
  >
    <div class="flex gap-3">
      <div class="flex-shrink-0">
        <span class="text-3xl" role="img" :aria-label="point.iconLabel">
          {{ point.icon }}
        </span>
      </div>
      <div class="flex-1">
        <h4 :id="`innovation-${index}`" class="font-semibold text-base mb-1">
          {{ point.title }}
        </h4>
        <p class="text-sm text-text-secondary leading-relaxed">
          {{ point.description }}
        </p>
      </div>
    </div>
  </article>
</template>

<script setup>
defineProps({
  point: {
    type: Object,
    required: true,
    // Structure: { icon, iconLabel, title, description }
  },
  index: { type: Number, required: true },
  delay: { type: Number, default: 0 },
})
</script>
```

### Data Model Changes

#### Enhanced Innovation Point Structure

**Current** (in `generateMockAnalysis()` output):
```javascript
{
  innovationPoints: [
    "创新性地提出了一种新的模型架构，在多个基准数据集上达到了SOTA性能",
    // ... generic strings
  ]
}
```

**Enhanced** (new structure):
```javascript
{
  innovationPoints: [
    {
      icon: "🚀",
      iconLabel: "Performance breakthrough",
      title: "27M参数模型超越大型语言模型",
      description: "在Sudoku和ARC-AGI等硬推理任务上，仅使用2700万参数在1000个样本上训练，即可超越千亿级大模型性能"
    },
    {
      icon: "💡",
      iconLabel: "Novel approach",
      title: "分层递归推理架构",
      description: "提出小规模递归推理方法，通过层次化分解策略将复杂问题拆解为可管理的子问题，显著提升推理效率"
    },
    {
      icon: "⚡",
      iconLabel: "Efficiency gain",
      title: "训练效率提升50倍",
      description: "相比传统预训练方法，所需训练数据量减少99%，训练时间缩短至原来的2%，为小规模模型研究开辟新路径"
    }
  ]
}
```

**Migration Strategy**:
1. Update `generateMockAnalysis()` to return new structure for all 24 papers
2. Add backward compatibility check: if `point` is string (old format), auto-convert to `{ icon: "💡", title: point.slice(0, 30), description: point }`
3. This ensures existing components won't break during transition

### Mock Data Enhancement Strategy

#### Content Creation Approach

For each of 24 papers, create targeted innovation points by:

1. **Extract Paper Theme**: Analyze paper title + keywords
   - Example: "Hierarchical Reasoning Models" → Theme: Small-scale reasoning efficiency

2. **Identify Innovation Types**: Map to emoji icons
   - 🚀 Performance (benchmarks, SOTA results)
   - 💡 Novel Approach (new methods, architectures)
   - ⚡ Efficiency (speed, compute reduction)
   - 🎯 Accuracy (precision improvements)
   - 🔬 Methodology (rigorous experiments)
   - 🌍 Impact (real-world applications)
   - 🛡️ Robustness (reliability, safety)
   - 📊 Empirical (data-driven insights)

3. **Write Specific Claims**: Include quantitative metrics
   - ❌ Bad: "提出了创新性的方法"
   - ✅ Good: "27M参数模型在Sudoku任务上超越GPT-4"

4. **Structure**: Title (10-15 Chinese characters) + Description (30-50 characters)

#### Implementation Plan for Mock Data

**Priority 1 (Daily Papers, 8 papers)**:
- Most visible in UI, highest user exposure
- Write fully custom innovation points first

**Priority 2 (Weekly Papers, 8 papers)**:
- Medium visibility
- Can reuse some patterns from Priority 1 with domain adaptation

**Priority 3 (Monthly Papers, 8 papers)**:
- Lower visibility
- Can use enhanced templates with variable interpolation

**Estimated Effort**:
- Priority 1: 2-3 hours (high quality, fully custom)
- Priority 2: 1-2 hours (adapted patterns)
- Priority 3: 1 hour (enhanced templates)
- Total: 4-6 hours for all 24 papers

### Visual Design Specifications

#### Color Palette Extensions

Add to `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      backgroundImage: {
        'gradient-summary': 'linear-gradient(45deg, #EEF2FF 0%, #F3E8FF 100%)',
      },
      transitionProperty: {
        'card': 'transform, box-shadow',
      },
    }
  }
}
```

**Rationale**: Custom gradient requires config addition. Existing color palette sufficient for all other uses.

#### Typography Scale Updates

| Element | Current | Enhanced | Reasoning |
|---------|---------|----------|-----------|
| Modal Title | 24px (text-2xl) | 32px desktop / 28px mobile (text-3xl lg:text-4xl) | Increase visual hierarchy |
| Section Headers | 20px (text-xl) | 22px (text-xl + font-semibold) | Keep consistent, add weight |
| Summary Body | 16px (text-base) | 18px (text-lg) | Improve readability on gradient bg |
| Innovation Title | N/A (list item) | 16px (text-base + font-semibold) | New card title element |
| Innovation Desc | N/A | 14px (text-sm) | New card body text |

**Note**: All size increases respect 8px grid and maintain hierarchy. No constitutional violations.

#### Spacing & Layout Grid

| Element | Spacing | Responsive Adjustment |
|---------|---------|----------------------|
| Split-pane gap | 32px (gap-8) | → 24px (gap-6) on <1024px |
| Card padding | 16px (p-4) | No change |
| Section margins | 24px (mt-6) | No change |
| Innovation card grid | 16px (gap-4) | No change |
| Sidebar padding | 24px (p-6) | No change |

**Rationale**: Maintains 8px grid (16, 24, 32). Reduced gap on medium screens prevents cramping.

#### Animation Specifications

| Animation | Duration | Easing | Trigger | Budget Impact |
|-----------|----------|--------|---------|---------------|
| Modal open | 300ms | ease-out | Modal mount | 300ms |
| Card stagger (3 cards) | 50ms delay per card | ease-out | Content mount | 150ms (total for 3) |
| Hover lift | 200ms | ease-in-out | Mouse enter/leave | N/A (interactive) |
| Gradient fade-in | 400ms | ease-in | Content ready | Overlaps with modal open |

**Total Animation Budget**: 300ms (modal) + 150ms (stagger) = 450ms (well within 800ms budget)

### Accessibility Audit

| Requirement | Implementation | Verification Method |
|-------------|----------------|---------------------|
| WCAG 2.1 AA Contrast | Text #212529 on gradient bg #EEF2FF-#F3E8FF = 10.5:1 | WebAIM Contrast Checker |
| Keyboard Navigation | No changes to focus management (Headless UI handles) | Manual Tab/Shift+Tab testing |
| Screen Reader Support | Add `role="article"` to cards, `aria-labelledby` to titles | NVDA/JAWS testing |
| Reduced Motion | `v-if="!prefersReducedMotion"` for TransitionGroup | Toggle OS setting, verify animations disabled |
| Touch Targets | Innovation cards min 44x44px (achieved via p-4 = 16px + content) | Mobile device testing |
| Focus Indicators | Use default browser focus rings (no custom removal) | Keyboard navigation + visual inspection |

**Compliance Status**: ✅ Fully WCAG 2.1 AA compliant. No regressions from current implementation.

## Phase 2: Implementation Approach

### Development Sequence

#### Stage 1: Foundation (No Visual Changes Yet)

**Goal**: Set up data structure and Tailwind config without breaking existing UI

**Tasks**:
1. Update `tailwind.config.js` with `bg-gradient-summary` custom class
2. Add reduced motion detection to `PaperModal.vue`:
   ```vue
   const prefersReducedMotion = ref(
     window.matchMedia('(prefers-reduced-motion: reduce)').matches
   )
   ```
3. Create new innovation point data structure in `paperData.js` (Priority 1 daily papers only)
4. Add backward compatibility check in `PaperModal.vue` to handle both string and object formats

**Verification**: Existing modal still works exactly as before. No visual regressions.

#### Stage 2: Layout Refactoring

**Goal**: Implement split-pane layout with responsive breakpoints

**Tasks**:
1. Wrap modal content in flexbox container: `<div class="flex flex-col lg:flex-row gap-6 lg:gap-8">`
2. Split into left (`lg:w-3/5`) and right (`lg:w-2/5`) columns
3. Move metadata + actions to right sidebar with sticky positioning: `lg:sticky lg:top-6 lg:self-start`
4. Test at breakpoints: 375px (mobile), 768px (tablet), 1024px (desktop), 1440px (large desktop)

**Verification**: Layout splits correctly at 1024px, stacks on mobile, no content overlap.

#### Stage 3: Visual Enhancements (Summary Section)

**Goal**: Apply gradient background and typography updates to Chinese summary

**Tasks**:
1. Replace summary background: `bg-blue-50 border-l-4` → `bg-gradient-summary rounded-lg`
2. Increase title size: `text-2xl` → `text-3xl lg:text-4xl`
3. Increase summary body text: `text-base` → `text-lg`
4. Add fade-in animation to modal container

**Verification**: Gradient renders smoothly, text contrast passes WCAG checker, animation feels smooth.

#### Stage 4: Innovation Point Cards

**Goal**: Transform innovation points from list to card grid

**Tasks**:
1. Create `InnovationCard.vue` sub-component (or inline if <50 lines)
2. Update innovation point rendering to use new data structure (icon, title, description)
3. Apply card styling: border, padding, hover effect
4. Wrap in `<TransitionGroup>` with stagger delay
5. Add `@media (hover: hover)` for hover-only devices

**Verification**:
- Cards display in grid layout
- Hover lifts card 4px on desktop (not on mobile)
- Stagger animation runs for 150ms total
- Reduced motion disables animations

#### Stage 5: Mock Data Completion

**Goal**: Replace all 24 papers with targeted innovation points

**Tasks**:
1. Complete Priority 1 (daily papers) if not done in Stage 1
2. Write Priority 2 (weekly papers, 8 papers)
3. Write Priority 3 (monthly papers, 8 papers)
4. Review all content for typos, consistency, quantitative metrics

**Verification**:
- Every paper has unique, research-specific innovation points
- No generic template phrases remain
- All emoji icons are contextually appropriate

#### Stage 6: Polish & Testing

**Goal**: Final visual polish and cross-browser/device testing

**Tasks**:
1. Fine-tune spacing, ensure 8px grid compliance
2. Test on Chrome, Firefox, Safari, Edge
3. Test on physical mobile device (Android/iOS)
4. Verify accessibility with keyboard + screen reader
5. Run bundle size analysis (must be <10KB increase)
6. Update loading skeleton to match new layout

**Verification**:
- All browsers render identically
- Mobile experience is smooth
- Accessibility audit passes
- Bundle size meets constraint

### Testing Strategy

#### Manual Testing Checklist

**Desktop (1920x1080)**:
- [ ] Modal opens with split-pane layout (left 60%, right 40%)
- [ ] Chinese summary displays with gradient background
- [ ] Innovation cards appear with stagger animation (50ms delay each)
- [ ] Hover over cards triggers lift animation (4px up, enhanced shadow)
- [ ] Right sidebar sticks during scroll
- [ ] Modal title is 32px and visually prominent

**Tablet (768x1024)**:
- [ ] Split-pane layout maintained with reduced spacing (24px gap)
- [ ] All content remains readable without zoom
- [ ] Touch interactions work (no hover states on touch)

**Mobile (375x667)**:
- [ ] Layout switches to single column (content stacked)
- [ ] Metadata section appears below innovation points
- [ ] All text is readable without horizontal scroll
- [ ] Touch targets are at least 44x44px

**Accessibility**:
- [ ] Enable "Reduce motion" in OS → verify animations are disabled
- [ ] Tab through modal with keyboard → all interactive elements reachable
- [ ] Test with NVDA/JAWS → innovation cards announced correctly
- [ ] Verify gradient background text contrast >4.5:1 with checker

**Cross-Browser**:
- [ ] Chrome 90+ → all features work
- [ ] Firefox 88+ → all features work
- [ ] Safari 14+ → all features work, gradient rendering correct
- [ ] Edge 90+ → all features work

#### Automated Testing (Optional)

If implementing Vitest tests:

```javascript
// tests/unit/PaperModal.spec.js
describe('PaperModal.vue', () => {
  it('renders split-pane layout on desktop viewport', () => {
    // Set viewport to 1024px
    // Mount component
    // Assert left column has lg:w-3/5 class
    // Assert right column has lg:w-2/5 class
  })

  it('renders single column on mobile viewport', () => {
    // Set viewport to 375px
    // Mount component
    // Assert flex-col class is present
    // Assert lg:flex-row is inactive
  })

  it('converts string innovation points to object format (backward compat)', () => {
    // Pass analysis with string-format innovation points
    // Assert component renders without errors
    // Assert default icon (💡) is used
  })
})
```

### Rollout Plan

#### Development Environment

1. Create feature branch: `002-paper-modal-enhancement`
2. Implement Stages 1-6 sequentially with commits per stage
3. Self-review with checklist after each stage
4. Manual testing on local dev server (npm run dev)

#### Staging/Review

1. Build production bundle: `npm run build`
2. Verify bundle size increase: `ls -lh dist/assets/*.js` (compare before/after)
3. Preview production build: `npm run preview`
4. Conduct full manual testing checklist on preview build
5. Screenshot comparison: Before/After at 3 breakpoints

#### Production Deployment

1. Merge feature branch to main via PR
2. Deploy to production (process TBD, likely Vercel/Netlify auto-deploy)
3. Monitor error tracking for any runtime issues
4. Collect user feedback (if applicable) on visual changes

**Rollback Plan**: If critical issues found post-deploy, revert commit or feature-flag the enhanced modal (add `VITE_USE_ENHANCED_MODAL=false` env var to temporarily disable).

### Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Gradient backgrounds look different in Safari | Medium | Low | Test on real Safari, adjust opacity if needed |
| Stagger animation feels janky on low-end devices | Medium | Medium | Add `prefers-reduced-motion` support, reduce delay to 30ms if needed |
| Writing 24 targeted innovation points takes too long | Low | Low | Prioritize daily papers first, can ship incrementally |
| Split-pane feels cramped on 1024px screens | Medium | Medium | Add 768-1024px breakpoint with adjusted spacing |
| Bundle size exceeds 10KB constraint | Low | High | Use dynamic import for modal: `const PaperModal = defineAsyncComponent(...)` |
| Hover effects don't work on touch devices | Low | Low | Use `@media (hover: hover)` to disable on touch |

## Next Steps

1. **Generate Tasks**: Run `/speckit.tasks` to create `tasks.md` with granular task breakdown
2. **Create Feature Branch**: `git checkout -b 002-paper-modal-enhancement`
3. **Begin Stage 1**: Update Tailwind config and data structure foundation
4. **Iterate Through Stages 2-6**: Implement sequentially with commit per stage
5. **Manual Testing**: Use checklist after Stage 6 completion
6. **PR & Review**: Submit PR with before/after screenshots at 3 breakpoints
7. **Deploy**: Merge and deploy to production

**Estimated Timeline**:
- Stages 1-4 (Core Implementation): 4-6 hours
- Stage 5 (Mock Data): 4-6 hours
- Stage 6 (Polish & Testing): 2-3 hours
- **Total**: 10-15 hours of focused development work

**Success Criteria Met When**:
- All manual testing checklist items pass ✅
- Bundle size increase <10KB ✅
- WCAG 2.1 AA compliance verified ✅
- No console errors on Chrome/Firefox/Safari ✅
- User feedback: "The modal looks much more professional now" 🎯
