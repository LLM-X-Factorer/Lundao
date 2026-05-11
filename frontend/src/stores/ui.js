import { defineStore } from 'pinia'
import { ref } from 'vue'
import { analyzePaper } from '@/api/paperService'
import { getPPTContent } from '@/api/pptContentService'
import { usePapersStore } from './papers'
import { useTasksStore } from './tasks'
import { generateMockAnalysis } from '@/mocks/paperData'

// Mock mode flag - controlled by environment variable
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const useUiStore = defineStore('ui', () => {
  // State
  const modalOpen = ref(false)
  const currentPaper = ref(null)
  const currentAnalysis = ref(null)
  const analysisLoading = ref(false)

  const toastVisible = ref(false)
  const toastMessage = ref('')
  const toastType = ref('info') // 'success', 'error', 'info'
  let toastTimeout = null

  // PPT Preview State
  const pptPreviewOpen = ref(false)
  const currentPPTContent = ref(null)
  const pptContentLoading = ref(false)
  const pptContentError = ref(null)

  // Actions
  const openModal = async (paperId, retryCount = 0) => {
    const papersStore = usePapersStore()

    // Find paper from papers store
    const paper = papersStore.papers.find(p => p.id === paperId)
    if (!paper) {
      showToast('论文未找到', 'error')
      return
    }

    currentPaper.value = paper
    modalOpen.value = true
    analysisLoading.value = true
    currentAnalysis.value = null

    // Determine if it's an arXiv paper or uploaded file
    const isArxiv = paper.source === 'arxiv'

    try {
      let response

      if (USE_MOCK_DATA) {
        // Use mock analysis data
        await new Promise(resolve => setTimeout(resolve, 800)) // Simulate API delay
        response = generateMockAnalysis(paper)
      } else {
        // Try real API first, fallback to mock on failure
        try {
          response = await analyzePaper(paperId, isArxiv)

          // Handle 202 (pending) response with retry logic
          if (response.analysisStatus === 'pending' && retryCount < 3) {
            const retryAfter = response.retryAfter || 15 // Default 15 seconds
            console.log(`Analysis pending, retrying in ${retryAfter}s... (attempt ${retryCount + 1}/3)`)

            setTimeout(() => {
              openModal(paperId, retryCount + 1)
            }, retryAfter * 1000)
            return
          }

          if (response.analysisStatus === 'pending' && retryCount >= 3) {
            throw new Error('分析耗时过长，请稍后重试。')
          }
        } catch (apiErr) {
          console.warn('API analysis failed, falling back to mock data:', apiErr.message)
          // Auto-fallback to mock analysis when API is unreachable
          await new Promise(resolve => setTimeout(resolve, 800))
          response = generateMockAnalysis(paper)
          showToast('演示模式：使用模拟分析数据', 'info')
        }
      }

      currentAnalysis.value = response
    } catch (error) {
      console.error('Error fetching analysis:', error)
      showToast(error.message || '加载分析失败', 'error')
    } finally {
      analysisLoading.value = false
    }
  }

  const closeModal = () => {
    modalOpen.value = false
    currentPaper.value = null
    currentAnalysis.value = null
    analysisLoading.value = false
  }

  const showToast = (message, type = 'info') => {
    if (toastTimeout) {
      clearTimeout(toastTimeout)
    }

    toastMessage.value = message
    toastType.value = type
    toastVisible.value = true

    toastTimeout = setTimeout(() => {
      hideToast()
    }, 3000) // Auto-dismiss after 3 seconds
  }

  const hideToast = () => {
    toastVisible.value = false
    if (toastTimeout) {
      clearTimeout(toastTimeout)
      toastTimeout = null
    }
  }

  const openPPTPreview = async (taskId) => {
    // Clear previous state
    currentPPTContent.value = null
    pptContentError.value = null
    pptContentLoading.value = true
    pptPreviewOpen.value = true

    try {
      // Find task object from tasks store to extract paperId
      const tasksStore = useTasksStore()
      const task = tasksStore.tasks.find(t => t.id === taskId)

      console.log('[UI Store] Opening PPT preview for taskId:', taskId)
      console.log('[UI Store] Found task object:', task)

      // Pass both taskId and task object for smart lookup (paperId-first strategy)
      const content = await getPPTContent(taskId, task)
      currentPPTContent.value = content
    } catch (error) {
      console.error('Error fetching PPT content:', error)
      pptContentError.value = error.message || '加载PPT内容失败'
      showToast(pptContentError.value, 'error')
      // Keep modal open to show error state
    } finally {
      pptContentLoading.value = false
    }
  }

  const closePPTPreview = () => {
    pptPreviewOpen.value = false
    currentPPTContent.value = null
    pptContentError.value = null
    pptContentLoading.value = false
  }

  return {
    // State
    modalOpen,
    currentPaper,
    currentAnalysis,
    analysisLoading,
    toastVisible,
    toastMessage,
    toastType,
    pptPreviewOpen,
    currentPPTContent,
    pptContentLoading,
    pptContentError,

    // Actions
    openModal,
    closeModal,
    showToast,
    hideToast,
    openPPTPreview,
    closePPTPreview,
  }
})
