<script setup>
import { watch, onMounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'info'].includes(value)
  },
  duration: {
    type: Number,
    default: 3000
  }
})

const emit = defineEmits(['close'])

let timer = null

const startTimer = () => {
  if (timer) clearTimeout(timer)
  if (props.visible && props.duration > 0) {
    timer = setTimeout(() => {
      emit('close')
    }, props.duration)
  }
}

watch(() => props.visible, (isVisible) => {
  if (isVisible) {
    startTimer()
  } else {
    if (timer) clearTimeout(timer)
  }
})

onMounted(() => {
  if (props.visible) {
    startTimer()
  }
})

const typeConfig = {
  success: {
    icon: '✓',
    bgColor: 'bg-green-50',
    borderColor: 'border-success',
    textColor: 'text-success',
    iconBg: 'bg-success'
  },
  error: {
    icon: '✕',
    bgColor: 'bg-red-50',
    borderColor: 'border-error',
    textColor: 'text-error',
    iconBg: 'bg-error'
  },
  info: {
    icon: 'ℹ',
    bgColor: 'bg-blue-50',
    borderColor: 'border-accent',
    textColor: 'text-accent',
    iconBg: 'bg-accent'
  }
}

const config = typeConfig[props.type]
</script>

<template>
  <Transition
    enter-active-class="transform transition duration-300 ease-out"
    enter-from-class="translate-y-[-100%] opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transform transition duration-200 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-[-100%] opacity-0"
  >
    <div
      v-if="visible"
      :class="[
        'fixed top-4 left-1/2 transform -translate-x-1/2 z-50',
        'flex items-center gap-3 px-4 py-3 rounded-md shadow-lg border-l-4',
        'max-w-md w-full',
        config.bgColor,
        config.borderColor
      ]"
    >
      <!-- Icon -->
      <div
        :class="[
          'flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-white text-sm font-bold',
          config.iconBg
        ]"
      >
        {{ config.icon }}
      </div>

      <!-- Message -->
      <div :class="['flex-1 text-sm font-medium', config.textColor]">
        {{ message }}
      </div>

      <!-- Close button -->
      <button
        type="button"
        :class="['flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors']"
        @click="emit('close')"
      >
        <span class="sr-only">关闭</span>
        <svg
          class="h-5 w-5"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </Transition>
</template>
