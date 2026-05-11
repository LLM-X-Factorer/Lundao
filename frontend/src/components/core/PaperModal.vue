<script setup>
import { computed, ref } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useTasksStore } from '@/stores/tasks'
import Modal from '@/components/common/Modal.vue'
import Button from '@/components/common/Button.vue'

const uiStore = useUiStore()
const tasksStore = useTasksStore()

// Reduced motion preference detection for accessibility
const prefersReducedMotion = ref(
  window.matchMedia('(prefers-reduced-motion: reduce)').matches
)

const handleClose = () => {
  uiStore.closeModal()
}

const handleGeneratePPT = async () => {
  if (!uiStore.currentPaper) return

  try {
    await tasksStore.createTask(uiStore.currentPaper.id, uiStore.currentPaper.title)
    uiStore.showToast('PPT生成任务已创建', 'success')
    uiStore.closeModal()
  } catch (error) {
    console.error('Failed to create PPT task:', error)
    uiStore.showToast('创建PPT任务失败，请重试', 'error')
  }
}

const canGeneratePPT = computed(() => {
  return uiStore.currentAnalysis && uiStore.currentAnalysis.analysisStatus === 'completed'
})

const formatAuthors = (authors) => {
  if (!authors || authors.length === 0) return 'Unknown'
  return authors.join(', ')
}

// Normalize innovation points to support both old (string) and new (object) formats
const normalizedInnovationPoints = computed(() => {
  if (!uiStore.currentAnalysis?.innovationPoints) return []

  return uiStore.currentAnalysis.innovationPoints.map((point, index) => {
    // If point is already an object with required fields, return as-is
    if (typeof point === 'object' && point.icon && point.title && point.description) {
      return point
    }

    // If point is a string (old format), convert to new format
    if (typeof point === 'string') {
      return {
        icon: '💡', // Default icon for legacy data
        iconLabel: 'Innovation',
        title: point.slice(0, 30) + (point.length > 30 ? '...' : ''), // First 30 chars as title
        description: point // Full text as description
      }
    }

    // Fallback for unexpected formats
    return {
      icon: '💡',
      iconLabel: 'Innovation',
      title: `创新点 ${index + 1}`,
      description: String(point)
    }
  })
})
</script>

<template>
  <Modal
    :open="uiStore.modalOpen"
    @close="handleClose"
  >
    <div v-if="uiStore.currentPaper">
      <!-- Paper Title + Metadata Group -->
      <div class="mb-6">
        <!-- Paper Title -->
        <h2 class="text-xl lg:text-2xl font-bold text-text-primary mb-2 leading-tight">
          {{ uiStore.currentPaper.title }}
        </h2>

        <!-- Paper Metadata (Subtitle) -->
        <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-text-secondary">
          <div class="flex items-center gap-1">
            <span class="font-medium">作者:</span>
            <span>{{ formatAuthors(uiStore.currentPaper.authors) }}</span>
          </div>

          <div v-if="uiStore.currentPaper.field" class="flex items-center gap-1">
            <span class="font-medium">领域:</span>
            <span>{{ uiStore.currentPaper.field }}</span>
          </div>

          <div v-if="uiStore.currentPaper.publicationDate" class="flex items-center gap-1">
            <span class="font-medium">日期:</span>
            <span>{{ new Date(uiStore.currentPaper.publicationDate).toLocaleDateString('zh-CN') }}</span>
          </div>
        </div>
      </div>

      <!-- Main Content Area -->
      <div>
        <!-- Loading State -->
        <div v-if="uiStore.analysisLoading" class="space-y-6">
          <div class="animate-pulse">
            <!-- Summary Skeleton -->
            <div class="mb-6">
              <div class="h-4 bg-gray-200 rounded w-32 mb-3"></div>
              <div class="bg-gray-100 rounded-lg p-4">
                <div class="space-y-2">
                  <div class="h-3 bg-gray-200 rounded w-full"></div>
                  <div class="h-3 bg-gray-200 rounded w-full"></div>
                  <div class="h-3 bg-gray-200 rounded w-4/5"></div>
                </div>
              </div>
            </div>

            <!-- Innovation Points Skeleton (2 columns, 6 cards) -->
            <div class="mb-6">
              <div class="h-4 bg-gray-200 rounded w-24 mb-4"></div>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div v-for="i in 6" :key="i" class="border border-gray-200 rounded-lg p-3 flex gap-3">
                  <div class="flex-shrink-0 w-8 h-8 bg-gray-200 rounded"></div>
                  <div class="flex-1 space-y-2">
                    <div class="h-3 bg-gray-200 rounded w-3/4"></div>
                    <div class="h-2 bg-gray-200 rounded w-full"></div>
                    <div class="h-2 bg-gray-200 rounded w-5/6"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Analysis Content -->
        <div v-else-if="uiStore.currentAnalysis">
          <!-- Error State -->
          <div v-if="uiStore.currentAnalysis.analysisStatus === 'failed'" class="mb-6">
            <div class="bg-red-50 border-l-4 border-error px-4 py-3 rounded">
              <p class="text-error font-medium">分析失败</p>
              <p class="text-sm text-red-700 mt-1">
                {{ uiStore.currentAnalysis.errorMessage || '无法分析此论文，可能是PDF格式不支持或内容无法解析。' }}
              </p>
            </div>
          </div>

          <!-- Success State -->
          <div v-else-if="uiStore.currentAnalysis.analysisStatus === 'completed'">
            <!-- Chinese Summary (Prominent) -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-text-primary mb-3">📝 中文摘要</h3>
              <div class="bg-gradient-summary rounded-lg p-4">
                <p class="text-base text-text-primary leading-relaxed whitespace-pre-wrap">
                  {{ uiStore.currentAnalysis.chineseSummary }}
                </p>
              </div>
            </div>

            <!-- Innovation Points (Full Width, 2 Columns) -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-text-primary mb-4">💡 创新点</h3>
              <TransitionGroup
                v-if="!prefersReducedMotion"
                name="fade-slide"
                tag="div"
                class="grid grid-cols-1 lg:grid-cols-2 gap-4"
              >
                <article
                  v-for="(point, index) in normalizedInnovationPoints"
                  :key="index"
                  class="border border-border-color rounded-lg p-3 motion-safe:transition-all motion-safe:duration-200 hover:shadow-md hover:-translate-y-1"
                  :style="{ transitionDelay: `${index * 50}ms` }"
                  role="article"
                  :aria-labelledby="`innovation-${index}`"
                >
                  <div class="flex gap-3">
                    <div class="flex-shrink-0">
                      <span class="text-2xl" role="img" :aria-label="point.iconLabel">
                        {{ point.icon }}
                      </span>
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 :id="`innovation-${index}`" class="font-semibold text-sm mb-1 text-text-primary">
                        {{ point.title }}
                      </h4>
                      <p class="text-xs text-text-secondary leading-relaxed">
                        {{ point.description }}
                      </p>
                    </div>
                  </div>
                </article>
              </TransitionGroup>
              <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <article
                  v-for="(point, index) in normalizedInnovationPoints"
                  :key="index"
                  class="border border-border-color rounded-lg p-3"
                  role="article"
                  :aria-labelledby="`innovation-${index}`"
                >
                  <div class="flex gap-3">
                    <div class="flex-shrink-0">
                      <span class="text-2xl" role="img" :aria-label="point.iconLabel">
                        {{ point.icon }}
                      </span>
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 :id="`innovation-${index}`" class="font-semibold text-sm mb-1 text-text-primary">
                        {{ point.title }}
                      </h4>
                      <p class="text-xs text-text-secondary leading-relaxed">
                        {{ point.description }}
                      </p>
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </div>

          <!-- Pending State -->
          <div v-else-if="uiStore.currentAnalysis.analysisStatus === 'pending'" class="mb-6">
            <div class="bg-yellow-50 border-l-4 border-yellow-500 px-4 py-3 rounded">
              <p class="text-yellow-800 font-medium">分析进行中...</p>
              <p class="text-sm text-yellow-700 mt-1">
                AI正在分析论文，请稍候...
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons (Bottom, Centered) -->
      <div class="mt-6 pt-6 border-t border-border-color">
        <div class="flex flex-wrap items-center justify-center gap-3">
          <Button
            variant="primary"
            :disabled="!canGeneratePPT || tasksStore.loading"
            :loading="tasksStore.loading"
            class="min-w-[160px]"
            @click="handleGeneratePPT"
          >
            一键生成组会PPT
          </Button>

          <Button
            v-if="uiStore.currentPaper.pdfUrl"
            variant="secondary"
            class="min-w-[160px]"
          >
            <a
              :href="uiStore.currentPaper.pdfUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center justify-center gap-2 w-full"
            >
              <svg
                class="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
                />
              </svg>
              <span>下载原文PDF</span>
            </a>
          </Button>
        </div>
      </div>
    </div>
  </Modal>
</template>

<style scoped>
/* Fade-slide animation for innovation point cards */
.fade-slide-enter-active {
  transition: opacity 200ms, transform 200ms;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

/* Hover effects for innovation cards (only on devices with hover capability) */
@media (hover: hover) {
  .hover\:shadow-md:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .hover\:-translate-y-1:hover {
    transform: translateY(-4px);
  }
}
</style>
