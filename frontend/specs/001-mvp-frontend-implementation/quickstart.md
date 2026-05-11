# Quickstart Guide: Local Development Setup

**Feature**: 论导Lite MVP Frontend
**Date**: 2025-10-14
**Phase**: 1 - Design

## Prerequisites

Ensure you have the following installed:

- **Node.js**: v18.x or later (v20.x recommended)
- **npm**: v9.x or later
- **Git**: Latest version
- **Code Editor**: VS Code recommended with extensions:
  - Volar (Vue Language Features)
  - ESLint
  - Tailwind CSS IntelliSense
  - Prettier

Check versions:
```bash
node --version  # Should be >= v18.0.0
npm --version   # Should be >= 9.0.0
git --version
```

## Step 1: Project Initialization

Create a new Vue 3 + Vite project:

```bash
npm create vite@latest lundao-lite-frontend -- --template vue
cd lundao-lite-frontend
```

**What this does**:
- Creates project with Vue 3 Single File Components
- Configures Vite for fast HMR and optimized builds
- Sets up basic ESLint configuration

## Step 2: Install Core Dependencies

Install required packages:

```bash
# Core dependencies
npm install vue@^3.4.0 pinia@^2.1.0 axios@^1.6.0

# UI & Styling
npm install -D tailwindcss@^3.4.0 postcss@^8.4.0 autoprefixer@^10.4.0
npm install @headlessui/vue@^1.7.0

# Development tools
npm install -D @vitejs/plugin-vue@^5.0.0
npm install -D eslint@^8.56.0 eslint-plugin-vue@^9.20.0

# Optional: Testing
npm install -D vitest@^1.2.0 @vue/test-utils@^2.4.0
```

## Step 3: Configure Tailwind CSS

Initialize Tailwind configuration:

```bash
npx tailwindcss init -p
```

Update `tailwind.config.js` with design system tokens:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-bg': '#FFFFFF',
        'secondary-bg': '#F8F9FA',
        'border-color': '#E9ECEF',
        'text-primary': '#212529',
        'text-secondary': '#6C757D',
        'accent': '#3A57E8',
        'success': '#198754',
        'error': '#DC3545',
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'h1': '28px',
        'h2': '22px',
        'h3': '18px',
        'body': '16px',
        'secondary': '14px',
      },
      spacing: {
        // 8px grid system
        '1': '8px',
        '2': '16px',
        '3': '24px',
        '4': '32px',
        '5': '40px',
        '6': '48px',
      },
      borderRadius: {
        'button': '6px',
        'card': '1px',
        'modal': '12px',
      },
    },
  },
  plugins: [],
}
```

Create `src/assets/styles/main.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom base styles */
@layer base {
  body {
    @apply text-text-primary bg-primary-bg;
    font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
  }
}
```

Import in `src/main.js`:

```javascript
import './assets/styles/main.css'
```

## Step 4: Add Chinese Fonts

Update `index.html` to load fonts from Google Fonts CDN:

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>论导Lite - AI助你三分钟搞定组会PPT</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

## Step 5: Set Up Project Structure

Create the directory structure:

```bash
mkdir -p src/api
mkdir -p src/assets/fonts
mkdir -p src/assets/images
mkdir -p src/assets/styles
mkdir -p src/components/common
mkdir -p src/components/core
mkdir -p src/composables
mkdir -p src/stores
mkdir -p src/views
```

## Step 6: Configure Axios API Client

Create `src/api/index.js`:

```javascript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  timeout: 60000, // 60 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add request logging or loading state here
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Global error handling
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default apiClient
```

Create service modules:

```bash
touch src/api/paperService.js
touch src/api/uploadService.js
touch src/api/taskService.js
```

## Step 7: Initialize Pinia Stores

Update `src/main.js`:

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')
```

Create store files:

```bash
touch src/stores/papers.js
touch src/stores/tasks.js
touch src/stores/ui.js
```

## Step 8: Environment Configuration

Create `.env.development`:

```env
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_TITLE=论导Lite - AI助你三分钟搞定组会PPT
```

Create `.env.production`:

```env
VITE_API_BASE_URL=https://api.lundao.com/api
VITE_APP_TITLE=论导Lite - AI助你三分钟搞定组会PPT
```

**Note**: Add `.env.local` to `.gitignore` for local overrides.

## Step 9: Update Vite Configuration

Modify `vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
})
```

## Step 10: ESLint Configuration

Create `.eslintrc.cjs`:

```javascript
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
  ],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module',
  },
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/require-default-prop': 'off',
  },
}
```

Add lint scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs --fix --ignore-path .gitignore"
  }
}
```

## Step 11: Create Initial Components

Create basic component templates:

**src/App.vue**:
```vue
<script setup>
import HomeView from './views/HomeView.vue'
</script>

<template>
  <div id="app" class="min-h-screen bg-primary-bg">
    <HomeView />
  </div>
</template>
```

**src/views/HomeView.vue**:
```vue
<script setup>
// Import components as they're created
</script>

<template>
  <div class="home-view">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 bg-white border-b border-border-color z-50">
      <div class="container mx-auto px-4 py-3">
        <h1 class="text-h2 font-semibold text-text-primary">
          论导Lite - AI助你三分钟搞定组会PPT
        </h1>
      </div>
    </header>

    <!-- Main content (padding-top for fixed header) -->
    <main class="pt-20 pb-8">
      <div class="container mx-auto px-4">
        <p class="text-center text-text-secondary">
          Development environment ready! Start building components.
        </p>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-secondary-bg border-t border-border-color py-6">
      <div class="container mx-auto px-4 text-center text-secondary">
        <p>&copy; 2025 论导Lite. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>
```

## Step 12: Run Development Server

Start the development server:

```bash
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Open `http://localhost:5173/` in your browser. You should see the basic layout with header and footer.

## Step 13: Verify Setup

### Check Tailwind CSS
Tailwind should be working if you see the correct colors and spacing in the browser.

### Check Fonts
Open browser DevTools → Network tab → Filter by "font". You should see Inter and Noto Sans SC loading from Google Fonts.

### Check Hot Module Replacement
Edit `src/views/HomeView.vue`, save, and verify the browser updates instantly without full reload.

### Check API Client
In browser console:
```javascript
import apiClient from './src/api/index.js'
// Should not throw errors
```

## Step 14: Backend Mock (Optional)

If backend is not ready, create a simple mock server:

Create `mock-server.js` in project root:

```javascript
import express from 'express'
import cors from 'cors'

const app = express()
app.use(cors())
app.use(express.json())

// Mock endpoints
app.get('/api/arxiv_papers', (req, res) => {
  res.json({
    papers: [
      {
        id: 'arxiv-2301.00000',
        title: 'Mock Paper Title',
        authors: ['Author 1', 'Author 2'],
        abstract: 'This is a mock abstract...',
        arxivId: '2301.00000',
        field: 'Machine Learning',
        keywords: ['AI', 'ML'],
        publicationDate: '2023-01-01',
        pdfUrl: 'https://arxiv.org/pdf/2301.00000.pdf',
        arxivUrl: 'https://arxiv.org/abs/2301.00000'
      }
    ],
    pagination: {
      currentPage: 1,
      totalPages: 1,
      totalItems: 1,
      itemsPerPage: 20
    }
  })
})

app.listen(3000, () => {
  console.log('Mock API server running on http://localhost:3000')
})
```

Install dependencies and run:
```bash
npm install express cors
node mock-server.js
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Tailwind Not Working
- Ensure `main.css` is imported in `main.js`
- Check `tailwind.config.js` content paths include `./src/**/*.vue`
- Restart dev server

### Fonts Not Loading
- Check Network tab for CORS errors
- Verify `preconnect` links in `index.html`
- Try self-hosting fonts if CDN blocked

### ESLint Errors
```bash
npm run lint
```

Fix auto-fixable issues, manually resolve others.

## Next Steps

1. ✅ Development environment ready
2. ⏭️  Implement Pinia stores (papers, tasks, ui)
3. ⏭️  Create common UI components (Button, Modal, Toast, Badge, Tabs, Pagination)
4. ⏭️  Create core business components (PaperCard, UploadDropzone, TaskItem, etc.)
5. ⏭️  Integrate API services with components
6. ⏭️  Add animations and transitions
7. ⏭️  Manual testing and polish

## Useful Commands

```bash
# Development
npm run dev              # Start dev server
npm run build            # Production build
npm run preview          # Preview production build
npm run lint             # Lint and fix code

# Testing (if configured)
npm run test             # Run unit tests
npm run test:coverage    # Generate coverage report
```

## Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Headless UI Vue Documentation](https://headlessui.com/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Axios Documentation](https://axios-http.com/)

## Development Tips

1. **Use Vue DevTools**: Install browser extension for debugging stores and components
2. **Hot reload**: Save files to see instant updates
3. **Component isolation**: Build components in isolation before integrating
4. **Mock data**: Use static mock data during development
5. **Git commits**: Commit after completing each major component
6. **Code reviews**: Review against constitution principles before merging

---

**Setup Complete!** 🎉

You're now ready to start implementing the 论导Lite MVP frontend. Proceed to task implementation following the sequence in `tasks.md` (to be generated by `/speckit.tasks`).
