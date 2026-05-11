<script setup>
import { onMounted, computed } from 'vue'
import { usePapersStore } from '@/stores/papers'
import Tabs from '@/components/common/Tabs.vue'
import PaperCard from './PaperCard.vue'
import Pagination from '@/components/common/Pagination.vue'

const papersStore = usePapersStore()

const tabs = [
  { key: 'daily', label: '每日热门' },
  { key: 'weekly', label: '每周热门' },
  { key: 'monthly', label: '每月热门' }
]

const selectedPeriod = computed({
  get: () => papersStore.selectedPeriod,
  set: (value) => papersStore.setPeriod(value)
})

const handlePageChange = (page) => {
  papersStore.setPage(page)
  // Scroll to top of paper grid
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const retryFetch = () => {
  papersStore.fetchPapers(papersStore.selectedPeriod, papersStore.currentPage)
}

onMounted(() => {
  // Set loading state and fetch initial papers
  papersStore.loading = true
  papersStore.fetchPapers('daily', 1)
})
</script>

<template>
  <div class="w-full">
    <!-- Section Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-text-primary mb-2">发现热门论文</h2>
      <p class="text-sm text-text-secondary">浏览arXiv上最新的热门研究论文</p>
    </div>

    <!-- Period Tabs -->
    <Tabs v-model="selectedPeriod" :tabs="tabs">
      <template #daily>
        <div class="py-4">
          <!-- Loading Skeleton -->
          <div v-if="papersStore.loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div
              v-for="i in 8"
              :key="`skeleton-${i}`"
              class="bg-secondary-bg border border-border-color rounded-sm p-4 animate-pulse"
            >
              <div class="h-4 bg-gray-300 rounded w-1/3 mb-3"></div>
              <div class="h-5 bg-gray-300 rounded w-full mb-2"></div>
              <div class="h-5 bg-gray-300 rounded w-5/6 mb-3"></div>
              <div class="h-3 bg-gray-300 rounded w-3/4 mb-4"></div>
              <div class="flex gap-1.5 mb-3">
                <div class="h-5 bg-gray-300 rounded w-16"></div>
                <div class="h-5 bg-gray-300 rounded w-20"></div>
                <div class="h-5 bg-gray-300 rounded w-14"></div>
              </div>
              <div class="h-3 bg-gray-300 rounded w-1/4"></div>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="papersStore.error" class="text-center py-12">
            <div class="bg-red-50 border-l-4 border-error px-6 py-4 rounded inline-block">
              <p class="text-error font-medium mb-2">加载失败</p>
              <p class="text-sm text-red-700 mb-4">{{ papersStore.error }}</p>
              <button
                class="px-4 py-2 bg-error text-white rounded-md hover:bg-red-600 transition-colors"
                @click="retryFetch"
              >
                重试
              </button>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="!papersStore.papers || papersStore.papers.length === 0" class="text-center py-12">
            <svg
              class="mx-auto h-24 w-24 text-text-secondary mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <p class="text-text-secondary text-lg">暂无论文</p>
            <p class="text-text-secondary text-sm mt-2">当前时间段没有找到热门论文</p>
          </div>

          <!-- Papers Grid -->
          <div v-else>
            <TransitionGroup
              name="fade"
              tag="div"
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
            >
              <PaperCard
                v-for="(paper, index) in papersStore.papers"
                :key="paper.id"
                :paper="paper"
                :style="{ transitionDelay: `${index * 50}ms` }"
              />
            </TransitionGroup>

            <!-- Pagination -->
            <div class="mt-8">
              <Pagination
                :current-page="papersStore.currentPage"
                :total-pages="papersStore.totalPages"
                @page-change="handlePageChange"
              />
            </div>
          </div>
        </div>
      </template>

      <template #weekly>
        <div class="py-4">
          <!-- Same structure as daily, but managed by tabs store state -->
          <div v-if="papersStore.loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div
              v-for="i in 8"
              :key="`skeleton-${i}`"
              class="bg-secondary-bg border border-border-color rounded-sm p-4 animate-pulse"
            >
              <div class="h-4 bg-gray-300 rounded w-1/3 mb-3"></div>
              <div class="h-5 bg-gray-300 rounded w-full mb-2"></div>
              <div class="h-5 bg-gray-300 rounded w-5/6 mb-3"></div>
              <div class="h-3 bg-gray-300 rounded w-3/4 mb-4"></div>
              <div class="flex gap-1.5 mb-3">
                <div class="h-5 bg-gray-300 rounded w-16"></div>
                <div class="h-5 bg-gray-300 rounded w-20"></div>
                <div class="h-5 bg-gray-300 rounded w-14"></div>
              </div>
              <div class="h-3 bg-gray-300 rounded w-1/4"></div>
            </div>
          </div>

          <div v-else-if="papersStore.error" class="text-center py-12">
            <div class="bg-red-50 border-l-4 border-error px-6 py-4 rounded inline-block">
              <p class="text-error font-medium mb-2">加载失败</p>
              <p class="text-sm text-red-700 mb-4">{{ papersStore.error }}</p>
              <button
                class="px-4 py-2 bg-error text-white rounded-md hover:bg-red-600 transition-colors"
                @click="retryFetch"
              >
                重试
              </button>
            </div>
          </div>

          <div v-else-if="!papersStore.papers || papersStore.papers.length === 0" class="text-center py-12">
            <svg
              class="mx-auto h-24 w-24 text-text-secondary mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <p class="text-text-secondary text-lg">暂无论文</p>
            <p class="text-text-secondary text-sm mt-2">当前时间段没有找到热门论文</p>
          </div>

          <div v-else>
            <TransitionGroup
              name="fade"
              tag="div"
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
            >
              <PaperCard
                v-for="(paper, index) in papersStore.papers"
                :key="paper.id"
                :paper="paper"
                :style="{ transitionDelay: `${index * 50}ms` }"
              />
            </TransitionGroup>

            <div class="mt-8">
              <Pagination
                :current-page="papersStore.currentPage"
                :total-pages="papersStore.totalPages"
                @page-change="handlePageChange"
              />
            </div>
          </div>
        </div>
      </template>

      <template #monthly>
        <div class="py-4">
          <div v-if="papersStore.loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div
              v-for="i in 8"
              :key="`skeleton-${i}`"
              class="bg-secondary-bg border border-border-color rounded-sm p-4 animate-pulse"
            >
              <div class="h-4 bg-gray-300 rounded w-1/3 mb-3"></div>
              <div class="h-5 bg-gray-300 rounded w-full mb-2"></div>
              <div class="h-5 bg-gray-300 rounded w-5/6 mb-3"></div>
              <div class="h-3 bg-gray-300 rounded w-3/4 mb-4"></div>
              <div class="flex gap-1.5 mb-3">
                <div class="h-5 bg-gray-300 rounded w-16"></div>
                <div class="h-5 bg-gray-300 rounded w-20"></div>
                <div class="h-5 bg-gray-300 rounded w-14"></div>
              </div>
              <div class="h-3 bg-gray-300 rounded w-1/4"></div>
            </div>
          </div>

          <div v-else-if="papersStore.error" class="text-center py-12">
            <div class="bg-red-50 border-l-4 border-error px-6 py-4 rounded inline-block">
              <p class="text-error font-medium mb-2">加载失败</p>
              <p class="text-sm text-red-700 mb-4">{{ papersStore.error }}</p>
              <button
                class="px-4 py-2 bg-error text-white rounded-md hover:bg-red-600 transition-colors"
                @click="retryFetch"
              >
                重试
              </button>
            </div>
          </div>

          <div v-else-if="!papersStore.papers || papersStore.papers.length === 0" class="text-center py-12">
            <svg
              class="mx-auto h-24 w-24 text-text-secondary mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <p class="text-text-secondary text-lg">暂无论文</p>
            <p class="text-text-secondary text-sm mt-2">当前时间段没有找到热门论文</p>
          </div>

          <div v-else>
            <TransitionGroup
              name="fade"
              tag="div"
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
            >
              <PaperCard
                v-for="(paper, index) in papersStore.papers"
                :key="paper.id"
                :paper="paper"
                :style="{ transitionDelay: `${index * 50}ms` }"
              />
            </TransitionGroup>

            <div class="mt-8">
              <Pagination
                :current-page="papersStore.currentPage"
                :total-pages="papersStore.totalPages"
                @page-change="handlePageChange"
              />
            </div>
          </div>
        </div>
      </template>
    </Tabs>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
