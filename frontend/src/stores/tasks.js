import { defineStore } from 'pinia'
import { ref, computed, onUnmounted } from 'vue'
import { createPPTTask, pollTaskStatus } from '@/api/taskService'
import { useTaskHistory } from '@/composables/useTaskHistory'
import { mockHistoricalTasks } from '@/mocks/taskData'

// Environment-based mock mode detection
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const useTasksStore = defineStore('tasks', () => {
  const { saveTasksToLocalStorage, loadTasksFromLocalStorage } = useTaskHistory()

  // State
  const tasks = ref([])
  const pollingActive = ref(false)
  let pollingInterval = null

  // Computed
  const activeTasks = computed(() =>
    tasks.value.filter(task => task.status === 'queued' || task.status === 'generating')
  )

  // Load tasks from localStorage on initialization
  const storedTasks = loadTasksFromLocalStorage()

  // Initialize with mock historical tasks if empty and in mock mode
  if (USE_MOCK_DATA && storedTasks.length === 0) {
    // First time in mock mode: load historical tasks
    tasks.value = [...mockHistoricalTasks]
    saveTasksToLocalStorage(tasks.value)
  } else {
    tasks.value = storedTasks
  }

  // Handle page refresh for orphaned mock tasks
  if (USE_MOCK_DATA) {
    tasks.value = tasks.value.map(task => {
      if (task.id.startsWith('mock-task-') &&
          ['queued', 'generating'].includes(task.status)) {
        return {
          ...task,
          status: 'failed',
          errorMessage: '页面刷新导致任务中断 (Mock模式)'
        }
      }
      return task
    })
    saveTasksToLocalStorage(tasks.value)
  }

  // Actions
  const createTask = async (paperId, paperTitle, isArxiv = true) => {
    try {
      const response = await createPPTTask(paperId, isArxiv)

      const newTask = {
        id: response.taskId,
        paperId,
        paperTitle,
        status: 'queued',
        createdAt: new Date().toISOString(),
        completedAt: null,
        downloadUrl: null,
        errorMessage: null,
        progress: null,
        retryCount: 0,
      }

      tasks.value.unshift(newTask)
      saveTasksToLocalStorage(tasks.value)

      // Start polling if not already active
      if (!pollingActive.value && activeTasks.value.length > 0) {
        startPolling()
      }

      return newTask
    } catch (error) {
      console.error('Error creating task:', error)
      throw error
    }
  }

  const updateTaskStatus = (taskId, statusData) => {
    const taskIndex = tasks.value.findIndex(t => t.id === taskId)
    if (taskIndex !== -1) {
      tasks.value[taskIndex] = {
        ...tasks.value[taskIndex],
        status: statusData.status,
        progress: statusData.progress || null,
        completedAt: statusData.status === 'completed' ? new Date().toISOString() : null,
        downloadUrl: statusData.downloadUrl || null,
        errorMessage: statusData.errorMessage || null,
      }
      saveTasksToLocalStorage(tasks.value)
    }
  }

  const startPolling = () => {
    if (pollingActive.value) return

    pollingActive.value = true
    pollingInterval = setInterval(async () => {
      const active = activeTasks.value

      if (active.length === 0) {
        stopPolling()
        return
      }

      // Poll all active tasks using Promise.allSettled
      const pollPromises = active.map(task =>
        pollTaskStatus(task.id)
          .then(statusData => ({ taskId: task.id, statusData, success: true }))
          .catch(error => ({ taskId: task.id, error, success: false }))
      )

      const results = await Promise.allSettled(pollPromises)

      results.forEach(result => {
        if (result.status === 'fulfilled' && result.value.success) {
          updateTaskStatus(result.value.taskId, result.value.statusData)
        }
      })
    }, 5000) // 5 seconds
  }

  const stopPolling = () => {
    if (pollingInterval) {
      clearInterval(pollingInterval)
      pollingInterval = null
    }
    pollingActive.value = false
  }

  const deleteTask = (taskId) => {
    tasks.value = tasks.value.filter(t => t.id !== taskId)
    saveTasksToLocalStorage(tasks.value)
  }

  const loadTasksFromStorage = () => {
    tasks.value = loadTasksFromLocalStorage()
  }

  const retryTask = async (taskId) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (!task) return

    // Increment retry count
    task.retryCount = (task.retryCount || 0) + 1

    if (task.retryCount > 3) {
      throw new Error('重试次数过多，请稍后再试')
    }

    // Create a new task (same paper)
    await createTask(task.paperId, task.paperTitle)
  }

  // Auto-start polling if there are active tasks on mount
  if (activeTasks.value.length > 0) {
    startPolling()
  }

  // Clean up polling on unmount
  onUnmounted(() => {
    stopPolling()
  })

  return {
    // State
    tasks,
    pollingActive,

    // Computed
    activeTasks,

    // Actions
    createTask,
    updateTaskStatus,
    startPolling,
    stopPolling,
    deleteTask,
    loadTasksFromStorage,
    retryTask,
  }
})
