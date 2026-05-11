<script setup>
import { useUiStore } from '@/stores/ui'

const props = defineProps({
  paper: {
    type: Object,
    required: true
  }
})

const uiStore = useUiStore()

const handleClick = () => {
  uiStore.openModal(props.paper.id)
}

const formatAuthors = (authors) => {
  if (!authors || authors.length === 0) return 'Unknown'
  if (authors.length <= 3) return authors.join(', ')
  return `${authors.slice(0, 3).join(', ')}等${authors.length}人`
}

const displayKeywords = (keywords) => {
  if (!keywords || keywords.length === 0) return []
  return keywords.slice(0, 3)
}
</script>

<template>
  <div
    class="bg-primary-bg border border-border-color rounded-sm p-4 cursor-pointer transition-all duration-200 hover:shadow-lg hover:scale-[1.02]"
    role="button"
    tabindex="0"
    :title="paper.title"
    @click="handleClick"
    @keydown.enter="handleClick"
  >
    <!-- Field Badge -->
    <div v-if="paper.field" class="mb-2">
      <span class="inline-block px-2 py-1 text-xs font-medium bg-secondary-bg text-text-secondary rounded">
        {{ paper.field }}
      </span>
    </div>

    <!-- Title -->
    <h3 class="text-lg font-semibold text-text-primary mb-2 line-clamp-2">
      {{ paper.title }}
    </h3>

    <!-- Authors -->
    <p class="text-sm text-text-secondary mb-3 line-clamp-1">
      {{ formatAuthors(paper.authors) }}
    </p>

    <!-- Keywords -->
    <div class="flex flex-wrap gap-1.5 mb-3">
      <template v-if="displayKeywords(paper.keywords).length > 0">
        <span
          v-for="(keyword, index) in displayKeywords(paper.keywords)"
          :key="index"
          class="px-2 py-0.5 text-xs bg-blue-50 text-accent rounded-full"
        >
          {{ keyword }}
        </span>
      </template>
      <span
        v-else
        class="text-xs text-text-secondary italic"
      >
        No keywords
      </span>
    </div>

    <!-- Metadata Footer -->
    <div class="flex items-center justify-between text-xs text-text-secondary">
      <span v-if="paper.publicationDate">
        {{ new Date(paper.publicationDate).toLocaleDateString('zh-CN') }}
      </span>
      <span v-if="paper.source === 'arxiv'" class="font-medium">
        arXiv
      </span>
      <span v-else-if="paper.source === 'upload'" class="font-medium">
        已上传
      </span>
    </div>
  </div>
</template>
