# Quickstart Guide: PPT Task Mock System

**Feature**: PPT Task Mock System
**Branch**: `003-ppt-task-mock`
**Date**: 2025-01-15
**Audience**: Frontend developers

---

## Prerequisites

- Node.js 18+ installed
- Project dependencies installed (`npm install`)
- Familiarity with Vue 3 and Vite development workflow

---

## Setup Instructions

### 1. Enable Mock Mode

Edit `.env.development` file in project root:

```bash
# .env.development
VITE_USE_MOCK_DATA=true
```

**Verify**: `.env.production` should have:
```bash
# .env.production
VITE_USE_MOCK_DATA=false
```

### 2. Start Development Server

```bash
npm run dev
```

### 3. Verify Mock Mode is Active

Check browser console for warning:
```
🚧 Mock Mode Enabled 🚧
PPT任务和分析数据使用mock,非真实后端数据
```

---

## Testing the Mock System

### Test 1: View Historical Tasks

**Steps**:
1. Open application (default: http://localhost:5173)
2. Scroll to "任务历史" section at bottom of page
3. Observe 3 pre-populated tasks:
   - 2 completed tasks with "Download PPT" buttons
   - 1 failed task with error message

**Expected Result**:
- Tasks display paper titles, timestamps, status indicators
- Completed tasks show green checkmark, 100% progress
- Failed task shows red error icon, error message "PPT生成超时,请重试"

---

### Test 2: Create New Task

**Steps**:
1. Click any paper card in discovery section
2. Modal opens with AI analysis
3. Click "一键生成组会PPT" button

**Expected Result**:
- Toast message appears: "PPT生成任务已创建"
- Modal closes automatically
- New task appears at top of TaskHistory with "queued" status
- No console errors

---

### Test 3: Observe Status Progression

**Steps**:
1. Create new task (as in Test 2)
2. Watch TaskHistory for 15 seconds (don't refresh page)

**Expected Timeline**:
- **0-5s**: Task shows "queued" status, no progress bar
- **5-15s**: Status changes to "generating", progress bar appears and grows 0% → 90%
- **15s+**: Status changes to "completed", progress jumps to 100%, "Download PPT" button appears

**Expected Result**:
- Status transitions happen automatically (no manual refresh needed)
- Progress bar animates smoothly
- Final state shows download button

---

### Test 4: Test Download Button (Mock)

**Steps**:
1. Click "Download PPT" button on any completed task

**Expected Result**:
- Toast message appears: "Mock模式: 实际部署后可下载真实PPT文件"
- No file download occurs
- No console errors

---

### Test 5: Page Refresh Persistence

**Steps**:
1. Create 1-2 new tasks
2. Wait for tasks to reach "generating" or "completed" status
3. Refresh page (F5 or Ctrl+R)

**Expected Result**:
- Completed tasks persist and remain completed
- Historical tasks (3 pre-populated) still visible
- Tasks that were in "queued" or "generating" status change to "failed" with message "页面刷新导致任务中断 (Mock模式)"

**Rationale**: Mock system loses in-memory timestamps on refresh, so active tasks fail gracefully.

---

### Test 6: Switch to Real API Mode

**Steps**:
1. Stop dev server (Ctrl+C)
2. Edit `.env.development`:
   ```bash
   VITE_USE_MOCK_DATA=false
   ```
3. Restart dev server: `npm run dev`
4. Try to create new task

**Expected Result**:
- Console warning "🚧 Mock Mode Enabled 🚧" **disappears**
- Clicking "Generate PPT" triggers real API call
- **Expected error** (if backend not running): API 404 or network error
- This confirms mode switching works correctly

**Cleanup**: Set `VITE_USE_MOCK_DATA=true` in `.env.development` to resume mock testing

---

## Troubleshooting

### Issue: No historical tasks appear

**Symptoms**: TaskHistory shows "暂无任务历史" message

**Diagnosis**:
1. Check console for mock mode warning
2. Verify `VITE_USE_MOCK_DATA=true` in `.env.development`
3. Check localStorage: Open DevTools → Application → Local Storage → Check for `lundao-tasks` key

**Solution**:
```bash
# Clear localStorage
localStorage.clear()

# Refresh page - historical tasks should load
```

---

### Issue: Tasks stuck in "queued" status

**Symptoms**: Task never progresses to "generating" after 5+ seconds

**Diagnosis**:
1. Check browser console for errors
2. Verify polling is active: `tasksStore.pollingActive` should be `true`

**Solution**:
```javascript
// In browser console
const tasksStore = useTasksStore()
console.log('Polling active:', tasksStore.pollingActive)
console.log('Active tasks:', tasksStore.activeTasks)

// Manually start polling if stopped
tasksStore.startPolling()
```

---

### Issue: localStorage quota exceeded

**Symptoms**: Toast warning "LocalStorage容量不足，已清理最早的任务"

**Diagnosis**: Too many tasks in history (>50)

**Solution**:
```bash
# Clear old tasks manually
localStorage.removeItem('lundao-tasks')

# Or in browser console
const tasksStore = useTasksStore()
tasksStore.tasks.value = tasksStore.tasks.value.slice(0, 10)  # Keep only 10 most recent
tasksStore.saveTasksToLocalStorage()
```

---

### Issue: Download button does nothing

**Symptoms**: Clicking download on completed task shows no toast

**Diagnosis**: Check if download URL starts with `/mock/downloads/`

**Solution**: This is expected behavior in mock mode. Toast should appear. If not, check:
```javascript
// In browser console
const tasksStore = useTasksStore()
const task = tasksStore.tasks[0]  // First task
console.log('Download URL:', task.downloadUrl)
// Should be: "/mock/downloads/mock-task-XXX.pptx"
```

---

## Advanced Testing

### Test Multiple Tasks Simultaneously

```javascript
// In browser console
const uiStore = useUiStore()
const tasksStore = useTasksStore()

// Create 5 tasks rapidly
for (let i = 0; i < 5; i++) {
  uiStore.openModal(`daily-000${i + 1}`)
  setTimeout(() => {
    document.querySelector('[data-test-id="generate-ppt"]').click()
  }, 100)
}

// Observe: All tasks progress independently
```

### Test Edge Case: Create Task, Refresh Immediately

```javascript
// 1. Create task
// 2. Immediately refresh page (within 5s)
// 3. Observe: Task changes to "failed" status
```

---

## Key Files for Debugging

| File | Purpose | What to Check |
|------|---------|---------------|
| `src/mocks/taskData.js` | Historical task data | Verify 3 tasks exist |
| `src/mocks/taskService.js` | Mock API functions | Check `taskCreationTimes` Map |
| `src/api/taskService.js` | API routing logic | Verify `USE_MOCK_DATA` flag |
| `src/stores/tasks.js` | Task state management | Check `pollingActive`, `activeTasks` |
| `.env.development` | Environment config | Verify `VITE_USE_MOCK_DATA=true` |

---

## Performance Benchmarks

| Operation | Expected Duration | Notes |
|-----------|-------------------|-------|
| Task creation | <600ms | 500ms mock delay + UI update |
| Status poll | <400ms | 300ms mock delay + store update |
| Page load with 50 tasks | <200ms | LocalStorage read + render |
| Progress bar animation | 10s (5-15s elapsed) | Smooth 0-90% transition |

---

## Next Steps

After verifying mock system works:

1. **Implement Backend Integration**: Replace mock functions with real API calls when backend ready
2. **Test with Real API**: Set `VITE_USE_MOCK_DATA=false` and verify behavior matches mock
3. **Deploy**: Ensure `.env.production` has `VITE_USE_MOCK_DATA=false`

---

## Quick Reference

**Enable Mock**:
```bash
# .env.development
VITE_USE_MOCK_DATA=true
```

**Disable Mock**:
```bash
# .env.development
VITE_USE_MOCK_DATA=false
```

**Clear All Tasks**:
```javascript
localStorage.removeItem('lundao-tasks')
location.reload()
```

**Check Mock Status**:
```javascript
console.log('Mock mode:', import.meta.env.VITE_USE_MOCK_DATA)
```

---

## Support

If issues persist:
1. Check CLAUDE.md for mock system documentation
2. Review `specs/003-ppt-task-mock-system/research.md` for design decisions
3. Consult `specs/003-ppt-task-mock-system/data-model.md` for entity definitions
