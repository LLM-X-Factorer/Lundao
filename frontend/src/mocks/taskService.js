/**
 * Mock Task Service
 *
 * Simulates PPT task creation and status polling for mock mode
 * Uses in-memory Map to track task creation times for status progression
 */

import { generateMockTaskId, delay } from './utils'

/**
 * Mock task timing configuration (in seconds)
 * Defines status transition thresholds for realistic progression
 */
export const MOCK_TASK_TIMING = {
  QUEUE_DURATION: 5,      // 0-5s: queued status
  GENERATE_DURATION: 10,  // 5-15s: generating status (10s duration)
  TOTAL_DURATION: 15      // 15s+: completed status
}

/**
 * In-memory Map to track task creation timestamps
 * Key: taskId (string)
 * Value: { createdAt: number, paperId: string, isArxiv: boolean }
 *
 * Note: Cleared on page refresh - orphaned tasks will fail on next poll
 */
const taskCreationTimes = new Map()

/**
 * Mock PPT task creation
 *
 * @param {string} paperId - Paper identifier (arXivId or fileId)
 * @param {boolean} isArxiv - Whether paper is from arXiv (default: true)
 * @returns {Promise<{taskId: string}>} Task creation response
 */
export const mockCreatePPTTask = async (paperId, isArxiv = true) => {
  // Simulate network delay (500ms)
  await delay(500)

  const taskId = generateMockTaskId()

  // Record creation timestamp for status progression
  taskCreationTimes.set(taskId, {
    createdAt: Date.now(),
    paperId,
    isArxiv
  })

  console.log(`[Mock] PPT task created: ${taskId} for paper ${paperId}`)

  return { taskId }
}

/**
 * Mock task status polling
 * Returns status based on elapsed time since creation
 *
 * @param {string} taskId - Task identifier
 * @returns {Promise<{status: string, progress: number|null, downloadUrl: string|null, errorMessage: string|null}>}
 */
export const mockPollTaskStatus = async (taskId) => {
  // Simulate network delay (300ms - faster than creation)
  await delay(300)

  const task = taskCreationTimes.get(taskId)

  // Task not found (page refresh scenario)
  if (!task) {
    return {
      status: 'failed',
      progress: 0,
      downloadUrl: null,
      errorMessage: '任务不存在或已过期'
    }
  }

  // Calculate elapsed time in seconds
  const elapsedSeconds = (Date.now() - task.createdAt) / 1000

  // Phase 1: Queued (0-5s)
  if (elapsedSeconds < MOCK_TASK_TIMING.QUEUE_DURATION) {
    return {
      status: 'queued',
      progress: null,
      downloadUrl: null,
      errorMessage: null
    }
  }

  // Phase 2: Generating (5-15s)
  if (elapsedSeconds < MOCK_TASK_TIMING.TOTAL_DURATION) {
    // Linear progress: 0-90% over 10 seconds
    const progress = Math.min(90, Math.floor((elapsedSeconds - MOCK_TASK_TIMING.QUEUE_DURATION) * 9))
    return {
      status: 'generating',
      progress,
      downloadUrl: null,
      errorMessage: null
    }
  }

  // Phase 3: Completed (15s+)
  // Download URL points to public/ppt-files/{paperId}.pptx
  // Use paperId instead of taskId for actual file mapping
  return {
    status: 'completed',
    progress: 100,
    downloadUrl: `/ppt-files/${task.paperId}.pptx`,
    errorMessage: null
  }
}

/**
 * Optional cleanup utility to remove expired task records
 * Can be called manually or on unmount to free memory
 */
export const cleanupExpiredTasks = () => {
  const now = Date.now()
  const EXPIRY_TIME = 24 * 60 * 60 * 1000 // 24 hours

  for (const [taskId, taskInfo] of taskCreationTimes.entries()) {
    if (now - taskInfo.createdAt > EXPIRY_TIME) {
      taskCreationTimes.delete(taskId)
      console.log(`[Mock] Cleaned up expired task: ${taskId}`)
    }
  }
}
