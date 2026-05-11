# Utilities Reference

Helper functions, configuration files, and utility modules.

---

## PPT Rendering

### pptRenderer.js

**Location**: `src/utils/pptRenderer.js`

**Purpose**: Convert Markdown to safe HTML with LaTeX formulas and code highlighting.

**Pipeline**:
```
Markdown → marked.parse() → KaTeX extension → highlight.js → DOMPurify → Safe HTML
```

**Functions**:

#### `parseSlides(markdown)`
Split Markdown into individual slides.

**Parameters**:
- `markdown`: `string` - Full PPT content

**Returns**: `string[]` - Array of slide Markdown strings

**Delimiter**: `---` (triple dash on its own line)

**Example**:
```javascript
const slides = parseSlides(`
# Slide 1

Content 1

---

# Slide 2

Content 2
`)
// Returns: ['# Slide 1\n\nContent 1', '# Slide 2\n\nContent 2']
```

---

#### `renderMarkdown(markdown)`
Render Markdown to safe HTML.

**Parameters**:
- `markdown`: `string` - Slide Markdown

**Returns**: `string` - Safe HTML string

**Features**:
- **KaTeX**: Renders LaTeX formulas (`$...$` inline, `$$...$$` block)
- **highlight.js**: Syntax highlighting for 7 languages (js, python, java, cpp, go, rust, bash)
- **DOMPurify**: XSS protection with KaTeX MathML whitelist

**Usage**:
```javascript
import { renderMarkdown } from '@/utils/pptRenderer'

const html = renderMarkdown('# Title\n\n$$E = mc^2$$\n\n```python\nprint("Hello")\n```')
```

---

### Supported Languages (highlight.js)

| Language | Code Fence | File Extension |
|----------|-----------|----------------|
| JavaScript | ```javascript | .js |
| Python | ```python | .py |
| Java | ```java | .java |
| C++ | ```cpp | .cpp |
| Go | ```go | .go |
| Rust | ```rust | .rs |
| Bash | ```bash | .sh |

---

### LaTeX Formula Syntax

**Inline Formula**: `$formula$`
```markdown
Einstein's famous equation is $E = mc^2$.
```

**Block Formula**: `$$formula$$`
```markdown
The quadratic formula:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
```

**Common LaTeX Commands**:
- Fractions: `\frac{numerator}{denominator}`
- Square root: `\sqrt{x}`
- Subscript: `x_i`
- Superscript: `x^2`
- Greek letters: `\alpha`, `\beta`, `\theta`
- Summation: `\sum_{i=1}^{n}`
- Integrals: `\int_{a}^{b}`

---

## Configuration Files

### pptImages.js

**Location**: `src/config/pptImages.js`

**Purpose**: Generate PPT slide image URLs.

**Constants**:
```javascript
const PAPER_IMAGE_DIRS = {
  'daily-0001': '/ppt-images/daily-0001',
  'daily-0002': '/ppt-images/daily-0002',
  // ... daily-0008
}

const IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
```

**Functions**:

#### `getSlideImageUrl(paperId, slideIndex, ext = 'png')`
Get URL for a specific slide image.

**Parameters**:
- `paperId`: `string` - Paper ID (e.g., 'daily-0001')
- `slideIndex`: `number` - Slide number (1-based)
- `ext`: `string` - Image extension (default: 'png')

**Returns**: `string` - Image URL

**Example**:
```javascript
getSlideImageUrl('daily-0001', 1)
// Returns: '/ppt-images/daily-0001/slide-1.png'
```

---

#### `getAllSlideUrls(paperId, totalSlides)`
Get URLs for all slides in a PPT.

**Parameters**:
- `paperId`: `string` - Paper ID
- `totalSlides`: `number` - Total number of slides

**Returns**: `Array<{index: number, url: string}>` - Slide objects

**Example**:
```javascript
getAllSlideUrls('daily-0001', 3)
// Returns: [
//   { index: 1, url: '/ppt-images/daily-0001/slide-1.png' },
//   { index: 2, url: '/ppt-images/daily-0001/slide-2.png' },
//   { index: 3, url: '/ppt-images/daily-0001/slide-3.png' }
// ]
```

---

### watermark.js

**Location**: `src/config/watermark.js`

**Purpose**: Watermark configuration from environment variables.

**Configuration**:
```javascript
export const watermarkConfig = {
  enabled: import.meta.env.VITE_WATERMARK_ENABLED === 'true',
  text: import.meta.env.VITE_WATERMARK_TEXT || '论导Lite - lundao.com',
  opacity: parseFloat(import.meta.env.VITE_WATERMARK_OPACITY) || 0.08,
  fontSize: '16px',
  color: '#000000'
}
```

**Environment Variables** (`.env.development`):
```env
VITE_WATERMARK_ENABLED=true
VITE_WATERMARK_TEXT="论导Lite 预览版 - lundao.com"
VITE_WATERMARK_OPACITY=0.08
```

**Usage**:
```vue
<script setup>
import { watermarkConfig } from '@/config/watermark'
</script>

<template>
  <Watermark
    v-if="watermarkConfig.enabled"
    :text="watermarkConfig.text"
    :opacity="watermarkConfig.opacity"
  />
</template>
```

---

## File Validation

### File Type Check

```javascript
const isValidPDF = (file) => {
  return file.type === 'application/pdf'
}
```

**MIME Types**:
- PDF: `application/pdf`

---

### File Size Check

```javascript
const MAX_FILE_SIZE = 20 * 1024 * 1024  // 20 MB

const isValidSize = (file) => {
  return file.size <= MAX_FILE_SIZE
}
```

**Size Limits**:
- PDF Upload: 20 MB
- localStorage Quota: ~5 MB (browser-dependent)

---

## Helper Functions

### Format File Size

**Location**: `src/components/core/UploadDropzone.vue`

```javascript
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 10) / 10 + ' ' + sizes[i]
}
```

**Usage**:
```javascript
formatFileSize(1024)        // '1 KB'
formatFileSize(2048576)     // '2 MB'
formatFileSize(10485760)    // '10 MB'
```

---

### Delay Promise

**Location**: `src/mocks/utils.js`

```javascript
export const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))
```

**Usage**:
```javascript
import { delay } from '@/mocks/utils'

// Simulate network delay
await delay(500)
console.log('500ms passed')
```

---

### Generate Mock Task ID

**Location**: `src/mocks/utils.js`

```javascript
export const generateMockTaskId = () => {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(7)
  return `mock-task-${timestamp}-${random}`
}
```

**Format**: `mock-task-{timestamp}-{random6chars}`

**Example**:
```javascript
generateMockTaskId()
// Returns: 'mock-task-1705300123456-a3f8e9'
```

---

## Security Utilities

### XSS Protection (DOMPurify)

**Configuration**:
```javascript
import DOMPurify from 'dompurify'

// Whitelist KaTeX-generated MathML tags
const cleanHTML = DOMPurify.sanitize(html, {
  ADD_TAGS: ['math', 'mrow', 'mi', 'mn', 'mo', 'msup', 'msub'],
  ADD_ATTR: ['xmlns']
})
```

**Protected Against**:
- `<script>` tags
- `<iframe>` embeds
- `onerror`, `onclick`, etc. event handlers
- JavaScript protocols (`javascript:`)

---

### Content Security Policy (Recommended)

**Production `index.html`**:
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-eval';
  style-src 'self' 'unsafe-inline' fonts.googleapis.com;
  font-src 'self' fonts.gstatic.com;
  img-src 'self' data:;
">
```

---

## Performance Utilities

### Image Lazy Loading

**Pattern** (Future Enhancement):
```vue
<img
  :src="slideUrl"
  loading="lazy"
  @load="handleImageLoad"
/>
```

---

### localStorage Quota Handling

**Pattern** (from `useTaskHistory.js`):
```javascript
try {
  localStorage.setItem('lundao-tasks', JSON.stringify(data))
} catch (err) {
  if (err.name === 'QuotaExceededError') {
    // Auto-prune oldest tasks
    const pruned = tasks.slice(0, 50)
    localStorage.setItem('lundao-tasks', JSON.stringify(pruned))
  }
}
```

---

## Date Formatting

### ISO Timestamp

```javascript
const timestamp = new Date().toISOString()
// '2025-11-17T12:34:56.789Z'
```

### Relative Time (Future Enhancement)

```javascript
const formatRelativeTime = (timestamp) => {
  const diff = Date.now() - new Date(timestamp).getTime()
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}
```

---

**Last Updated**: 2025-11-17  
**See Also**: [Components](./components.md), [API Services](./api-services.md)
