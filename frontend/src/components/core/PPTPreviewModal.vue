<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { useUiStore } from '@/stores/ui'
import { getAllSlideUrls } from '@/config/pptImages'
import Button from '@/components/common/Button.vue'
import Watermark from '@/components/common/Watermark.vue'
import { watermarkConfig } from '@/config/watermark'

const uiStore = useUiStore()

// Local state
const currentSlideIndex = ref(0)
const slideUrls = ref([])
const imageLoading = ref(true)
const imageError = ref(null)
const closeButtonRef = ref(null)
const currentImageLoaded = ref(false)

// Computed
const paperTitle = computed(() => {
  return uiStore.currentPPTContent?.metadata?.paperTitle || '无标题'
})

const totalSlides = computed(() => slideUrls.value.length)

const currentSlideUrl = computed(() => {
  return slideUrls.value[currentSlideIndex.value]?.url || ''
})

const canGoPrev = computed(() => currentSlideIndex.value > 0)
const canGoNext = computed(() => currentSlideIndex.value < totalSlides.value - 1)

// Methods
const nextSlide = () => {
  if (canGoNext.value) {
    currentSlideIndex.value++
    currentImageLoaded.value = false
  }
}

const prevSlide = () => {
  if (canGoPrev.value) {
    currentSlideIndex.value--
    currentImageLoaded.value = false
  }
}

const goToSlide = (index) => {
  if (index >= 0 && index < totalSlides.value) {
    currentSlideIndex.value = index
    currentImageLoaded.value = false
  }
}

const close = () => {
  uiStore.closePPTPreview()
}

const loadSlides = () => {
  try {
    const content = uiStore.currentPPTContent
    if (!content) {
      imageError.value = '无PPT内容可预览'
      imageLoading.value = false
      return
    }

    if (content.type !== 'images') {
      imageError.value = '不支持的PPT内容格式'
      imageLoading.value = false
      return
    }

    const paperId = content.paperId
    if (!paperId) {
      imageError.value = '缺少论文ID信息'
      imageLoading.value = false
      return
    }

    // 从content获取实际幻灯片数量
    const slideCount = content.totalSlides || 14  // 默认14张
    slideUrls.value = getAllSlideUrls(paperId, slideCount)

    if (slideUrls.value.length === 0) {
      imageError.value = '未找到PPT截图'
      imageLoading.value = false
      return
    }

    currentSlideIndex.value = 0
    imageError.value = null
    imageLoading.value = false
    currentImageLoaded.value = false
  } catch (error) {
    console.error('Load slides error:', error)
    imageError.value = error.message || '加载失败'
    imageLoading.value = false
  }
}

const handleImageLoad = () => {
  currentImageLoaded.value = true
}

const handleImageError = () => {
  imageError.value = `图片加载失败：slide-${currentSlideIndex.value + 1}.png`
  currentImageLoaded.value = false
}

// Keyboard navigation
const handleKeydown = (e) => {
  if (!uiStore.pptPreviewOpen) return

  switch (e.key) {
    case 'ArrowRight':
      nextSlide()
      break
    case 'ArrowLeft':
      prevSlide()
      break
    case 'Escape':
      close()
      break
    case 'Home':
      goToSlide(0)
      break
    case 'End':
      goToSlide(totalSlides.value - 1)
      break
  }
}

// Watch for content changes and load slides
watch(
  () => uiStore.currentPPTContent,
  (newContent) => {
    if (newContent) {
      imageLoading.value = true
      loadSlides()
    }
  },
  { immediate: true }
)

// Focus management
watch(
  () => uiStore.pptPreviewOpen,
  (isOpen) => {
    if (isOpen) {
      nextTick(() => {
        closeButtonRef.value?.focus()
      })
    } else {
      // Reset state when modal closes
      currentSlideIndex.value = 0
      slideUrls.value = []
      imageError.value = null
      imageLoading.value = true
      currentImageLoaded.value = false
    }
  }
)

// Lifecycle
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <TransitionRoot :show="uiStore.pptPreviewOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="close">
      <!-- Backdrop -->
      <TransitionChild
        as="template"
        enter="ease-out duration-200"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-150"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      </TransitionChild>

      <!-- Modal container -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:scale-95"
          >
            <DialogPanel class="relative transform rounded-xl bg-primary-bg shadow-xl transition-all w-full max-w-6xl">
              <div class="ppt-preview-container h-[85vh] flex flex-col">
                <!-- Header -->
                <div class="flex items-center justify-between px-6 py-4 border-b border-border-color bg-white rounded-t-xl">
                  <div class="flex-1 pr-8">
                    <h3 class="text-xl font-semibold text-text-primary line-clamp-1">
                      {{ paperTitle }}
                    </h3>
                    <p v-if="uiStore.currentPPTContent?.metadata" class="text-sm text-text-secondary mt-1">
                      {{ uiStore.currentPPTContent.metadata.author }} ·
                      {{ uiStore.currentPPTContent.metadata.field }}
                    </p>
                  </div>
                  <button
                    ref="closeButtonRef"
                    type="button"
                    class="text-text-secondary hover:text-text-primary transition-colors p-1"
                    @click="close"
                  >
                    <span class="sr-only">关闭</span>
                    <svg
                      class="h-6 w-6"
                      xmlns="http://www.w3.org/2000/svg"
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

                <!-- Loading State -->
                <div
                  v-if="uiStore.pptContentLoading || imageLoading"
                  class="flex-1 flex items-center justify-center bg-gray-50"
                >
                  <div class="text-center">
                    <svg
                      class="animate-spin h-12 w-12 text-accent mx-auto mb-4"
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
                      <path
                        class="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    <p class="text-text-secondary">加载PPT内容中...</p>
                  </div>
                </div>

                <!-- Error State -->
                <div
                  v-else-if="uiStore.pptContentError || imageError"
                  class="flex-1 flex items-center justify-center bg-gray-50"
                >
                  <div class="text-center px-6">
                    <svg
                      class="h-12 w-12 text-error mx-auto mb-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                      />
                    </svg>
                    <h3 class="text-lg font-semibold text-text-primary mb-2">内容加载失败</h3>
                    <p class="text-sm text-text-secondary mb-4">
                      {{ uiStore.pptContentError || imageError }}
                    </p>
                    <Button variant="secondary" @click="loadSlides">重新加载</Button>
                  </div>
                </div>

                <!-- Slide Image Display -->
                <div
                  v-else
                  class="flex-1 px-8 py-8 bg-gray-50 flex items-center justify-center"
                  role="region"
                  aria-label="PPT预览"
                  aria-live="polite"
                >
                  <!-- Fixed-height slide container -->
                  <div class="slide-container">
                    <!-- Image loading indicator -->
                    <div
                      v-if="!currentImageLoaded"
                      class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 z-10"
                    >
                      <svg
                        class="animate-spin h-8 w-8 text-accent"
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
                        <path
                          class="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                    </div>

                    <!-- Slide image -->
                    <img
                      :src="currentSlideUrl"
                      :alt="`幻灯片 ${currentSlideIndex + 1}`"
                      class="slide-image"
                      :class="{ 'opacity-0': !currentImageLoaded }"
                      role="img"
                      :aria-label="`第${currentSlideIndex + 1}页，共${totalSlides}页`"
                      @load="handleImageLoad"
                      @error="handleImageError"
                    />

                    <!-- Watermark Overlay -->
                    <Watermark
                      v-if="watermarkConfig.enabled"
                      :text="watermarkConfig.text"
                      :opacity="watermarkConfig.opacity"
                      :font-size="watermarkConfig.fontSize"
                      :color="watermarkConfig.color"
                    />
                  </div>
                </div>

                <!-- Navigation Footer -->
                <div
                  v-if="!uiStore.pptContentLoading && !imageLoading && !uiStore.pptContentError && !imageError"
                  class="flex items-center justify-between px-6 py-4 border-t border-border-color bg-white rounded-b-xl"
                >
                  <Button
                    variant="secondary"
                    size="small"
                    :disabled="!canGoPrev"
                    @click="prevSlide"
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
                        d="M15 19l-7-7 7-7"
                      />
                    </svg>
                    上一页
                  </Button>

                  <span class="text-sm text-text-secondary font-medium">
                    第 {{ currentSlideIndex + 1 }} / {{ totalSlides }} 张
                  </span>

                  <Button
                    variant="secondary"
                    size="small"
                    :disabled="!canGoNext"
                    @click="nextSlide"
                  >
                    下一页
                    <svg
                      class="h-4 w-4 ml-1"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </Button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<style scoped>
/* Fixed-height slide container for consistent presentation */
.slide-container {
  @apply w-full max-w-5xl bg-white shadow-2xl rounded-xl relative;
  height: 600px;
  max-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Slide image - fit within container while maintaining aspect ratio */
.slide-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: opacity 0.3s ease-in-out;
}

.slide-image.opacity-0 {
  opacity: 0;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .slide-container {
    height: 400px;
    max-height: 50vh;
  }
}
</style>
