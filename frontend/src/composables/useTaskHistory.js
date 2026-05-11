import { ref } from 'vue'

const STORAGE_KEY = 'lundao-tasks'
const STORAGE_VERSION_KEY = 'lundao-tasks-version'
const CURRENT_VERSION = '2' // Version 2: Image-based PPT preview (2025-01-17)
const MAX_TASKS = 50 // Keep max 50 recent tasks when pruning
const TASK_EXPIRY_HOURS = 24 // Remove tasks older than 24 hours

/**
 * Composable for managing task history in localStorage
 */
export function useTaskHistory() {
  const error = ref(null)

  /**
   * Save tasks to localStorage
   * @param {Array} tasks - Array of task objects
   */
  const saveTasksToLocalStorage = (tasks) => {
    try {
      const jsonData = JSON.stringify(tasks)
      localStorage.setItem(STORAGE_KEY, jsonData)
      localStorage.setItem(STORAGE_VERSION_KEY, CURRENT_VERSION)
      error.value = null
    } catch (err) {
      if (err.name === 'QuotaExceededError') {
        console.warn('localStorage quota exceeded, attempting to prune old tasks')
        // Prune oldest completed tasks
        const prunedTasks = pruneOldTasks(tasks)
        try {
          const jsonData = JSON.stringify(prunedTasks)
          localStorage.setItem(STORAGE_KEY, jsonData)
          error.value = 'Storage limit reached. Oldest tasks removed.'
        } catch (retryErr) {
          console.error('Failed to save even after pruning:', retryErr)
          error.value = 'Failed to save task history'
        }
      } else {
        console.error('Error saving to localStorage:', err)
        error.value = 'Failed to save task history'
      }
    }
  }

  /**
   * Load tasks from localStorage
   * @returns {Array} Array of task objects
   */
  const loadTasksFromLocalStorage = () => {
    try {
      // Check version compatibility
      const storedVersion = localStorage.getItem(STORAGE_VERSION_KEY)
      if (storedVersion !== CURRENT_VERSION) {
        console.log(`[Task History] Version mismatch (stored: ${storedVersion}, current: ${CURRENT_VERSION}). Clearing old data.`)
        localStorage.removeItem(STORAGE_KEY)
        localStorage.setItem(STORAGE_VERSION_KEY, CURRENT_VERSION)
        return []
      }

      const jsonData = localStorage.getItem(STORAGE_KEY)
      if (!jsonData) return []

      const tasks = JSON.parse(jsonData)
      // Clear expired tasks on load
      const validTasks = clearExpiredTasks(tasks)
      return validTasks
    } catch (err) {
      console.error('Error loading from localStorage:', err)
      return []
    }
  }

  /**
   * Clear expired tasks (older than 24 hours)
   * @param {Array} tasks - Array of task objects
   * @returns {Array} Filtered tasks
   */
  const clearExpiredTasks = (tasks) => {
    const now = new Date()
    const expiryTime = TASK_EXPIRY_HOURS * 60 * 60 * 1000 // 24 hours in ms

    return tasks.filter(task => {
      const taskDate = new Date(task.createdAt)
      return (now - taskDate) < expiryTime
    })
  }

  /**
   * Prune oldest completed tasks, keeping max 50 recent
   * @param {Array} tasks - Array of task objects
   * @returns {Array} Pruned tasks
   */
  const pruneOldTasks = (tasks) => {
    // Keep all active tasks (queued, generating)
    const activeTasks = tasks.filter(t => t.status === 'queued' || t.status === 'generating')

    // Sort completed/failed tasks by date, keep most recent MAX_TASKS
    const completedTasks = tasks
      .filter(t => t.status === 'completed' || t.status === 'failed')
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      .slice(0, MAX_TASKS)

    return [...activeTasks, ...completedTasks]
  }

  return {
    saveTasksToLocalStorage,
    loadTasksFromLocalStorage,
    clearExpiredTasks,
    error,
  }
}
