# Mock API Contract: Create PPT Task

**Function**: `mockCreatePPTTask`
**File**: `src/mocks/taskService.js`
**Purpose**: Simulate PPT task creation for mock mode

## Signature

```javascript
export const mockCreatePPTTask = async (paperId, isArxiv = true)
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `paperId` | string | Yes | - | Paper identifier (arX ivId or fileId) |
| `isArxiv` | boolean | No | `true` | Whether paper is from arXiv (true) or uploaded PDF (false) |

## Output

**Type**: `Promise<Object>`

**Success Response**:
```javascript
{
  taskId: string  // Format: "mock-task-{timestamp}-{random}"
}
```

**Example**:
```javascript
{
  taskId: "mock-task-1705300123456-a3f8e9"
}
```

## Behavior

1. **Generate Unique Task ID**:
   - Format: `mock-task-{Date.now()}-{random6chars}`
   - Random component: 6 alphanumeric lowercase characters
   - Example: `mock-task-1705300123456-a3f8e9`

2. **Record Creation Timestamp**:
   - Store in `taskCreationTimes` Map: `{ taskId → { createdAt, paperId, isArxiv } }`
   - `createdAt`: Unix timestamp in milliseconds (`Date.now()`)

3. **Simulate Network Delay**:
   - Add 500ms delay via `await new Promise(resolve => setTimeout(resolve, 500))`
   - Mimics real API latency for realistic testing

4. **Return Task ID**:
   - Return object with `taskId` field
   - Store uses this ID to create task object with `status: 'queued'`

## Error Handling

**No errors thrown** - Mock always succeeds to enable uninterrupted frontend testing.

*Optional future enhancement*: Random 10% failure rate for error state testing.

## Usage Example

```javascript
// src/stores/tasks.js
const response = await createPPTTask(paperId, paperTitle, isArxiv)
// response = { taskId: "mock-task-1705300123456-a3f8e9" }

const newTask = {
  id: response.taskId,
  paperId,
  paperTitle,
  status: 'queued',
  createdAt: new Date().toISOString(),
  // ... other fields
}
```

## Implementation

```javascript
// src/mocks/taskService.js
import { generateMockTaskId, delay } from './utils'

const taskCreationTimes = new Map()

export const mockCreatePPTTask = async (paperId, isArxiv = true) => {
  // Simulate network delay
  await delay(500)

  const taskId = generateMockTaskId()

  // Record creation timestamp
  taskCreationTimes.set(taskId, {
    createdAt: Date.now(),
    paperId,
    isArxiv
  })

  console.log(`[Mock] PPT task created: ${taskId}`)

  return { taskId }
}
```

## Testing

```javascript
// Manual test in browser console
const result = await mockCreatePPTTask('daily-0001', true)
console.log(result)  // { taskId: "mock-task-..." }

// Verify Map entry
console.log(taskCreationTimes.get(result.taskId))
// { createdAt: 1705300123456, paperId: 'daily-0001', isArxiv: true }
```

## Notes

- Task ID format (`mock-task-*`) distinguishes from real UUIDs
- Map is module-scoped, persists across function calls but not page refreshes
- 500ms delay matches typical backend response time for task creation
