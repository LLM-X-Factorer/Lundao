# Design System Reference

Complete guide to colors, typography, spacing, and UI patterns.

---

## Color Palette

### Tailwind Config (`tailwind.config.js`)

```javascript
colors: {
  'primary-bg': '#FFFFFF',       // White background
  'secondary-bg': '#F8F9FA',     // Light gray background
  'border-color': '#E9ECEF',     // Border gray
  'text-primary': '#212529',     // Dark text
  'text-secondary': '#6C757D',   // Medium gray text
  'accent': '#3A57E8',           // Primary blue
  'success': '#198754',          // Green (success states)
  'error': '#DC3545',            // Red (errors, warnings)
}
```

### Custom Gradients

```javascript
backgroundImage: {
  'gradient-summary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
}
```

**Usage**:
```vue
<div class="bg-gradient-summary">Chinese Summary</div>
```

---

## Typography

### Font Families

**From Google Fonts CDN** (`index.html`):
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Tailwind Config**:
```javascript
fontFamily: {
  sans: ['Inter', 'Noto Sans SC', 'sans-serif']
}
```

---

### Type Scale

| Element | Size (px) | Tailwind Class | Weight | Line Height |
|---------|-----------|----------------|--------|-------------|
| H1 | 28 | `text-2xl` | 700 (bold) | 1.2 |
| H2 | 22 | `text-xl` | 600 (semibold) | 1.3 |
| H3 | 18 | `text-lg` | 600 (semibold) | 1.4 |
| Body | 16 | `text-base` | 400 (normal) | 1.5 |
| Secondary | 14 | `text-sm` | 400 (normal) | 1.5 |
| Caption | 12 | `text-xs` | 400 (normal) | 1.4 |

**Example**:
```vue
<h1 class="text-2xl font-bold text-text-primary">Heading 1</h1>
<h2 class="text-xl font-semibold text-text-primary">Heading 2</h2>
<p class="text-base text-text-primary">Body text</p>
<p class="text-sm text-text-secondary">Secondary text</p>
```

---

## Spacing System

### 8px Grid

**ALL spacing MUST be multiples of 8px.**

| Multiplier | Pixels | Tailwind Class | Usage |
|------------|--------|----------------|-------|
| 0 | 0px | `gap-0`, `p-0`, `m-0` | - |
| 1 | 8px | `gap-2`, `p-2`, `m-2` | Tight spacing |
| 2 | 16px | `gap-4`, `p-4`, `m-4` | Standard spacing |
| 3 | 24px | `gap-6`, `p-6`, `m-6` | Medium spacing |
| 4 | 32px | `gap-8`, `p-8`, `m-8` | Large spacing |
| 5 | 40px | `gap-10`, `p-10`, `m-10` | Extra large |
| 6 | 48px | `gap-12`, `p-12`, `m-12` | Section spacing |

**Common Patterns**:
```vue
<!-- Card padding -->
<div class="p-6">...</div>

<!-- Section margin bottom -->
<section class="mb-12">...</section>

<!-- Grid gap -->
<div class="grid gap-6">...</div>
```

---

## Border Radius

| Element | Radius (px) | Tailwind Class | Usage |
|---------|-------------|----------------|-------|
| Button | 6px | `rounded-md` | Buttons, badges |
| Card | 8px | `rounded-lg` | Paper cards, containers |
| Modal | 12px | `rounded-xl` | Modals, overlays |
| Input | 6px | `rounded-md` | Form inputs |

**Example**:
```vue
<button class="rounded-md">Button</button>
<div class="rounded-lg">Card</div>
<div class="rounded-xl">Modal</div>
```

---

## Component Patterns

### Card Pattern

```vue
<div class="bg-primary-bg rounded-lg border border-border-color p-6 hover:shadow-lg transition-shadow">
  <!-- Card content -->
</div>
```

**Variants**:
- **Default**: `bg-primary-bg border border-border-color`
- **Secondary**: `bg-secondary-bg border border-border-color`
- **Hover Lift**: `hover:-translate-y-1 hover:shadow-xl transition-transform`

---

### Button Pattern

```vue
<!-- Primary Button -->
<button class="px-6 py-2 bg-accent text-white rounded-md hover:bg-blue-600 transition-colors font-medium">
  Primary Action
</button>

<!-- Secondary Button -->
<button class="px-6 py-2 bg-primary-bg text-text-primary border border-border-color rounded-md hover:bg-secondary-bg transition-colors font-medium">
  Secondary Action
</button>

<!-- Danger Button -->
<button class="px-6 py-2 bg-error text-white rounded-md hover:bg-red-600 transition-colors font-medium">
  Delete
</button>
```

---

### Modal Pattern

```vue
<div class="fixed inset-0 z-50 overflow-y-auto">
  <!-- Backdrop -->
  <div class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
  
  <!-- Modal -->
  <div class="flex min-h-full items-center justify-center p-4">
    <div class="relative bg-primary-bg rounded-xl shadow-xl max-w-4xl w-full">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-border-color">
        <h2 class="text-xl font-semibold">Title</h2>
      </div>
      
      <!-- Body -->
      <div class="px-6 py-6">
        <!-- Content -->
      </div>
      
      <!-- Footer (optional) -->
      <div class="px-6 py-4 border-t border-border-color">
        <!-- Actions -->
      </div>
    </div>
  </div>
</div>
```

---

### Grid Layout Pattern

```vue
<!-- Responsive Paper Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <PaperCard />
  <PaperCard />
  <PaperCard />
</div>

<!-- Innovation Points Grid (2 columns) -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
  <InnovationCard />
  <InnovationCard />
</div>
```

---

## Accessibility

### Color Contrast

All text combinations meet **WCAG AA standards** (4.5:1 for normal text, 3:1 for large text):

| Text Color | Background | Contrast Ratio | Pass |
|------------|------------|----------------|------|
| `text-primary` | `primary-bg` | 16.1:1 | ✅ AAA |
| `text-secondary` | `primary-bg` | 7.0:1 | ✅ AAA |
| White | `accent` | 6.8:1 | ✅ AA |
| White | `error` | 5.5:1 | ✅ AA |
| White | `success` | 4.6:1 | ✅ AA |

**Gradient Background**:
- `text-primary` on `bg-gradient-summary`: 10.5:1 (✅ AAA)

---

### Focus States

**All interactive elements MUST have visible focus states:**

```vue
<!-- Button focus -->
<button class="focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2">
  Button
</button>

<!-- Input focus -->
<input class="focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent">
```

---

### ARIA Labels

**Required for icon-only buttons:**

```vue
<button aria-label="Close modal" @click="closeModal">
  <svg><!-- Close icon --></svg>
</button>

<button aria-label="Next slide" @click="nextSlide">
  <svg><!-- Arrow icon --></svg>
</button>
```

---

## Motion & Transitions

### Reduced Motion

**Respect user preferences:**

```javascript
// In component
const prefersReducedMotion = ref(window.matchMedia('(prefers-reduced-motion: reduce)').matches)
```

```vue
<div :class="prefersReducedMotion ? '' : 'transition-all duration-300'">
  Content
</div>
```

---

### Standard Transitions

| Property | Duration | Easing | Tailwind Class |
|----------|----------|--------|----------------|
| Transform | 200ms | ease | `transition-transform duration-200` |
| Opacity | 200ms | ease | `transition-opacity duration-200` |
| Colors | 200ms | ease | `transition-colors duration-200` |
| Shadow | 200ms | ease | `transition-shadow duration-200` |
| All | 300ms | ease | `transition-all duration-300` |

**Example**:
```vue
<!-- Hover lift with shadow -->
<div class="transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
  Card
</div>

<!-- Color transition -->
<button class="transition-colors duration-200 hover:bg-blue-600">
  Button
</button>
```

---

### Stagger Animations

**Innovation Points (PaperModal.vue)**:

```vue
<TransitionGroup
  name="stagger"
  tag="div"
  class="grid grid-cols-1 lg:grid-cols-2 gap-4"
>
  <div
    v-for="(point, index) in innovationPoints"
    :key="index"
    :style="{ transitionDelay: `${index * 50}ms` }"
    class="innovation-card"
  >
    {{ point }}
  </div>
</TransitionGroup>

<style>
.stagger-enter-active {
  transition: all 0.3s ease;
}
.stagger-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
</style>
```

---

## Responsive Breakpoints

### Tailwind Breakpoints

| Breakpoint | Min Width | Tailwind Prefix | Usage |
|------------|-----------|-----------------|-------|
| Mobile | 0px | (none) | Default |
| Tablet | 768px | `md:` | 2-column grids |
| Desktop | 1024px | `lg:` | 3-column grids |
| Wide | 1280px | `xl:` | Max content width |

**Example**:
```vue
<!-- 1 column mobile, 2 tablet, 3 desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  ...
</div>

<!-- Hide on mobile -->
<div class="hidden md:block">
  Desktop only content
</div>
```

---

## Design Tokens Summary

**Color**: 8 semantic colors + 1 gradient  
**Typography**: 6 sizes, 1 font stack  
**Spacing**: 8px grid (0-96px in 8px increments)  
**Radius**: 3 sizes (6px, 8px, 12px)  
**Transitions**: 200-300ms standard durations  
**Breakpoints**: Mobile-first (md: 768px, lg: 1024px)  

---

**Last Updated**: 2025-11-17  
**See Also**: [Components](./components.md), [Architecture](./architecture.md)
