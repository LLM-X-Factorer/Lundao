import apiClient from './index'
import { mockCreatePPTTask, mockPollTaskStatus } from '@/mocks/taskService'

// Environment-based mock mode detection
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

/**
 * Create PPT generation task
 * @param {string} paperId - Paper ID (arxivId or fileId)
 * @param {boolean} isArxiv - Whether this is an arXiv paper (true) or uploaded PDF (false)
 * @returns {Promise<Object>} Response containing taskId
 */
export const createPPTTask = async (paperId, isArxiv = true) => {
  // Route to mock service in mock mode
  if (USE_MOCK_DATA) {
    return mockCreatePPTTask(paperId, isArxiv)
  }

  // Real API call
  const requestBody = isArxiv ? { arxivId: paperId } : { fileId: paperId }

  const response = await apiClient.post('/generate_ppt', requestBody, {
    timeout: 30000, // 30 seconds for task creation
  })

  return response.data
}

/**
 * Poll task status
 * @param {string} taskId - Task ID to check
 * @returns {Promise<Object>} Task status data
 */
export const pollTaskStatus = async (taskId) => {
  // Route to mock service in mock mode
  if (USE_MOCK_DATA) {
    return mockPollTaskStatus(taskId)
  }

  // Real API call
  const response = await apiClient.get('/task_status', {
    params: { taskId },
    timeout: 10000, // 10 seconds for polling requests
  })

  return response.data
}
