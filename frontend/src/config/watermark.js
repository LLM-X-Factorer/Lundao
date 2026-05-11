/**
 * Watermark Configuration
 * Controls watermark appearance in PPT preview modal
 */

export const watermarkConfig = {
  // Enable/disable watermark globally
  enabled: import.meta.env.VITE_WATERMARK_ENABLED !== 'false',

  // Watermark text
  text: import.meta.env.VITE_WATERMARK_TEXT || '论导Lite 预览版',

  // Opacity (0-1, lower = more transparent)
  opacity: parseFloat(import.meta.env.VITE_WATERMARK_OPACITY) || 0.08,

  // Font size in pixels
  fontSize: 16,

  // Text color
  color: '#000000',

  /**
   * Get watermark text for specific task (optional customization)
   * @param {Object} _task - Task object (reserved for future customization)
   * @returns {string} Customized watermark text
   */
  getTextByTask: (_task) => {
    const baseText = import.meta.env.VITE_WATERMARK_TEXT || '论导Lite'
    // Can customize based on task properties if needed
    // Example: return `${baseText} - ${_task.paperTitle}`
    return baseText
  }
}
