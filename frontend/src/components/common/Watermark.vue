<script setup>
import { computed } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: '论导Lite 预览版 - lundao.com'
  },
  opacity: {
    type: Number,
    default: 0.08 // Very low opacity to not interfere with reading
  },
  fontSize: {
    type: Number,
    default: 16
  },
  color: {
    type: String,
    default: '#000000'
  }
})

// Watermark text from props
const watermarkText = computed(() => props.text)

// 9-grid watermark positions with rotation
const watermarkPositions = [
  { top: '10%', left: '10%', rotate: -30 },
  { top: '10%', left: '50%', rotate: -30 },
  { top: '10%', right: '10%', rotate: -30 },
  { top: '50%', left: '10%', rotate: -30 },
  { top: '50%', left: '50%', rotate: -30 }, // Center
  { top: '50%', right: '10%', rotate: -30 },
  { bottom: '10%', left: '10%', rotate: -30 },
  { bottom: '10%', left: '50%', rotate: -30 },
  { bottom: '10%', right: '10%', rotate: -30 }
]

// Container style
const containerStyle = computed(() => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  pointerEvents: 'none', // Don't block user interactions
  zIndex: 1, // Above content
  userSelect: 'none' // Not selectable
}))

// Individual watermark style
const getWatermarkStyle = (position) => ({
  position: 'absolute',
  ...position,
  transform: `translate(-50%, -50%) rotate(${position.rotate}deg)`,
  fontSize: `${props.fontSize}px`,
  color: props.color,
  opacity: props.opacity,
  whiteSpace: 'nowrap',
  fontWeight: 'bold',
  letterSpacing: '2px',
  userSelect: 'none',
  pointerEvents: 'none'
})
</script>

<template>
  <div
    class="watermark-container"
    :style="containerStyle"
  >
    <!-- Multiple watermark texts distributed across 9 positions -->
    <div
      v-for="(position, index) in watermarkPositions"
      :key="index"
      class="watermark-text"
      :style="getWatermarkStyle(position)"
    >
      {{ watermarkText }}
    </div>
  </div>
</template>

<style scoped>
.watermark-container {
  /* Prevent being covered */
  isolation: isolate;
}

.watermark-text {
  /* Prevent text selection and dragging */
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-user-drag: none;
}
</style>
