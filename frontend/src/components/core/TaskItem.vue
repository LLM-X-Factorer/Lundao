<script setup>
import { computed } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { useUiStore } from '@/stores/ui'
import Badge from '@/components/common/Badge.vue'
import Button from '@/components/common/Button.vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const tasksStore = useTasksStore()
const uiStore = useUiStore()

const handleDelete = () => {
  tasksStore.deleteTask(props.task.id)
}

const handleRetry = () => {
  tasksStore.retryTask(props.task.id)
}

const handleDownload = async (event) => {
  // Verify file exists before download
  const fileUrl = props.task.downloadUrl
  if (!fileUrl) {
    event.preventDefault()
    uiStore.showToast('下载链接不存在', 'error')
    return
  }

  try {
    // Check if file exists (HEAD request)
    const response = await fetch(fileUrl, { method: 'HEAD' })
    if (!response.ok) {
      event.preventDefault()
      uiStore.showToast('文件不存在或已过期，请重新生成', 'error')
      return
    }
  } catch (error) {
    console.error('Download verification failed:', error)
    event.preventDefault()
    uiStore.showToast('下载失败，请检查网络连接', 'error')
    return
  }

  // File exists, browser will handle download via <a> tag
}

const handlePreview = () => {
  uiStore.openPPTPreview(props.task.id)
}

const formatRelativeTime = (timestamp) => {
  if (!timestamp) return ''

  const now = new Date()
  const then = new Date(timestamp)
  const diffMs = now - then
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  if (diffSec < 60) return '刚刚'
  if (diffMin < 60) return `${diffMin}分钟前`
  if (diffHour < 24) return `${diffHour}小时前`
  if (diffDay === 1) return '昨天'
  if (diffDay < 7) return `${diffDay}天前`
  return then.toLocaleDateString('zh-CN')
}

const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 10) / 10 + ' ' + sizes[i]
}

const expirationWarning = computed(() => {
  if (props.task.status !== 'completed' || !props.task.expiresAt) return null

  const now = new Date()
  const expires = new Date(props.task.expiresAt)
  const diffHours = Math.floor((expires - now) / (1000 * 60 * 60))

  if (diffHours < 0) return '已过期'
  if (diffHours < 2) return `将在${diffHours}小时后过期`
  return null
})
</script>

<template>
  <div class="bg-primary-bg border border-border-color rounded-md p-4 hover:shadow-md transition-shadow">
    <!-- Header -->
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1">
        <h4 class="text-base font-semibold text-text-primary mb-1 line-clamp-1">
          {{ task.paperTitle }}
        </h4>
        <p class="text-xs text-text-secondary">
          {{ formatRelativeTime(task.createdAt) }}
        </p>
      </div>
      <div class="flex items-center gap-2">
        <Badge :status="task.status" />
        <button
          type="button"
          class="text-text-secondary hover:text-error transition-colors p-1"
          @click="handleDelete"
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
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Status-specific Content -->
    <div class="mt-3">
      <!-- Queued -->
      <div v-if="task.status === 'queued'" class="flex items-center gap-2 text-sm text-text-secondary">
        <svg
          class="animate-spin h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <span>排队等待生成...</span>
      </div>

      <!-- Generating -->
      <div v-else-if="task.status === 'generating'">
        <div class="flex items-center justify-between text-sm text-text-secondary mb-2">
          <span>正在生成PPT...</span>
          <span v-if="task.progress">{{ task.progress }}%</span>
        </div>
        <div v-if="task.progress" class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="bg-accent h-2 rounded-full transition-all duration-300"
            :style="{ width: `${task.progress}%` }"
          ></div>
        </div>
        <div v-else class="w-full bg-gray-200 rounded-full h-2">
          <div class="bg-accent h-2 rounded-full animate-pulse" style="width: 60%"></div>
        </div>
      </div>

      <!-- Completed -->
      <div v-else-if="task.status === 'completed'" class="space-y-3">
        <div class="flex items-center justify-between text-sm">
          <span class="text-text-secondary">
            完成于 {{ formatRelativeTime(task.completedAt) }}
          </span>
          <span v-if="task.fileSize" class="text-text-secondary">
            {{ formatFileSize(task.fileSize) }}
          </span>
        </div>

        <!-- Expiration Warning -->
        <div v-if="expirationWarning" class="text-xs text-yellow-700 bg-yellow-50 px-3 py-1 rounded">
          ⚠️ {{ expirationWarning }}
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-2">
          <!-- Preview Button -->
          <Button
            variant="secondary"
            size="small"
            @click="handlePreview"
          >
            <svg
              class="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
            预览
          </Button>

          <!-- Download Button -->
          <a
            v-if="task.downloadUrl"
            :href="task.downloadUrl"
            download
            class="inline-flex items-center gap-2 px-4 py-2 bg-success text-white rounded-md hover:bg-green-600 transition-colors text-sm font-medium"
            @click="handleDownload"
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
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            <span>下载PPT</span>
          </a>
        </div>
      </div>

      <!-- Failed -->
      <div v-else-if="task.status === 'failed'" class="space-y-3">
        <div class="bg-red-50 border-l-4 border-error px-3 py-2 rounded">
          <p class="text-sm text-error font-medium mb-1">生成失败</p>
          <p class="text-xs text-red-700">
            {{ task.errorMessage || '未知错误，请重试' }}
          </p>
        </div>

        <div class="flex gap-2">
          <Button
            variant="secondary"
            size="small"
            @click="handleRetry"
          >
            <svg
              class="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            重试
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
