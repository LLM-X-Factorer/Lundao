# 📚 Reference Documentation

This directory contains comprehensive reference documentation for the Lundao-Lite frontend project.

## Quick Navigation

### Core Documentation
- **[Architecture](./architecture.md)** - System architecture, tech stack, and design patterns
- **[Components](./components.md)** - All Vue components with props, emits, and usage
- **[State Management](./state-management.md)** - Pinia stores and composables
- **[API Services](./api-services.md)** - API client, service modules, and mock system
- **[Design System](./design-system.md)** - Colors, typography, spacing, and UI patterns
- **[Utilities](./utilities.md)** - Helper functions and configuration
- **[Deployment](./deployment.md)** - Docker, Aliyun ECS, and static hosting deployment guides

### Specialized Topics
- **[PPT Preview System](./ppt-preview.md)** - Image-based PPT preview implementation
- **[Mock Data System](./mock-system.md)** - Complete mock data architecture
- **[Task Lifecycle](./task-lifecycle.md)** - PPT generation task state machine
- **[Upload Flow](./upload-flow.md)** - File upload and validation workflow

## Documentation Structure

```
ref/
├── README.md                 # This file - navigation guide
├── architecture.md           # High-level system architecture
├── components.md             # Component API reference
├── state-management.md       # Stores and composables
├── api-services.md           # API client and services
├── design-system.md          # UI/UX design system
├── utilities.md              # Helper functions
├── deployment.md             # Deployment guides (Docker, Aliyun, etc.)
├── ppt-preview.md            # PPT preview feature
├── mock-system.md            # Mock data system
├── task-lifecycle.md         # Task state management
└── upload-flow.md            # Upload workflow
```

## How to Use This Documentation

### For New Developers
1. Start with [Architecture](./architecture.md) to understand the big picture
2. Read [Design System](./design-system.md) to learn UI patterns
3. Review [Components](./components.md) for available building blocks
4. Check [State Management](./state-management.md) for data flow

### For Feature Development
1. Check [Components](./components.md) for existing components
2. Review [API Services](./api-services.md) for backend integration
3. Consult [Design System](./design-system.md) for styling guidelines
4. See [Mock System](./mock-system.md) for testing without backend

### For Debugging
1. Check [Task Lifecycle](./task-lifecycle.md) for task status issues
2. Review [Upload Flow](./upload-flow.md) for upload problems
3. See [State Management](./state-management.md) for data sync issues
4. Consult [PPT Preview](./ppt-preview.md) for preview errors

### For Deployment
1. Start with [Deployment](./deployment.md) for deployment options overview
2. Use Docker for local development and testing
3. Follow Aliyun ECS guide for production deployment
4. Configure Nginx for reverse proxy and HTTPS

## Key Concepts

### Component Architecture
- **Common Components**: Reusable UI primitives (Button, Modal, Toast)
- **Core Components**: Business logic components (PaperCard, TaskItem, UploadDropzone)
- **Single-Page App**: All features on root route `/` (no router)

### State Management
- **papers.js**: Paper discovery and pagination
- **tasks.js**: PPT task lifecycle and polling
- **ui.js**: Global UI state (modals, toasts)

### Mock vs Real Mode
- Environment variable: `VITE_USE_MOCK_DATA`
- Mock mode: Complete frontend development without backend
- Real mode: Production integration with backend APIs

### Design Principles
1. **Tool-First Philosophy**: No accounts, no friction
2. **Single-Page Minimalism**: Everything on `/`
3. **Value-First**: AI insights before metadata
4. **Aesthetic Trust**: Strict design system adherence

## External References

### Project Documentation
- **Project Instructions**: `/CLAUDE.md` - Main project guide
- **Quick Start Guide**: `/QUICKSTART.md` - Development quickstart
- **Test Report**: `/TEST-SUMMARY.md` - Testing summary

### Deployment Documentation
- **Docker Deployment**: `/DOCKER-DEPLOYMENT.md` - Complete Docker guide (370+ lines)
- **Aliyun Deployment**: `/ALIYUN-DEPLOYMENT.md` - Aliyun ECS deployment (520+ lines)
- **Deployment Summary**: `/ALIYUN-DEPLOYMENT-SUMMARY.md` - Deployment overview
- **Static Hosting**: `/DEPLOYMENT.md` - Netlify and GitHub Pages

### Deployment Scripts
- **One-Click Deploy**: `/deploy/deploy.sh` - Automated deployment script
- **Update Script**: `/deploy/update.sh` - Smart update with rollback
- **Nginx Config**: `/deploy/nginx.conf` - Reverse proxy configuration
- **Quick Start**: `/deploy/QUICKSTART.md` - 5-minute deployment guide

### Specifications
- **MVP Spec**: `/specs/001-mvp-frontend-implementation/` - Core implementation
- **Feature Specs**: `/specs/002-*/` through `/specs/006-*/` - Enhancement features

---

**Last Updated**: 2025-11-18
**Documentation Version**: 1.1 - Added deployment documentation
