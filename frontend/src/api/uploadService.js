import apiClient from './index'

// Mock mode flag
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

/**
 * Mock upload implementation
 * Simulates file upload progress and returns a mock fileId
 * @param {File} file - PDF file to upload
 * @param {Function} onProgress - Progress callback (receives percentage 0-100)
 * @returns {Promise<Object>} Response containing fileId
 */
const mockUploadPDF = async (file, onProgress) => {
  console.log('[Mock Upload] Simulating file upload:', file.name)

  // Simulate upload progress
  const progressSteps = [0, 25, 50, 75, 100]
  for (const step of progressSteps) {
    await new Promise(resolve => setTimeout(resolve, 300))
    if (onProgress) {
      onProgress(step)
    }
  }

  // Return mock fileId (use daily-0001 as the target paper)
  const mockFileId = `upload-${Date.now()}-${Math.random().toString(36).substring(7)}`

  console.log('[Mock Upload] Upload completed, fileId:', mockFileId)

  return {
    fileId: mockFileId,
    fileName: file.name,
    fileSize: file.size,
    uploadedAt: new Date().toISOString(),
    // Link to daily-0001 paper for demonstration
    paperId: 'daily-0001'
  }
}

/**
 * Upload PDF file
 * @param {File} file - PDF file to upload
 * @param {Function} onProgress - Progress callback (receives percentage 0-100)
 * @returns {Promise<Object>} Response containing fileId and analysis data
 */
export const uploadPDF = async (file, onProgress) => {
  if (USE_MOCK_DATA) {
    return mockUploadPDF(file, onProgress)
  }

  // Real API upload
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/upload_pdf', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 120000, // 2 minutes for large files
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        if (onProgress) {
          onProgress(percentCompleted)
        }
      }
    },
  })

  return response.data
}
