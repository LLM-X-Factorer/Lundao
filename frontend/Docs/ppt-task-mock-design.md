# PPT任务Mock系统设计方案

## 问题分析

### 当前痛点
1. **PPT生成功能**:点击"一键生成组会PPT"后直接调用真实API,无mock时会弹框报错
2. **任务历史功能**:TaskHistory组件空空如也,无法展示完整的业务流程
3. **状态轮询机制**:无法模拟queued → generating → completed的状态变化过程
4. **用户体验断裂**:Paper discovery有完善的mock,但PPT功能没有,导致前端开发体验不一致

### 核心目标
以纯前端视角,通过mock数据完整模拟PPT生成和任务管理的业务流程,包括:
- ✅ 任务创建 (返回taskId)
- ✅ 状态轮询 (queued → generating → completed)
- ✅ 进度更新 (0% → 100%)
- ✅ 下载链接生成
- ✅ 历史任务展示
- ✅ 错误状态模拟 (可选)

---

## 设计方案

### 1. 架构设计

#### 1.1 Mock数据结构

```javascript
// src/mocks/taskData.js

// 历史任务mock数据 (展示不同状态)
export const mockHistoricalTasks = [
  {
    id: 'mock-task-001',
    paperId: 'daily-0001',
    paperTitle: 'Hierarchical Reasoning Models: Small-Scale Recursive Reasoning Outperforms LLMs',
    status: 'completed',
    createdAt: '2025-01-14T10:00:00.000Z',
    completedAt: '2025-01-14T10:03:00.000Z',
    downloadUrl: '/mock/downloads/hrm-presentation.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },
  {
    id: 'mock-task-002',
    paperId: 'daily-0002',
    paperTitle: 'OpenTSLM: Time Series as Native Modality in Pretrained Language Models',
    status: 'completed',
    createdAt: '2025-01-14T14:30:00.000Z',
    completedAt: '2025-01-14T14:33:00.000Z',
    downloadUrl: '/mock/downloads/opentslm-presentation.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },
  {
    id: 'mock-task-003',
    paperId: 'weekly-0005',
    paperTitle: 'Federated Learning for Healthcare: Privacy-Preserving Disease Prediction',
    status: 'failed',
    createdAt: '2025-01-13T16:20:00.000Z',
    completedAt: null,
    downloadUrl: null,
    progress: 45,
    errorMessage: 'PPT生成超时,请重试',
    retryCount: 1
  }
]
```

#### 1.2 Mock服务模块

```javascript
// src/mocks/taskService.js

import { generateMockTaskId } from './utils'

// 用于追踪mock任务的创建时间 (模拟状态演进)
const taskCreationTimes = new Map()

/**
 * Mock: 创建PPT生成任务
 * @param {string} paperId - Paper ID
 * @param {boolean} isArxiv - 是否arXiv论文
 * @returns {Promise<{taskId: string}>}
 */
export const mockCreatePPTTask = async (paperId, isArxiv = true) => {
  // 模拟网络延迟 (500ms)
  await new Promise(resolve => setTimeout(resolve, 500))

  const taskId = generateMockTaskId()

  // 记录任务创建时间,用于模拟状态演进
  taskCreationTimes.set(taskId, {
    createdAt: Date.now(),
    paperId,
    isArxiv
  })

  console.log(`[Mock] PPT task created: ${taskId}`)

  return { taskId }
}

/**
 * Mock: 轮询任务状态
 * 模拟状态演进: queued (0-5s) → generating (5-15s) → completed (15s+)
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>} 任务状态数据
 */
export const mockPollTaskStatus = async (taskId) => {
  // 模拟网络延迟 (300ms)
  await new Promise(resolve => setTimeout(resolve, 300))

  const taskInfo = taskCreationTimes.get(taskId)

  if (!taskInfo) {
    // 任务不存在 (可能是重启后localStorage中的旧任务)
    return {
      status: 'failed',
      progress: 0,
      errorMessage: '任务不存在或已过期'
    }
  }

  const elapsedSeconds = (Date.now() - taskInfo.createdAt) / 1000

  // 状态演进逻辑
  if (elapsedSeconds < 5) {
    // 0-5秒: 排队中
    return {
      status: 'queued',
      progress: null
    }
  } else if (elapsedSeconds < 15) {
    // 5-15秒: 生成中 (进度0-90%)
    const progress = Math.min(90, Math.floor((elapsedSeconds - 5) * 9))
    return {
      status: 'generating',
      progress
    }
  } else {
    // 15秒后: 完成
    return {
      status: 'completed',
      progress: 100,
      downloadUrl: `/mock/downloads/${taskId}.pptx`
    }
  }
}

/**
 * 清理过期的任务追踪信息 (可选,防止内存泄漏)
 */
export const cleanupExpiredTasks = () => {
  const now = Date.now()
  const EXPIRY_TIME = 24 * 60 * 60 * 1000 // 24小时

  for (const [taskId, taskInfo] of taskCreationTimes.entries()) {
    if (now - taskInfo.createdAt > EXPIRY_TIME) {
      taskCreationTimes.delete(taskId)
    }
  }
}
```

#### 1.3 工具函数

```javascript
// src/mocks/utils.js

/**
 * 生成mock任务ID
 * 格式: mock-task-{timestamp}-{random}
 */
export const generateMockTaskId = () => {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 8)
  return `mock-task-${timestamp}-${random}`
}

/**
 * 模拟网络延迟
 */
export const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))
```

---

### 2. API Service层改造

#### 2.1 taskService.js 添加Mock逻辑

```javascript
// src/api/taskService.js

import apiClient from './index'
import { mockCreatePPTTask, mockPollTaskStatus } from '@/mocks/taskService'

// Mock mode flag
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

/**
 * Create PPT generation task
 */
export const createPPTTask = async (paperId, isArxiv = true) => {
  if (USE_MOCK_DATA) {
    return mockCreatePPTTask(paperId, isArxiv)
  }

  const requestBody = isArxiv ? { arxivId: paperId } : { fileId: paperId }
  const response = await apiClient.post('/generate_ppt', requestBody, {
    timeout: 30000,
  })
  return response.data
}

/**
 * Poll task status
 */
export const pollTaskStatus = async (taskId) => {
  if (USE_MOCK_DATA) {
    return mockPollTaskStatus(taskId)
  }

  const response = await apiClient.get('/task_status', {
    params: { taskId },
    timeout: 10000,
  })
  return response.data
}
```

---

### 3. Store层改造

#### 3.1 tasks.js Store 添加历史任务初始化

```javascript
// src/stores/tasks.js

import { defineStore } from 'pinia'
import { ref, computed, onUnmounted } from 'vue'
import { createPPTTask, pollTaskStatus } from '@/api/taskService'
import { useTaskHistory } from '@/composables/useTaskHistory'
import { mockHistoricalTasks } from '@/mocks/taskData'

// Mock mode flag
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export const useTasksStore = defineStore('tasks', () => {
  const { saveTasksToLocalStorage, loadTasksFromLocalStorage } = useTaskHistory()

  // State
  const tasks = ref([])
  const pollingActive = ref(false)
  let pollingInterval = null

  // Computed
  const activeTasks = computed(() =>
    tasks.value.filter(task => task.status === 'queued' || task.status === 'generating')
  )

  // Load tasks from localStorage on initialization
  const storedTasks = loadTasksFromLocalStorage()

  if (USE_MOCK_DATA && storedTasks.length === 0) {
    // First time in mock mode: load historical mock tasks
    tasks.value = [...mockHistoricalTasks]
    saveTasksToLocalStorage(tasks.value)
  } else {
    tasks.value = storedTasks
  }

  // ... rest of the store logic (createTask, updateTaskStatus, etc.)

  return {
    // ... exports
  }
})
```

---

### 4. 用户体验优化

#### 4.1 状态演进时间线

```
时间轴 (Mock模式):
─────────────────────────────────────────────────
0s        5s               15s
│         │                 │
queued    generating        completed
(无进度)  (0% → 90%)       (100% + 下载链接)

真实体验:
1. 点击"生成PPT" → Toast提示"任务已创建" → Modal关闭
2. TaskHistory出现新任务,状态"queued",无进度条
3. 5秒后状态变为"generating",进度条0% → 90% (动画)
4. 15秒后状态变为"completed",进度100%,出现"下载PPT"按钮
```

#### 4.2 Mock下载处理

由于mock模式下没有真实文件,下载链接的处理:

**选项A (推荐): Toast提示**
```javascript
// src/components/core/TaskItem.vue
const handleDownload = () => {
  if (USE_MOCK_DATA && props.task.downloadUrl?.startsWith('/mock/')) {
    uiStore.showToast('Mock模式: 实际部署后可下载真实PPT文件', 'info')
    return
  }

  // Real download logic
  window.open(props.task.downloadUrl, '_blank')
}
```

**选项B: 生成示例PPT占位符**
```javascript
// 生成一个空白的PPTX文件并触发下载 (可选,较复杂)
```

#### 4.3 错误状态模拟 (可选)

在 `mockHistoricalTasks` 中提供failed状态的任务示例 (已包含在设计中)

---

## 实现步骤

### Phase 1: Mock数据和服务 (T001-T003)

**T001: 创建mock数据文件**
- 文件: `src/mocks/taskData.js`
- 内容: `mockHistoricalTasks` (3条历史任务: 2 completed + 1 failed)
- 验证: 能正确导入并访问mock数据

**T002: 创建mock服务模块**
- 文件: `src/mocks/taskService.js`
- 实现: `mockCreatePPTTask`, `mockPollTaskStatus`, `cleanupExpiredTasks`
- 验证: 单独调用mock函数能返回正确格式数据

**T003: 创建工具函数**
- 文件: `src/mocks/utils.js`
- 实现: `generateMockTaskId`, `delay`
- 验证: taskId格式正确 (mock-task-{timestamp}-{random})

### Phase 2: API层集成 (T004-T005)

**T004: 改造 taskService.js**
- 文件: `src/api/taskService.js`
- 添加: `USE_MOCK_DATA` 判断逻辑
- 修改: `createPPTTask` 和 `pollTaskStatus` 添加mock分支
- 验证: Mock模式下调用返回mock数据,真实模式下调用API

**T005: 测试API层切换**
- 切换 `VITE_USE_MOCK_DATA=true/false`
- 验证: 环境变量能正确控制行为

### Phase 3: Store层集成 (T006-T007)

**T006: 改造 tasks.js Store**
- 文件: `src/stores/tasks.js`
- 添加: `USE_MOCK_DATA` flag
- 修改: 初始化逻辑,首次进入mock模式时加载 `mockHistoricalTasks`
- 验证: 刷新页面后TaskHistory能显示3条历史任务

**T007: 测试任务创建流程**
- 在mock模式下点击"生成PPT"
- 验证: Toast提示成功,新任务出现在TaskHistory顶部,状态为queued
- 等待15秒,验证状态演进: queued → generating → completed

### Phase 4: UI优化 (T008-T009)

**T008: 优化下载按钮行为**
- 文件: `src/components/core/TaskItem.vue`
- 添加: Mock模式下的下载提示逻辑
- 验证: 点击mock任务的"下载PPT"按钮显示提示,不报错

**T009: 添加Mock模式提示 (可选)**
- 文件: `src/components/core/TaskHistory.vue`
- 在列表顶部添加Badge: "Mock模式 - 仅用于前端开发"
- 样式: 浅灰色背景,小字号,不突兀
- 验证: 仅在 `VITE_USE_MOCK_DATA=true` 时显示

### Phase 5: 测试和文档 (T010-T011)

**T010: 端到端测试**
- [ ] Paper discovery → 点击paper → Modal打开 → 点击"生成PPT"
- [ ] Toast提示成功,Modal关闭
- [ ] TaskHistory出现新任务,状态queued
- [ ] 5秒后变为generating,进度条0-90%
- [ ] 15秒后变为completed,显示下载按钮
- [ ] 刷新页面,任务仍然存在 (localStorage持久化)
- [ ] 切换 `VITE_USE_MOCK_DATA=false`,任务创建会报错 (预期行为,后端未实现)

**T011: 更新README文档**
- 文件: `src/mocks/README.md`
- 添加: PPT任务mock系统说明
- 包含: 使用方法、状态演进时间线、注意事项

---

## 技术细节

### 时间控制策略

**为什么选择 0-5-15秒的时间线?**
1. **0-5秒 queued**: 模拟后端任务队列等待,符合真实场景
2. **5-15秒 generating**: 10秒生成时间,进度条平滑增长,用户有可感知的等待体验
3. **15秒+ completed**: 总计15秒完成,不会让用户等太久,也不会太快导致察觉不到状态变化

**可调参数 (后续优化)**:
```javascript
// src/mocks/config.js
export const MOCK_TASK_TIMING = {
  QUEUE_DURATION: 5,      // 排队时长 (秒)
  GENERATE_DURATION: 10,  // 生成时长 (秒)
  TOTAL_DURATION: 15      // 总时长 (秒)
}
```

### 内存管理

**问题**: `taskCreationTimes` Map会持续增长,可能导致内存泄漏

**解决方案**:
1. 定期清理 (24小时后删除)
2. 在store unmount时清理
3. 页面刷新后Map自动清空 (acceptable,用户不会长时间不刷新)

**实现**:
```javascript
// store onUnmounted hook
onUnmounted(() => {
  stopPolling()
  cleanupExpiredTasks()
})
```

### LocalStorage兼容性

**问题**: Mock任务ID格式 `mock-task-*` 与真实任务ID不同,会混合存储

**解决方案**: 兼容两种格式,不需要特殊处理
- localStorage存储所有任务 (mock + real)
- 切换到真实模式时,mock任务的轮询会失败 (taskCreationTimes中不存在)
- 用户可手动删除mock任务,或自动过期清理

---

## 预期效果

### 开发体验提升

**Before (现状)**:
```
1. 启动项目 → Paper discovery正常 → 点击paper → Modal打开 → 分析正常
2. 点击"生成PPT" → 🔴 API报错弹框 → 任务历史空空如也
3. 开发者无法看到完整业务流程,难以调整UI/交互
```

**After (实现后)**:
```
1. 启动项目 → Paper discovery正常 → 点击paper → Modal打开 → 分析正常
2. 点击"生成PPT" → ✅ Toast提示成功 → 任务历史出现新任务
3. 观察状态演进: queued → generating (进度条) → completed (下载按钮)
4. 历史任务展示: 2条已完成 + 1条失败 + 1条新创建 (动态)
5. 开发者能完整看到业务流程,快速迭代UI优化
```

### 用户演示价值

**Demo场景**:
```
产品演示: "现在我们点击这篇论文... (Modal打开) ...AI分析完成...
          (点击生成PPT) ...任务已创建... (切换到任务历史)
          ...您可以看到任务状态从排队到生成中... (15秒后)
          ...完成了! 可以下载PPT了"

客户反馈: "整个流程很流畅,体验很好!"
```

**Without Mock (尴尬场景)**:
```
产品演示: "现在我们点击生成PPT... (报错弹框) ...呃,这个功能还在开发中,
          后端API还没好... (客户皱眉)"

客户反馈: "这真的是可用的产品吗?"
```

---

## 风险和注意事项

### 1. Mock/Real切换提醒

**风险**: 开发者忘记切换环境变量,导致生产环境使用mock数据

**缓解**:
- 在 `.env.production` 中明确设置 `VITE_USE_MOCK_DATA=false`
- 在Console中打印mock模式警告 (仅dev环境)
- 在UI上显示"Mock模式"徽章 (可选)

```javascript
// src/main.js
if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
  console.warn('%c🚧 Mock Mode Enabled 🚧', 'color: orange; font-size: 20px; font-weight: bold')
  console.warn('PPT任务和分析数据使用mock,非真实后端数据')
}
```

### 2. LocalStorage冲突

**风险**: Mock任务ID与真实任务ID混合存储,切换模式后可能混乱

**缓解**: taskId命名区分 (`mock-task-*` vs `real-task-*`),互不干扰

### 3. 状态不一致

**风险**: 页面刷新后,`taskCreationTimes` Map清空,localStorage中的queued任务无法继续演进

**解决方案A (推荐)**: 刷新后将所有queued/generating任务标记为failed
```javascript
// tasks.js store initialization
if (USE_MOCK_DATA) {
  tasks.value = loadTasksFromLocalStorage().map(task => {
    if (task.id.startsWith('mock-task-') &&
        ['queued', 'generating'].includes(task.status)) {
      return {
        ...task,
        status: 'failed',
        errorMessage: '页面刷新导致任务中断 (Mock模式)'
      }
    }
    return task
  })
}
```

**解决方案B**: 在localStorage中也存储createdAt,恢复演进进度 (较复杂,暂不实现)

---

## 后续优化 (Optional)

### 1. 错误场景模拟

添加10%随机失败率,模拟真实网络环境:
```javascript
export const mockCreatePPTTask = async (paperId, isArxiv) => {
  // 10% chance of failure
  if (Math.random() < 0.1) {
    throw new Error('模拟网络错误: 任务创建失败')
  }
  // ...
}
```

### 2. 可配置时间线

```javascript
// .env.development
VITE_MOCK_TASK_DURATION=10  # 自定义总时长 (秒)
```

### 3. Mock PPT文件生成

使用 [PptxGenJS](https://gitbrent.github.io/PptxGenJS/) 生成真实的PPTX文件 (Base64),可真实下载

---

## 总结

这个设计方案遵循SpecKit最佳实践:
1. ✅ **问题导向**: 明确当前痛点和目标
2. ✅ **渐进式实现**: 分5个Phase,每个Phase可独立验证
3. ✅ **保持一致性**: 与现有mock系统 (paperData.js) 保持相同的架构模式
4. ✅ **用户体验优先**: 真实模拟完整业务流程,不仅是数据mock
5. ✅ **风险管理**: 提前识别潜在问题并提供解决方案
6. ✅ **可维护性**: 清晰的文件结构,易于后续维护和扩展

**预期工作量**: 3-4小时 (包含测试和文档)

**价值**:
- 前端开发体验提升 80%
- 产品演示完整度提升 100%
- 后端开发解耦,前后端并行开发效率提升 50%
