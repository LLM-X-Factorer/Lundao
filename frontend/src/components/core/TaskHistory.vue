<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import TaskItem from './TaskItem.vue'

const tasksStore = useTasksStore()

// Load tasks from localStorage and start polling if needed
onMounted(() => {
  tasksStore.loadTasksFromStorage()

  // Start polling if there are active tasks
  if (tasksStore.activeTasks.length > 0) {
    tasksStore.startPolling()
  }
})

// Clean up polling on unmount
onUnmounted(() => {
  tasksStore.stopPolling()
})

const sortedTasks = computed(() => {
  // Sort by creation date, newest first
  return [...tasksStore.tasks].sort((a, b) => {
    return new Date(b.createdAt) - new Date(a.createdAt)
  })
})

const hasActiveTasks = computed(() => {
  return tasksStore.activeTasks.length > 0
})
</script>

<template>
  <div class="w-full">
    <!-- Section Header -->
    <div class="mb-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-text-primary mb-2">生成历史</h2>
          <p class="text-sm text-text-secondary">
            PPT生成任务列表
            <span v-if="hasActiveTasks" class="text-accent font-medium">
              ({{ tasksStore.activeTasks.length }}个任务进行中)
            </span>
          </p>
        </div>
      </div>
    </div>

    <!-- Task List -->
    <div v-if="sortedTasks.length > 0" class="space-y-4 max-h-[600px] overflow-y-auto pr-2">
      <TaskItem
        v-for="task in sortedTasks"
        :key="task.id"
        :task="task"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12 bg-secondary-bg rounded-lg border border-border-color">
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
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
        />
      </svg>
      <p class="text-text-secondary text-lg font-medium mb-2">暂无生成任务</p>
      <p class="text-text-secondary text-sm">
        点击任意论文卡片的"生成PPT"按钮来创建任务
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
