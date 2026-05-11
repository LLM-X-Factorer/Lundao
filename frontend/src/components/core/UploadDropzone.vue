<script setup>
import { ref, computed } from 'vue'
import { useFileUpload } from '@/composables/useFileUpload'
import { useUiStore } from '@/stores/ui'
import { useTasksStore } from '@/stores/tasks'

const uiStore = useUiStore()
const tasksStore = useTasksStore()
const { progress, uploading, error, uploadFile } = useFileUpload()

const isDragging = ref(false)
const selectedFile = ref(null)

const handleDragOver = (e) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDragging.value = false

  const files = e.dataTransfer.files
  if (files.length > 0) {
    handleFileSelection(files[0])
  }
}

const handleFileInput = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    handleFileSelection(files[0])
  }
}

const handleFileSelection = (file) => {
  console.log('[Upload] File selected:', file.name, file.type, file.size)

  // Validate file type
  if (file.type !== 'application/pdf') {
    error.value = '请上传PDF文件'
    selectedFile.value = null
    console.error('[Upload] Invalid file type:', file.type)
    setTimeout(() => {
      error.value = null
    }, 5000)
    return
  }

  // Validate file size (20MB)
  const maxSize = 20 * 1024 * 1024
  if (file.size > maxSize) {
    error.value = '文件大小超过20MB限制'
    selectedFile.value = null
    console.error('[Upload] File too large:', file.size, 'bytes')
    setTimeout(() => {
      error.value = null
    }, 5000)
    return
  }

  selectedFile.value = file
  error.value = null
  console.log('[Upload] File validation passed, ready to upload')
}

const removeFile = () => {
  selectedFile.value = null
  error.value = null
  progress.value = 0
}

const handleUpload = async () => {
  if (!selectedFile.value) return

  try {
    console.log('[Upload] Starting upload for file:', selectedFile.value.name)
    const response = await uploadFile(selectedFile.value)
    console.log('[Upload] Upload response:', response)

    // After successful upload, create PPT generation task
    if (response && response.fileId) {
      uiStore.showToast('上传成功！正在生成PPT...', 'success')

      // In mock mode, use the paperId from response (daily-0001)
      // In real mode, use the fileId as paperId
      const paperId = response.paperId || response.fileId
      const fileName = response.fileName || selectedFile.value.name
      const paperTitle = `上传论文: ${fileName.replace('.pdf', '')}`

      console.log('[Upload] Creating PPT task for paperId:', paperId, 'title:', paperTitle)

      try {
        // Create a new PPT generation task
        // For uploaded files, isArxiv = false
        await tasksStore.createTask(paperId, paperTitle, false)
        console.log('[Upload] Task created successfully')

        removeFile()

        // Scroll to task history section
        setTimeout(() => {
          const taskHistorySection = document.querySelector('section:last-of-type')
          if (taskHistorySection) {
            taskHistorySection.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        }, 500)
      } catch (taskError) {
        console.error('[Upload] Task creation error:', taskError)
        uiStore.showToast('任务创建失败: ' + (taskError.message || '未知错误'), 'error')
      }
    } else {
      console.error('[Upload] Invalid response - missing fileId:', response)
      uiStore.showToast('上传响应数据异常', 'error')
    }
  } catch (err) {
    console.error('[Upload] Upload error:', err)
    // Error is already set by useFileUpload composable
    // Show additional toast if error is not already displayed
    if (!error.value) {
      uiStore.showToast('上传失败: ' + (err.message || '未知错误'), 'error')
    }
  }
}

const progressText = computed(() => {
  if (progress.value === 0) return ''
  if (progress.value < 25) return '准备上传...'
  if (progress.value < 75) return `上传中... ${progress.value}%`
  if (progress.value < 100) return '完成中...'
  return '上传完成！分析中...'
})

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 10) / 10 + ' ' + sizes[i]
}
</script>

<template>
  <div class="w-full">
    <!-- Dropzone -->
    <div
      :class="[
        'relative border-2 border-dashed rounded-lg p-8 transition-all duration-200',
        isDragging
          ? 'border-accent bg-blue-50'
          : error
            ? 'border-error bg-red-50'
            : 'border-border-color bg-secondary-bg hover:border-accent',
        uploading ? 'pointer-events-none opacity-75' : 'cursor-pointer'
      ]"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
    >
      <!-- File Input - Hide when file is selected to allow button clicks -->
      <input
        v-if="!selectedFile"
        type="file"
        accept="application/pdf"
        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        :disabled="uploading"
        @change="handleFileInput"
      />

      <div class="text-center">
        <!-- Upload Icon -->
        <svg
          class="mx-auto h-12 w-12 mb-4"
          :class="isDragging ? 'text-accent' : error ? 'text-error' : 'text-text-secondary'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>

        <!-- Upload Text -->
        <div v-if="!selectedFile">
          <p class="text-base font-medium text-text-primary mb-1">
            拖拽PDF文件到此处，或点击选择文件
          </p>
          <p class="text-sm text-text-secondary">
            支持PDF格式，最大20MB
          </p>
        </div>

        <!-- Selected File Preview -->
        <div v-else-if="!uploading" class="flex items-center justify-center gap-4">
          <div class="flex items-center gap-3 bg-primary-bg px-4 py-3 rounded-md border border-border-color">
            <svg class="h-8 w-8 text-error" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
                clip-rule="evenodd"
              />
            </svg>
            <div class="text-left">
              <p class="text-sm font-medium text-text-primary">{{ selectedFile.name }}</p>
              <p class="text-xs text-text-secondary">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <button
              type="button"
              class="text-text-secondary hover:text-error transition-colors"
              @click.stop="removeFile"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <button
            type="button"
            class="px-6 py-2 bg-accent text-white rounded-md hover:bg-blue-600 transition-colors font-medium"
            @click="() => { console.log('[Upload] Button clicked!'); handleUpload(); }"
          >
            开始上传
          </button>
        </div>

        <!-- Upload Progress -->
        <div v-else>
          <p class="text-sm font-medium text-text-primary mb-3">{{ progressText }}</p>
          <div class="w-full max-w-md mx-auto bg-gray-200 rounded-full h-2.5">
            <div
              class="bg-accent h-2.5 rounded-full transition-all duration-300"
              :style="{ width: `${progress}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-3">
      <div class="bg-red-50 border-l-4 border-error px-4 py-3 rounded">
        <p class="text-sm text-error font-medium">{{ error }}</p>
      </div>
    </div>
  </div>
</template>
