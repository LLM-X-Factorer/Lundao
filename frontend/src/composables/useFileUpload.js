import { ref } from 'vue'
import { uploadPDF } from '@/api/uploadService'

const MAX_FILE_SIZE = 20 * 1024 * 1024 // 20MB in bytes

/**
 * Composable for managing file upload state and validation
 */
export function useFileUpload() {
  const progress = ref(0)
  const uploading = ref(false)
  const error = ref(null)
  const fileId = ref(null)

  /**
   * Validate PDF file
   * @param {File} file - File to validate
   * @returns {boolean} - True if valid, false otherwise
   */
  const validateFile = (file) => {
    error.value = null

    if (!file) {
      error.value = 'No file selected'
      return false
    }

    if (file.type !== 'application/pdf') {
      error.value = 'Only PDF files are supported'
      return false
    }

    if (file.size > MAX_FILE_SIZE) {
      const sizeMB = (file.size / (1024 * 1024)).toFixed(2)
      error.value = `File size (${sizeMB}MB) exceeds 20MB limit`
      return false
    }

    return true
  }

  /**
   * Upload file with progress tracking
   * @param {File} file - File to upload
   * @returns {Promise<Object>} - Upload response data
   */
  const uploadFile = async (file) => {
    if (!validateFile(file)) {
      throw new Error(error.value)
    }

    uploading.value = true
    progress.value = 0
    error.value = null
    fileId.value = null

    try {
      const response = await uploadPDF(file, (percent) => {
        progress.value = percent
      })

      fileId.value = response.fileId
      return response
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.message || 'Upload failed'
      error.value = errorMessage
      throw err
    } finally {
      uploading.value = false
    }
  }

  /**
   * Reset upload state
   */
  const reset = () => {
    progress.value = 0
    uploading.value = false
    error.value = null
    fileId.value = null
  }

  return {
    progress,
    uploading,
    error,
    fileId,
    validateFile,
    uploadFile,
    reset,
  }
}
