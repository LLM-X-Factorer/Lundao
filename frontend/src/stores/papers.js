import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchArxivPapers } from '@/api/paperService'
import { dailyPapers, weeklyPapers, monthlyPapers } from '@/mocks/paperData'

// Mock mode flag - controlled by environment variable
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const usePapersStore = defineStore('papers', () => {
  // State
  const papers = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedPeriod = ref('daily')
  const currentPage = ref(1)
  const totalPages = ref(1)

  // Computed
  const hasPapers = computed(() => papers.value.length > 0)

  // Mock data fetcher
  const fetchMockPapers = (period = 'daily', page = 1) => {
    return new Promise((resolve) => {
      // Simulate network delay
      setTimeout(() => {
        const mockData = {
          daily: dailyPapers,
          weekly: weeklyPapers,
          monthly: monthlyPapers
        }

        const allPapers = mockData[period] || dailyPapers
        const pageSize = 8
        const total = Math.ceil(allPapers.length / pageSize)
        const start = (page - 1) * pageSize
        const end = start + pageSize
        const pagePapers = allPapers.slice(start, end)

        resolve({
          papers: pagePapers,
          totalPages: total,
          currentPage: page,
          totalCount: allPapers.length
        })
      }, 500) // 500ms delay to simulate API call
    })
  }

  // Actions
  const fetchPapers = async (period = 'daily', page = 1) => {
    loading.value = true
    error.value = null

    try {
      let response

      if (USE_MOCK_DATA) {
        // Use mock data when backend is not available
        response = await fetchMockPapers(period, page)
      } else {
        // Try real API first, fallback to mock on failure
        try {
          response = await fetchArxivPapers(period, page, 20)
        } catch (apiErr) {
          console.warn('API request failed, falling back to mock data:', apiErr.message)
          // Auto-fallback to mock data when API is unreachable
          response = await fetchMockPapers(period, page)
          // Show friendly info message instead of error
          error.value = '演示模式：当前使用模拟数据 (后端API未连接)'
        }
      }

      papers.value = response.papers || []
      totalPages.value = response.totalPages || 1
      currentPage.value = page
      selectedPeriod.value = period
    } catch (err) {
      // Final fallback: if even mock data fails, show error
      error.value = err.response?.data?.message || 'Failed to fetch papers'
      papers.value = []
      console.error('Error fetching papers:', err)
    } finally {
      loading.value = false
    }
  }

  const setPeriod = async (period) => {
    if (period !== selectedPeriod.value) {
      selectedPeriod.value = period
      currentPage.value = 1
      await fetchPapers(period, 1)
    }
  }

  const setPage = async (page) => {
    if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
      await fetchPapers(selectedPeriod.value, page)
    }
  }

  return {
    // State
    papers,
    loading,
    error,
    selectedPeriod,
    currentPage,
    totalPages,

    // Computed
    hasPapers,

    // Actions
    fetchPapers,
    setPeriod,
    setPage,
  }
})
