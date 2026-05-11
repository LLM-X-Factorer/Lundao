import { ref } from 'vue'

/**
 * Composable for managing task polling intervals
 */
export function useTaskPolling() {
  const isPolling = ref(false)
  let intervalId = null

  /**
   * Start polling interval
   * @param {Function} callback - Function to call on each interval
   * @param {number} interval - Interval in milliseconds (default: 5000)
   */
  const startPolling = (callback, interval = 5000) => {
    if (isPolling.value) {
      console.warn('Polling already active')
      return
    }

    isPolling.value = true
    intervalId = setInterval(() => {
      if (typeof callback === 'function') {
        callback()
      }
    }, interval)

    console.log(`Polling started (every ${interval}ms)`)
  }

  /**
   * Stop polling interval
   */
  const stopPolling = () => {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
      isPolling.value = false
      console.log('Polling stopped')
    }
  }

  return {
    isPolling,
    startPolling,
    stopPolling,
  }
}
