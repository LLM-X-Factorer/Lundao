import axios from 'axios'

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  timeout: 60000, // 60 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging and loading state
apiClient.interceptors.request.use(
  (config) => {
    // Log request for debugging in development
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.params || config.data)
    }
    return config
  },
  (error) => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

// Response interceptor for global error handling
apiClient.interceptors.response.use(
  (response) => {
    // Log response for debugging in development
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.data)
    }
    return response
  },
  (error) => {
    console.error('[API Response Error]', error)

    // Handle specific error types
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout')
    } else if (!error.response) {
      console.error('Network error - no response from server')
    } else {
      const { status, data } = error.response
      console.error(`HTTP ${status}:`, data?.message || data?.error || 'Unknown error')
    }

    return Promise.reject(error)
  }
)

export default apiClient
