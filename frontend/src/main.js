import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')

// Mock mode console warning
if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
  console.warn('%c🚧 Mock Mode Enabled 🚧', 'color: orange; font-size: 20px; font-weight: bold')
  console.warn('PPT任务和分析数据使用mock,非真实后端数据')
}
