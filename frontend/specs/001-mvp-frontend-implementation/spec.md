# Feature Specification: 论导Lite MVP Frontend

**Feature Branch**: `001-mvp-frontend-implementation`
**Created**: 2025-10-14
**Status**: Draft
**Input**: User description: "based on @Docs/ files"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Discover and Analyze Trending Papers (Priority: P1)

A Chinese graduate student preparing for their weekly group meeting needs to find recent papers in their research field. They visit the application, browse trending papers from arXiv organized by timeframe (today, this week, this month), select a paper that interests them, and immediately see an AI-generated Chinese summary with key innovation points—all without creating an account.

**Why this priority**: This is the core value proposition—enabling users to quickly understand papers. It demonstrates the AI analysis capability and provides immediate value on first visit without any friction.

**Independent Test**: Can be fully tested by accessing the application, browsing the paper list, clicking a paper card, and verifying that the AI analysis (Chinese summary + innovation points) displays correctly. Delivers standalone value even without the upload or PPT generation features.

**Acceptance Scenarios**:

1. **Given** the user visits the application for the first time, **When** they view the homepage, **Then** they see trending papers organized in tabs (Daily, Weekly, Monthly) without any login prompt
2. **Given** the user is viewing the paper discovery section, **When** they switch between time period tabs, **Then** the paper list updates to show papers for that period with loading feedback
3. **Given** the user sees the paper list, **When** they hover over a paper card, **Then** the card shows visual feedback (subtle shadow or scale)
4. **Given** the user clicks on a paper card, **When** the modal opens, **Then** they see the paper title, authors, and a loading state for AI analysis
5. **Given** AI analysis is loading, **When** analysis completes, **Then** the Chinese summary and innovation points display prominently in the modal
6. **Given** the paper modal is open, **When** the user clicks outside the modal or a close button, **Then** the modal closes smoothly

---

### User Story 2 - Upload and Analyze Custom Papers (Priority: P2)

A researcher has a PDF paper from their institution's repository (not on arXiv) that they need to present. They drag-and-drop the PDF file into the upload zone, see upload progress, and once complete, immediately view the AI-generated Chinese analysis of their paper—again, without any account creation.

**Why this priority**: Extends the value proposition beyond arXiv papers, making the tool useful for any academic PDF. Critical for users whose research areas aren't well-represented on arXiv or who need to analyze papers from other sources.

**Independent Test**: Can be tested by uploading a PDF file and verifying the upload progress, success feedback, and AI analysis modal display. Works independently of the discovery feature.

**Acceptance Scenarios**:

1. **Given** the user is on the homepage, **When** they see the upload zone, **Then** it displays clear instructions ("Drag PDF here or click to select")
2. **Given** the user drags a PDF file over the upload zone, **When** the file enters the zone, **Then** the border highlights and shows a visual indicator
3. **Given** the user drops a PDF file, **When** upload begins, **Then** a progress bar shows upload percentage and the zone is disabled
4. **Given** upload completes successfully, **When** the file is processed, **Then** a brief success animation plays and the paper analysis modal opens automatically
5. **Given** upload fails, **When** an error occurs, **Then** the user sees a clear error message with the reason
6. **Given** the user uploads a non-PDF file, **When** validation runs, **Then** the system rejects it with a friendly error message

---

### User Story 3 - Generate and Track Presentation Slides (Priority: P1)

After reviewing the AI analysis of a paper (either from discovery or upload), the user clicks "Generate Presentation PPT" button. The system creates a generation task, shows it in the history section with "Queued" status, and automatically updates the status to "Generating" then "Complete

d" through background polling. When complete, the user downloads their PPT with a single click.

**Why this priority**: This is the ultimate deliverable—the "3 minutes to presentation" promise. While analysis is valuable, generating the actual PPT is what completes the workflow and provides the full tool value.

**Independent Test**: Can be tested by initiating PPT generation from any analyzed paper, verifying task creation, status polling updates, and final download. The complete user journey from discovery/upload → analysis → PPT.

**Acceptance Scenarios**:

1. **Given** the user has viewed a paper's AI analysis, **When** they click "Generate Presentation PPT", **Then** the button shows loading state and a request is sent
2. **Given** the PPT generation request succeeds, **When** the modal closes, **Then** a toast notification appears saying "PPT generation task created, check history below"
3. **Given** a task is created, **When** the user views the task history section, **Then** they see a new task row with paper title, "Queued" status badge, creation time, and pending action
4. **Given** tasks exist in history, **When** the system polls for updates (every 5 seconds), **Then** task statuses update automatically without user action
5. **Given** a task status changes to "Completed", **When** the UI updates, **Then** the "Download PPT" button becomes clickable with appropriate styling
6. **Given** a task status is "Failed", **When** displayed, **Then** the user sees the failure reason and a "Retry" button
7. **Given** the user clicks "Download PPT" on a completed task, **When** the download starts, **Then** the PPT file downloads to their device
8. **Given** the user clicks the delete button on a task, **When** confirmed, **Then** the task is removed from the list and localStorage
9. **Given** the user closes and reopens the browser, **When** they return to the application, **Then** all previous tasks persist from localStorage

---

### User Story 4 - Navigate Paginated Paper Lists (Priority: P3)

When viewing trending papers, the user can navigate through multiple pages of results to explore more papers beyond the initial set. The pagination component allows moving between pages smoothly without full page reloads.

**Why this priority**: Improves discovery by allowing users to explore more papers, but not critical for MVP functionality. Users can still get value from the first page of results.

**Independent Test**: Can be tested by loading the paper discovery section and using pagination controls to navigate between pages.

**Acceptance Scenarios**:

1. **Given** the user views a paper list with more results than fit on one page, **When** they scroll to the bottom, **Then** they see pagination controls showing current page and total pages
2. **Given** the user is on page 1, **When** they click "Next" or page 2, **Then** the list updates to show page 2 papers with loading feedback
3. **Given** the user is on a middle page, **When** they use pagination, **Then** both "Previous" and "Next" buttons are enabled
4. **Given** the user is on the last page, **When** they view pagination, **Then** the "Next" button is disabled

---

### Edge Cases

- What happens when the arXiv API is unavailable or times out? (Show friendly error state with retry option)
- What happens when AI analysis takes longer than 30 seconds? (Continue showing loading state; implement timeout at 60 seconds with error message)
- What happens when a user uploads a corrupted or encrypted PDF? (Show clear error: "Unable to process this PDF file")
- What happens when localStorage is full? (Clear oldest completed tasks automatically, notify user)
- What happens when the backend polling endpoint returns an error? (Stop polling, show error badge on affected task)
- What happens when a user has 50+ tasks in history? (Implement "Clear completed tasks" bulk action)
- What happens when the user is on a slow 3G connection? (Show loading states earlier, optimize asset sizes)
- What happens when JavaScript is disabled? (Show message: "This application requires JavaScript")

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display trending arXiv papers organized by time period (Daily, Weekly, Monthly) in a tabbed interface
- **FR-002**: System MUST display each paper as a card showing title, authors, and research field/keywords
- **FR-003**: System MUST provide visual feedback (shadow/scale effect) when user hovers over paper cards
- **FR-004**: System MUST open a modal dialog when user clicks on any paper card
- **FR-005**: System MUST display an elegant loading state (skeleton screen or animation) while fetching AI analysis
- **FR-006**: System MUST display AI-generated Chinese summary and innovation points prominently in the paper modal
- **FR-007**: System MUST provide a file upload zone that accepts PDF files via drag-and-drop or click-to-browse
- **FR-008**: System MUST show upload progress with percentage during file upload
- **FR-009**: System MUST validate uploaded files are PDF format and show error for non-PDF files
- **FR-010**: System MUST automatically open the paper analysis modal after successful PDF upload
- **FR-011**: System MUST provide a prominent "Generate Presentation PPT" button in the paper modal
- **FR-012**: System MUST create a task record when user initiates PPT generation
- **FR-013**: System MUST display task generation history with columns: paper title, status, creation time, actions
- **FR-014**: System MUST persist all task records in browser localStorage for persistence across sessions
- **FR-015**: System MUST poll backend every 5 seconds to update task statuses automatically
- **FR-016**: System MUST display task status using visually distinct badges (Queued, Generating, Completed, Failed)
- **FR-017**: System MUST enable "Download PPT" button only when task status is "Completed"
- **FR-018**: System MUST provide a "Retry" button for failed tasks
- **FR-019**: System MUST provide a "Delete" button for each task to remove it from history
- **FR-020**: System MUST display toast notifications for important actions (task created, errors)
- **FR-021**: System MUST implement smooth transitions and animations for all state changes (modal open/close, button states, list updates)
- **FR-022**: System MUST provide pagination for paper lists when results exceed one page
- **FR-023**: System MUST display friendly empty states when no papers are available or history is empty
- **FR-024**: System MUST complete all interactions within 100ms visual feedback requirement
- **FR-025**: System MUST work without any user registration or authentication
- **FR-026**: System MUST provide secondary actions in paper modal (Download PDF, Visit arXiv page) as links
- **FR-027**: System MUST display a fixed header with logo and slogan at top of page
- **FR-028**: System MUST display a footer with product info, feedback channels, and terms links
- **FR-029**: System MUST handle API failures gracefully with user-friendly error messages
- **FR-030**: System MUST maintain responsive layout for desktop screens from 13-inch to large displays

### Key Entities

- **Paper**: Represents an academic paper with attributes: title, authors, abstract, arXiv ID (if applicable), uploaded file ID (if uploaded), research field/keywords, publication date
- **AI Analysis**: Represents the AI-generated insights for a paper with attributes: Chinese summary text, list of innovation points, analysis timestamp
- **PPT Generation Task**: Represents a presentation generation request with attributes: task ID, associated paper reference, status (queued/generating/completed/failed), creation timestamp, download URL (when completed), error message (if failed)
- **Task History**: Collection of PPT generation tasks persisted in browser localStorage, maintaining order by creation time

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can discover, analyze, and initiate PPT generation for a paper within 3 minutes of first visiting the application
- **SC-002**: All user interactions (clicks, hovers, form submissions) provide visual feedback within 100 milliseconds
- **SC-003**: Application loads and displays initial trending papers within 1.5 seconds on standard 3G connection
- **SC-004**: Users can successfully complete the full workflow (discover/upload → analyze → generate → download) without encountering any registration or login prompts
- **SC-005**: Task status updates appear in the UI within 5-10 seconds of backend status changes (polling interval tolerance)
- **SC-006**: Paper discovery section displays 10-20 papers per page with smooth pagination
- **SC-007**: All task history persists across browser sessions through localStorage
- **SC-008**: Users can upload PDF files up to 20MB size without timeout errors
- **SC-009**: Modal animations and transitions complete smoothly at 60fps on modern browsers
- **SC-010**: Empty states and error states provide clear next actions without technical jargon
- **SC-011**: Application maintains visual consistency with design system (colors, typography, spacing) across all components
- **SC-012**: Users can manage (view, download, retry, delete) unlimited tasks in their history section

### Assumptions

- Backend APIs are available and return data in expected formats as documented in PRD section 4
- ArXiv API provides reliable trending paper data with reasonable response times (<2 seconds)
- Backend AI analysis completes within 60 seconds for 90% of papers
- Backend PPT generation completes within 5 minutes for 90% of papers
- Users have JavaScript enabled in modern browsers (Chrome, Firefox, Safari, Edge from last 2 years)
- Users primarily access the application from desktop or laptop computers (13-inch or larger screens)
- Average paper PDFs are 2-10MB in size
- Chinese text rendering is supported by user's operating system
- Network bandwidth is sufficient for uploading multi-megabyte PDF files
- User's localStorage has at least 5MB available space for task history

### Dependencies

- Backend API endpoints must be implemented as specified in PRD section 4
- Design assets (logo, icons) must be provided in web-compatible formats
- Inter and Noto Sans SC fonts must be loaded from web font service or bundled
- Backend must support CORS for frontend API requests during development

## Technical Constraints

### Performance Targets

- First Contentful Paint (FCP): <1.5 seconds on 3G connection
- Time to Interactive (TTI): <3 seconds on 3G connection
- Largest Contentful Paint (LCP): <2.5 seconds
- Cumulative Layout Shift (CLS): <0.1
- First Input Delay (FID): <100 milliseconds

### Browser Support

- Chrome/Edge: Last 2 major versions
- Firefox: Last 2 major versions
- Safari: Last 2 major versions
- No Internet Explorer support required

### Accessibility

- Keyboard navigation support for all interactive elements
- ARIA labels for screen reader compatibility (provided by Headless UI)
- Sufficient color contrast ratios (WCAG AA compliance)
- Focus indicators visible on all focusable elements

### Design System Compliance

All visual implementations must adhere to the design system defined in the BluePrint:

**Colors**:
- Primary Background: #FFFFFF or #FDFDFD
- Secondary Background: #F8F9FA
- Borders: #E9ECEF
- Primary Text: #212529
- Secondary Text: #6C757D
- Brand/Accent: #3A57E8
- Success: #198754
- Error: #DC3545

**Typography**:
- Font Family: Inter (English/numbers), Noto Sans SC (Chinese)
- H1: 28px, H2: 22px, H3/Card: 18px, Body: 16px, Secondary: 14px

**Spacing**:
- All spacing must use 8px grid system (8px, 16px, 24px, 32px multiples)

**Components**:
- Button border-radius: 6px
- Card border: 1px solid #E9ECEF, hover shadow permitted
- Modal border-radius: 12px

## Out of Scope

The following are explicitly excluded from this MVP:

- User authentication and account management
- User profiles or personalization features
- Bookmarking or saving favorite papers
- Sharing or collaboration features
- Email notifications for task completion
- Mobile responsive design (desktop-first only for MVP)
- Dark mode toggle
- Internationalization beyond Chinese (no English localization yet)
- Advanced search or filtering of papers
- Editing or customization of generated PPTs
- Analytics or usage tracking
- Admin dashboard or content management
- Payment or subscription features
- Multi-file batch upload
- Real-time WebSocket updates (using polling instead)
- Browser extension or mobile app
- Offline functionality or service worker caching
- PDF preview or embedded viewer
- Citation export or bibliography generation
