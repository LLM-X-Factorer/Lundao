# Lundao-Lite-FrontEnd
论导Lite前端项目

## Project Overview

论导Lite is an AI-powered SaaS tool designed for Chinese academic researchers (master's
and PhD students) to streamline the paper discovery, understanding, and presentation
workflow. The MVP frontend enables users to discover trending papers, upload PDFs, get
AI analysis, and generate presentation slides—all within 3 minutes, without registration.

## Core Principles

This project strictly follows five non-negotiable design principles:

1. **Tool-First Philosophy** (工具化，非平台化): No user management, no engagement
   mechanics—pure workflow efficiency
2. **Single-Page Minimalism** (单页极简): All core features on one page, zero navigation
   friction
3. **Zero Friction** (零摩擦体验): No authentication required, localStorage-based state
4. **Value-First Design** (价值前置): AI insights displayed prominently before metadata
5. **Aesthetics as Trust** (美学优先): Modern, minimalist design with strict Design
   System adherence

See `.specify/memory/constitution.md` for complete governance and technical standards.

## Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **CSS**: Tailwind CSS
- **Components**: Headless UI
- **State**: Pinia
- **HTTP**: Axios
- **Markdown**: marked + KaTeX + highlight.js
- **Security**: DOMPurify

## Features

### ✅ Paper Discovery (Feature #001)
- Trending papers from arXiv (daily, weekly, monthly)
- AI-powered Chinese analysis with innovation points
- PDF upload support (up to 20MB)

### ✅ PPT Generation (Feature #003)
- One-click PPT generation from papers
- Task history with real-time status tracking
- Mock system for offline development

### ✅ PPT Preview (Feature #004) 🎉 NEW
- Full Markdown rendering with academic formatting
- **LaTeX formula support** (inline `$...$` and block `$$...$$`)
- **Code syntax highlighting** (7 languages: Python, JavaScript, Java, C++, SQL, Bash, JSON)
- Slide-by-slide navigation with keyboard shortcuts
- Watermark protection (9-grid layout)
- XSS protection via DOMPurify
- Bundle: 197 KB gzipped (including KaTeX fonts)

**See**: `specs/004-ppt-preview-feature/README.md` for complete documentation

## Documentation

- **PRD**: `Docs/PRD.md` - Product requirements and feature specifications
- **BluePrint**: `Docs/BluePrint.md` - Design system and development roadmap
- **Constitution**: `.specify/memory/constitution.md` - Project governance and principles

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Project Structure

```
src/
├── api/           # Backend API integration
├── components/
│   ├── common/    # Reusable UI primitives
│   └── core/      # Business logic components
├── composables/   # Composition API logic
├── stores/        # Pinia state management
└── views/         # Page-level components
```

For detailed architecture and development workflow, see the constitution and blueprint
documents.
