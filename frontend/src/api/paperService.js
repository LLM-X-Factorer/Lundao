import apiClient from './index'

/**
 * Fetch trending arXiv papers by period
 * @param {string} period - 'daily', 'weekly', or 'monthly'
 * @param {number} page - Page number (1-indexed)
 * @param {number} limit - Number of papers per page (default: 20)
 * @returns {Promise<Object>} Response containing papers array and pagination info
 */
export const fetchArxivPapers = async (period = 'daily', page = 1, limit = 20) => {
  const response = await apiClient.get('/arxiv_papers', {
    params: { period, page, limit },
    timeout: 30000, // 30 seconds for paper fetching
  })
  return response.data
}

/**
 * Get AI analysis for a paper
 * @param {string} paperId - Paper ID (arxivId or fileId)
 * @param {boolean} isArxiv - Whether this is an arXiv paper (true) or uploaded PDF (false)
 * @returns {Promise<Object>} Analysis data with Chinese summary and innovation points
 */
export const analyzePaper = async (paperId, isArxiv = true) => {
  const params = isArxiv ? { arxivId: paperId } : { fileId: paperId }

  const response = await apiClient.get('/analyze_paper', {
    params,
    timeout: 65000, // 65 seconds (longer than backend 60s timeout)
  })

  return response.data
}
