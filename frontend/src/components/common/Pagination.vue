<script setup>
import { computed } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['page-change'])

const pages = computed(() => {
  const maxVisible = 7
  const pages = []

  if (props.totalPages <= maxVisible) {
    // Show all pages
    for (let i = 1; i <= props.totalPages; i++) {
      pages.push(i)
    }
  } else {
    // Show with ellipsis
    const leftSiblingIndex = Math.max(props.currentPage - 1, 1)
    const rightSiblingIndex = Math.min(props.currentPage + 1, props.totalPages)

    const shouldShowLeftDots = leftSiblingIndex > 2
    const shouldShowRightDots = rightSiblingIndex < props.totalPages - 1

    // Always show first page
    pages.push(1)

    if (shouldShowLeftDots) {
      pages.push('...')
    }

    // Show pages around current
    for (let i = leftSiblingIndex; i <= rightSiblingIndex; i++) {
      if (i !== 1 && i !== props.totalPages) {
        pages.push(i)
      }
    }

    if (shouldShowRightDots) {
      pages.push('...')
    }

    // Always show last page
    if (props.totalPages > 1) {
      pages.push(props.totalPages)
    }
  }

  return pages
})

const goToPage = (page) => {
  if (typeof page === 'number' && page !== props.currentPage) {
    emit('page-change', page)
  }
}

const goToPrevious = () => {
  if (props.currentPage > 1) {
    emit('page-change', props.currentPage - 1)
  }
}

const goToNext = () => {
  if (props.currentPage < props.totalPages) {
    emit('page-change', props.currentPage + 1)
  }
}

const handleKeydown = (e) => {
  switch (e.key) {
    case 'ArrowLeft':
      e.preventDefault()
      goToPrevious()
      break
    case 'ArrowRight':
      e.preventDefault()
      goToNext()
      break
    case 'Home':
      e.preventDefault()
      goToPage(1)
      break
    case 'End':
      e.preventDefault()
      goToPage(props.totalPages)
      break
  }
}
</script>

<template>
  <nav
    v-if="totalPages > 1"
    class="flex items-center justify-center gap-2"
    aria-label="Pagination"
    tabindex="0"
    @keydown="handleKeydown"
  >
    <!-- Previous button -->
    <Button
      variant="secondary"
      size="small"
      :disabled="currentPage === 1"
      @click="goToPrevious"
    >
      <svg
        class="h-5 w-5"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      <span class="sr-only">上一页</span>
    </Button>

    <!-- Page numbers -->
    <div class="flex items-center gap-1">
      <template v-for="(page, index) in pages" :key="index">
        <span
          v-if="page === '...'"
          class="px-3 py-2 text-text-secondary"
        >
          ...
        </span>
        <button
          v-else
          :class="[
            'px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200',
            page === currentPage
              ? 'bg-accent text-white'
              : 'text-text-primary hover:bg-secondary-bg'
          ]"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>
    </div>

    <!-- Next button -->
    <Button
      variant="secondary"
      size="small"
      :disabled="currentPage === totalPages"
      @click="goToNext"
    >
      <svg
        class="h-5 w-5"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
      </svg>
      <span class="sr-only">下一页</span>
    </Button>
  </nav>
</template>
