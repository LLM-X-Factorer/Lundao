import apiClient from './index'
import { getMockPPTContentByTask } from '@/mocks/pptContentData'

// Mock模式检测
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

/**
 * 获取PPT内容
 * @param {string} taskId - 任务ID
 * @param {Object} task - 完整的任务对象（仅Mock模式需要，用于获取paperId）
 * @returns {Promise<Object>} PPTContent对象
 */
export async function getPPTContent(taskId, task = null) {
  if (USE_MOCK_DATA) {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    return getMockPPTContentByTask(taskId, task)
  }

  // Real API
  const response = await apiClient.get('/ppt_content', {
    params: { taskId }
  })
  return response.data
}
