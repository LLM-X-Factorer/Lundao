/**
 * Mock System Utilities
 *
 * Helper functions for mock data generation and network simulation
 */

/**
 * Generate unique mock task ID
 * Format: mock-task-{timestamp}-{random6chars}
 *
 * @returns {string} Unique task identifier
 * @example generateMockTaskId() // "mock-task-1705300123456-a3f8e9"
 */
export const generateMockTaskId = () => {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 8)
  return `mock-task-${timestamp}-${random}`
}

/**
 * Simulate network delay for realistic API behavior
 *
 * @param {number} ms - Delay duration in milliseconds
 * @returns {Promise<void>}
 * @example await delay(500) // Wait 500ms
 */
export const delay = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms))
}
