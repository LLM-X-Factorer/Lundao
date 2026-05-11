<script setup>
import PaperDiscovery from '@/components/core/PaperDiscovery.vue'
import PaperModal from '@/components/core/PaperModal.vue'
import PPTPreviewModal from '@/components/core/PPTPreviewModal.vue'
import UploadDropzone from '@/components/core/UploadDropzone.vue'
import TaskHistory from '@/components/core/TaskHistory.vue'
import Toast from '@/components/common/Toast.vue'
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Fixed Header -->
    <header class="fixed top-0 left-0 right-0 bg-primary-bg border-b border-border-color z-40 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center gap-3">
          <svg
            class="h-8 w-8 text-accent"
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
          <h1 class="text-2xl font-bold text-text-primary">
            论导Lite - AI助你三分钟搞定组会PPT
          </h1>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 pt-20 pb-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Upload Custom Paper Section -->
        <section class="mb-12">
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-text-primary mb-2">上传自定义论文</h2>
            <p class="text-sm text-text-secondary">支持PDF格式，最大20MB</p>
          </div>
          <UploadDropzone />
        </section>

        <!-- Paper Discovery Section -->
        <section class="mb-12">
          <PaperDiscovery />
        </section>

        <!-- Task History Section -->
        <section class="mb-12">
          <TaskHistory />
        </section>
      </div>
    </main>

    <!-- Fixed Footer -->
    <footer class="fixed bottom-0 left-0 right-0 bg-primary-bg border-t border-border-color z-30">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <p class="text-center text-sm text-text-secondary">
          © 2025 论导Lite. All rights reserved.
        </p>
      </div>
    </footer>

    <!-- Paper Modal -->
    <PaperModal />

    <!-- PPT Preview Modal -->
    <PPTPreviewModal />

    <!-- Toast Notifications -->
    <Toast
      :visible="uiStore.toastVisible"
      :message="uiStore.toastMessage"
      :type="uiStore.toastType"
      @close="uiStore.hideToast"
    />
  </div>
</template>
