<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) => ['queued', 'generating', 'completed', 'failed'].includes(value)
  }
})

const statusConfig = computed(() => {
  const configs = {
    queued: {
      label: '排队中',
      bgColor: 'bg-yellow-100',
      textColor: 'text-yellow-800',
      borderColor: 'border-yellow-200'
    },
    generating: {
      label: '生成中',
      bgColor: 'bg-blue-100',
      textColor: 'text-blue-800',
      borderColor: 'border-blue-200'
    },
    completed: {
      label: '已完成',
      bgColor: 'bg-green-100',
      textColor: 'text-green-800',
      borderColor: 'border-green-200'
    },
    failed: {
      label: '失败',
      bgColor: 'bg-red-100',
      textColor: 'text-red-800',
      borderColor: 'border-red-200'
    }
  }

  return configs[props.status]
})
</script>

<template>
  <span
    :class="[
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
      statusConfig.bgColor,
      statusConfig.textColor,
      statusConfig.borderColor
    ]"
  >
    {{ statusConfig.label }}
  </span>
</template>
