# Feature #004: PPT内容预览功能 - 技术设计

## 架构设计

### 1. 数据流图

```
用户点击"预览"
  ↓
TaskItem.vue 触发 uiStore.openPPTPreview(taskId)
  ↓
uiStore 调用 getPPTContent(taskId)
  ↓
[Mock模式] → pptContentData.js 返回Markdown内容
[Real API] → GET /api/ppt_content?taskId={uuid}
  ↓
uiStore.currentPPTContent 更新
  ↓
PPTPreviewModal.vue 监听状态变化
  ↓
parseSlides(markdown) 分割为数组 ["slide1", "slide2", ...]
  ↓
renderSlide(slideMarkdown) 使用 marked + DOMPurify
  ↓
用户浏览幻灯片（翻页/关闭）
```

---

## 2. 组件架构

### 2.1 新增组件

#### `PPTPreviewModal.vue`
**职责**: 幻灯片预览容器
**Props**: 无（从uiStore读取状态）
**State**:
```javascript
{
  currentSlideIndex: 0,          // 当前页码（0-based）
  renderedSlides: [],            // 渲染后的HTML数组
  isLoading: false,              // 渲染中状态
  renderError: null              // 渲染错误
}
```

**关键方法**:
```javascript
// 翻页
nextSlide()
prevSlide()
goToSlide(index)

// 键盘导航
handleKeydown(event) {
  if (event.key === 'ArrowRight') nextSlide()
  if (event.key === 'ArrowLeft') prevSlide()
  if (event.key === 'Escape') uiStore.closePPTPreview()
}

// 渲染
async renderAllSlides() {
  const slides = parseSlides(uiStore.currentPPTContent.markdown)
  renderedSlides.value = slides.map(slide => renderSlide(slide))
}
```

**布局结构**:
```vue
<Modal :open="uiStore.pptPreviewOpen" size="6xl">
  <div class="ppt-preview-container h-[80vh] flex flex-col">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b">
      <h3>{{ paperTitle }}</h3>
      <button @click="close">×</button>
    </div>

    <!-- Slide Content Area -->
    <div class="flex-1 overflow-y-auto p-8 bg-gray-50">
      <div class="max-w-4xl mx-auto bg-white shadow-lg rounded-lg p-12">
        <div v-html="renderedSlides[currentSlideIndex]"></div>
      </div>
    </div>

    <!-- Navigation Footer -->
    <div class="flex items-center justify-between p-4 border-t bg-white">
      <Button @click="prevSlide" :disabled="currentSlideIndex === 0">
        ← 上一页
      </Button>
      <span class="text-sm text-gray-600">
        {{ currentSlideIndex + 1 }} / {{ renderedSlides.length }}
      </span>
      <Button @click="nextSlide" :disabled="currentSlideIndex === renderedSlides.length - 1">
        下一页 →
      </Button>
    </div>
  </div>
</Modal>
```

---

### 2.2 修改现有组件

#### `TaskItem.vue` (修改)
**新增**: "预览"按钮（仅completed状态显示）

```vue
<!-- Completed状态区域 -->
<div v-else-if="task.status === 'completed'" class="space-y-3">
  <!-- ... 现有内容 ... -->

  <!-- Action Buttons -->
  <div class="flex gap-2">
    <!-- 新增：预览按钮 -->
    <Button
      variant="secondary"
      size="small"
      @click="handlePreview"
    >
      <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      </svg>
      预览
    </Button>

    <!-- 现有：下载按钮 -->
    <a v-if="task.downloadUrl" ... >
      下载PPT
    </a>
  </div>
</div>
```

**新增方法**:
```javascript
const handlePreview = () => {
  uiStore.openPPTPreview(props.task.id)
}
```

---

## 3. 状态管理（Pinia Store）

### 3.1 `ui.js` Store扩展

**新增State**:
```javascript
const pptPreviewOpen = ref(false)
const currentPPTContent = ref(null) // { taskId, markdown, metadata }
const pptContentLoading = ref(false)
const pptContentError = ref(null)
```

**新增Actions**:
```javascript
const openPPTPreview = async (taskId) => {
  pptPreviewOpen.value = true
  pptContentLoading.value = true
  pptContentError.value = null

  try {
    const content = await getPPTContent(taskId)
    currentPPTContent.value = content
  } catch (error) {
    pptContentError.value = error.message
    showToast('加载PPT内容失败', 'error')
  } finally {
    pptContentLoading.value = false
  }
}

const closePPTPreview = () => {
  pptPreviewOpen.value = false
  currentPPTContent.value = null
  pptContentError.value = null
}
```

---

## 4. API服务层

### 4.1 新增文件: `api/pptContentService.js`

```javascript
import apiClient from './index'
import { USE_MOCK_DATA } from '@/config'
import { getMockPPTContent } from '@/mocks/pptContentData'

/**
 * 获取PPT内容（Markdown格式）
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>} PPTContent对象
 */
export async function getPPTContent(taskId) {
  if (USE_MOCK_DATA) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500))
    return getMockPPTContent(taskId)
  }

  const response = await apiClient.get('/ppt_content', {
    params: { taskId }
  })
  return response.data
}
```

---

## 5. Mock数据层

### 5.1 新增文件: `mocks/pptContentData.js`

```javascript
/**
 * Mock PPT Content Data
 * Markdown格式的PPT内容，用于预览功能
 */

/**
 * PPT内容数据库（taskId → content映射）
 */
export const mockPPTContents = {
  // Task 1: Hierarchical Reasoning Models（包含数学公式和代码）
  'mock-task-001': {
    taskId: 'mock-task-001',
    markdown: `# Hierarchical Reasoning Models
小规模递归推理超越大语言模型

---

## 研究背景

### 当前挑战
- 大语言模型（LLM）在复杂推理任务上表现受限
- 计算成本高昂，难以实时部署
- 黑盒特性导致推理过程不可解释

### 研究动机
寻找**更高效、更透明**的推理范式

---

## 核心创新

### 🎯 层次化递归推理框架
1. **分解**: 将复杂问题拆解为子问题
2. **递归**: 自底向上逐层求解
3. **聚合**: 合成最终答案

### 📊 关键指标
- 计算成本降低 **70%**
- 推理准确率提升 **15%**
- 响应速度提高 **3x**

---

## 数学原理

### 递归复杂度分析

设问题规模为 $n$，分解为 $k$ 个子问题，则：

$$T(n) = k \\cdot T(\\frac{n}{k}) + O(n)$$

当 $k=2$ 时，时间复杂度为：

$$T(n) = O(n \\log n)$$

相比传统方法的 $O(n^2)$，效率提升显著。

---

## 算法实现

### 伪代码

\`\`\`python
def hierarchical_reasoning(problem, depth=0):
    # Base case: 简单问题直接求解
    if is_simple(problem):
        return solve_directly(problem)

    # Decompose: 分解为子问题
    subproblems = decompose(problem)

    # Recursive: 递归求解子问题
    results = [
        hierarchical_reasoning(sub, depth+1)
        for sub in subproblems
    ]

    # Aggregate: 聚合子问题结果
    return aggregate(results)
\`\`\`

---

## 技术架构

### 三层推理模型
\`\`\`
输入层 → [问题分解]
  ↓
中间层 → [子问题求解] ×N
  ↓
输出层 → [答案聚合]
\`\`\`

### 优势对比
| 方法 | 准确率 | 成本 | 可解释性 |
|------|--------|------|---------|
| GPT-4 | 85% | 高 | 低 |
| 本方法 | 88% | **低** | **高** |

---

## 应用场景

### 🏥 医疗诊断
- 多症状综合分析
- 病因推理链路透明

### 📚 教育辅导
- 数学证明步骤拆解
- 个性化学习路径

### 🔬 科研辅助
- 实验假设验证
- 文献逻辑梳理

---

## 实验结果

### 基准测试（5个数据集）
- **ARC Challenge**: 88.2% (+12% vs baseline)
- **GSM8K**: 91.5% (+8%)
- **LogicQA**: 79.3% (+15%)

### 消融实验
- 移除递归机制 → 准确率下降18%
- 减少层数 → 成本降低但准确率下降10%

---

## 未来工作

### 短期目标
1. 扩展到多模态输入（图文混合推理）
2. 优化层次结构自动学习算法

### 长期愿景
构建**可解释、高效、普适**的推理范式
推动AI从"黑盒"走向"白盒"

---

## 致谢

感谢论导Lite提供的一键生成功能！
本PPT由AI自动生成 🎉`,
    metadata: {
      paperTitle: 'Hierarchical Reasoning Models: Small-Scale Recursive Reasoning Outperforms LLMs',
      slideCount: 10,
      generatedAt: '2025-01-14T10:03:15.000Z',
      author: 'Chen et al.',
      field: '机器学习'
    }
  },

  // Task 2: OpenTSLM
  'mock-task-002': {
    taskId: 'mock-task-002',
    markdown: `# OpenTSLM
开放时间序列语言模型

---

## 核心创新

### 🎯 统一跨领域预测框架
- 单一模型处理多种时间序列任务
- 零样本迁移能力（Zero-shot Transfer）
- 端到端训练，无需人工特征工程

---

## 技术亮点

### 架构设计
- **Transformer编码器** + 时间序列专用嵌入
- **多尺度注意力机制**
- **动态上下文窗口**（自适应历史长度）

### 性能指标
- 8个基准数据集中**7个SOTA**
- 平均MAE降低**22%**
- 推理速度提升**5倍**

---

## 应用前景

### 📈 金融市场预测
- 股票价格趋势
- 加密货币波动预警

### 🌤️ 天气预报
- 多变量联合预测（温度、湿度、风速）
- 极端天气预警

### 🏭 工业物联网
- 设备故障预测（提前7天预警）
- 能源消耗优化

---

## 总结

OpenTSLM标志着时间序列预测进入**预训练大模型时代**
开放权重助力研究社区快速迭代 🚀`,
    metadata: {
      paperTitle: 'OpenTSLM: Open Time Series Language Model for Unified Cross-Domain Forecasting',
      slideCount: 4,
      generatedAt: '2025-01-14T14:33:10.000Z',
      author: 'Wang et al.',
      field: '时间序列分析'
    }
  },

  // Task 3: Failed task（暂无内容，用于测试错误处理）
  'mock-task-003': null  // Failed task不应该有预览内容
}

/**
 * 获取Mock PPT内容
 * @param {string} taskId - 任务ID
 * @returns {Object} PPTContent对象
 * @throws {Error} 如果taskId不存在或任务失败
 */
export function getMockPPTContent(taskId) {
  const content = mockPPTContents[taskId]

  if (content === null) {
    throw new Error('该任务未成功生成PPT，无法预览')
  }

  if (content === undefined) {
    throw new Error('未找到PPT内容')
  }

  return content
}

/**
 * 检查任务是否有预览内容
 * @param {string} taskId - 任务ID
 * @returns {boolean}
 */
export function hasPPTContent(taskId) {
  return mockPPTContents[taskId] !== undefined &&
         mockPPTContents[taskId] !== null
}
```

---

## 6. 工具函数层

### 6.1 新增文件: `utils/pptRenderer.js`

```javascript
import { marked } from 'marked'
import markedKatex from 'marked-katex-extension'
import hljs from 'highlight.js/lib/core'
import DOMPurify from 'dompurify'

// 按需导入常用语言（避免全量导入）
import javascript from 'highlight.js/lib/languages/javascript'
import python from 'highlight.js/lib/languages/python'
import java from 'highlight.js/lib/languages/java'
import cpp from 'highlight.js/lib/languages/cpp'
import sql from 'highlight.js/lib/languages/sql'
import bash from 'highlight.js/lib/languages/bash'
import json from 'highlight.js/lib/languages/json'

// 注册语言
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('python', python)
hljs.registerLanguage('java', java)
hljs.registerLanguage('cpp', cpp)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('json', json)

/**
 * 配置marked扩展
 */
// 1. KaTeX数学公式支持
marked.use(markedKatex({
  throwOnError: false,     // 公式错误时不中断渲染
  output: 'html',          // 输出HTML格式
  displayMode: false,      // 行内公式模式
  strict: false            // 宽松解析
}))

// 2. 代码高亮支持
marked.setOptions({
  gfm: true,               // GitHub Flavored Markdown
  breaks: true,            // 换行符转<br>
  headerIds: false,        // 禁用标题ID（幻灯片不需要锚点）
  highlight: (code, lang) => {
    // 如果指定了语言且支持，则高亮
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.warn('Highlight.js error:', err)
      }
    }
    // 否则返回原始代码（自动转义）
    return code
  }
})

/**
 * 将Markdown拆分为幻灯片数组
 * @param {string} markdown - 完整的Markdown文本
 * @returns {string[]} 幻灯片数组
 */
export function parseSlides(markdown) {
  if (!markdown || typeof markdown !== 'string') {
    return []
  }

  return markdown
    .split(/^---$/m)  // 使用 --- 作为分隔符（独立行）
    .map(slide => slide.trim())
    .filter(slide => slide.length > 0)
}

/**
 * 渲染单个幻灯片的Markdown为HTML
 * @param {string} slideMarkdown - 单页幻灯片的Markdown
 * @returns {string} 清理后的HTML
 */
export function renderSlide(slideMarkdown) {
  if (!slideMarkdown || typeof slideMarkdown !== 'string') {
    return '<p class="text-gray-400">空白页</p>'
  }

  try {
    // Step 1: Markdown → HTML (包含KaTeX和代码高亮)
    const rawHtml = marked.parse(slideMarkdown)

    // Step 2: 安全清理（防止XSS）
    const sanitizedHtml = DOMPurify.sanitize(rawHtml, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre', 'span',
        'ul', 'ol', 'li',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'blockquote', 'a', 'img',
        // KaTeX需要的标签
        'annotation', 'math', 'mrow', 'mi', 'mo', 'mn', 'mtext', 'mspace',
        'semantics', 'mstyle', 'msup', 'msub', 'mfrac', 'mover', 'munder'
      ],
      ALLOWED_ATTR: [
        'href', 'src', 'alt', 'title', 'class', 'style',
        // KaTeX需要的属性
        'xmlns', 'encoding', 'data-*'
      ],
      // 允许KaTeX的style属性
      ALLOWED_STYLES: {
        '*': {
          'color': [/^#[0-9a-f]{3,6}$/i],
          'font-size': [/^\d+(?:\.\d+)?(?:px|em|rem|%)$/],
          'margin': [/^\d+(?:\.\d+)?(?:px|em|rem)$/],
          'padding': [/^\d+(?:\.\d+)?(?:px|em|rem)$/]
        }
      }
    })

    return sanitizedHtml
  } catch (error) {
    console.error('Slide rendering error:', error)
    return `<p class="text-red-500">渲染错误: ${error.message}</p>`
  }
}

/**
 * 渲染所有幻灯片
 * @param {string} markdown - 完整的Markdown文本
 * @returns {string[]} 渲染后的HTML数组
 */
export function renderAllSlides(markdown) {
  const slides = parseSlides(markdown)
  return slides.map(slide => renderSlide(slide))
}
```

---

## 7. 水印功能设计

### 7.1 水印需求分析

**目的**:
1. **品牌保护**: 标识内容来自论导Lite平台
2. **防盗用**: 防止未授权传播PPT预览截图
3. **用户引导**: 提示用户下载完整版PPT

**设计原则**:
- 半透明（不干扰内容阅读）
- 多位置分布（防止裁剪）
- 自适应幻灯片尺寸
- 无法通过简单CSS隐藏

### 7.2 水印技术方案

#### 方案选择

| 方案 | 实现方式 | 优点 | 缺点 | 选择 |
|------|---------|------|------|------|
| A. CSS伪元素 | `::before/::after` | 简单 | 易被禁用CSS移除 | ❌ |
| B. Canvas绘制 | 动态生成图片 | 难以移除 | 性能开销大 | ❌ |
| C. DOM叠加层 | 绝对定位div | 平衡性能和安全 | 可被DOM操作移除 | ✅ |
| D. SVG背景 | `background-image` | 矢量清晰 | 易被CSS覆盖 | ❌ |

**选择方案C**: DOM叠加层 + 多重保护机制

#### 实现细节

**水印组件**: `components/common/Watermark.vue`

```vue
<template>
  <div
    class="watermark-container"
    :style="containerStyle"
  >
    <!-- 多个水印文字，分布在不同位置 -->
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

<script setup>
import { computed } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: '论导Lite 预览版 - lundao.com'
  },
  opacity: {
    type: Number,
    default: 0.08  // 极低透明度，不干扰阅读
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

// 水印文字
const watermarkText = computed(() => props.text)

// 水印位置（9宫格分布 + 中心旋转）
const watermarkPositions = [
  { top: '10%', left: '10%', rotate: -30 },
  { top: '10%', left: '50%', rotate: -30 },
  { top: '10%', right: '10%', rotate: -30 },
  { top: '50%', left: '10%', rotate: -30 },
  { top: '50%', left: '50%', rotate: -30 },  // 中心
  { top: '50%', right: '10%', rotate: -30 },
  { bottom: '10%', left: '10%', rotate: -30 },
  { bottom: '10%', left: '50%', rotate: -30 },
  { bottom: '10%', right: '10%', rotate: -30 }
]

// 容器样式
const containerStyle = computed(() => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  pointerEvents: 'none',  // 不阻止用户交互
  zIndex: 1,              // 在内容之上
  userSelect: 'none'      // 不可选中
}))

// 单个水印样式
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

<style scoped>
.watermark-container {
  /* 防止被覆盖 */
  isolation: isolate;
}

.watermark-text {
  /* 防止文字选中和拖拽 */
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-user-drag: none;
}
</style>
```

#### 集成到PPTPreviewModal

```vue
<!-- PPTPreviewModal.vue -->
<template>
  <Modal :open="uiStore.pptPreviewOpen" size="6xl">
    <div class="ppt-preview-container h-[80vh] flex flex-col">
      <!-- ... Header ... -->

      <!-- Slide Content Area with Watermark -->
      <div class="flex-1 overflow-y-auto p-8 bg-gray-50 relative">
        <div class="max-w-4xl mx-auto bg-white shadow-lg rounded-lg p-12 relative">
          <!-- 幻灯片内容 -->
          <div class="slide-content" v-html="renderedSlides[currentSlideIndex]"></div>

          <!-- 水印叠加层 -->
          <Watermark
            text="论导Lite 预览版 - lundao.com"
            :opacity="0.08"
            :fontSize="16"
          />
        </div>
      </div>

      <!-- ... Footer ... -->
    </div>
  </Modal>
</template>

<script setup>
import Watermark from '@/components/common/Watermark.vue'
// ... other imports
</script>
```

### 7.3 水印配置管理

**环境变量控制**:

```bash
# .env.development
VITE_WATERMARK_TEXT="论导Lite 预览版 - lundao.com"
VITE_WATERMARK_OPACITY=0.08
VITE_WATERMARK_ENABLED=true

# .env.production
VITE_WATERMARK_TEXT="论导Lite - lundao.com"
VITE_WATERMARK_OPACITY=0.1
VITE_WATERMARK_ENABLED=true
```

**配置文件**: `src/config/watermark.js`

```javascript
export const watermarkConfig = {
  enabled: import.meta.env.VITE_WATERMARK_ENABLED !== 'false',
  text: import.meta.env.VITE_WATERMARK_TEXT || '论导Lite 预览版',
  opacity: parseFloat(import.meta.env.VITE_WATERMARK_OPACITY) || 0.08,
  fontSize: 16,
  color: '#000000',
  // 可选：根据任务状态调整水印文字
  getTextByTask: (task) => {
    const baseText = import.meta.env.VITE_WATERMARK_TEXT || '论导Lite'
    return `${baseText} - ${task.paperTitle}`
  }
}
```

### 7.4 水印安全增强（可选，Phase 2）

**MutationObserver防篡改**:

```javascript
// utils/watermarkProtection.js
export function protectWatermark(watermarkElement) {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      // 检测水印是否被删除或隐藏
      if (!document.contains(watermarkElement) ||
          watermarkElement.style.display === 'none' ||
          watermarkElement.style.opacity === '0') {
        console.warn('Watermark tampering detected')
        // 重新添加水印或记录日志
      }
    })
  })

  observer.observe(watermarkElement.parentNode, {
    childList: true,
    attributes: true,
    subtree: true
  })

  return observer
}
```

---

## 8. 样式设计

### 8.1 幻灯片容器样式（包含代码高亮和数学公式）

**CSS文件导入** (在PPTPreviewModal.vue中):

```vue
<script setup>
// 导入依赖样式
import 'highlight.js/styles/github-dark.css'  // 代码高亮主题
import 'katex/dist/katex.min.css'             // KaTeX数学公式
</script>
```

**组件样式**:

```vue
<style scoped>
/* 幻灯片内容区域样式 */
.slide-content {
  @apply prose prose-lg max-w-none;

  /* 标题样式 */
  :deep(h1) {
    @apply text-3xl font-bold text-text-primary mb-6 pb-3 border-b-2 border-accent;
  }

  :deep(h2) {
    @apply text-2xl font-semibold text-text-primary mt-8 mb-4;
  }

  :deep(h3) {
    @apply text-xl font-medium text-text-secondary mt-6 mb-3;
  }

  /* 段落样式 */
  :deep(p) {
    @apply text-base text-text-primary leading-relaxed mb-4;
  }

  /* 列表样式 */
  :deep(ul) {
    @apply list-disc list-inside space-y-2 mb-4;
  }

  :deep(ol) {
    @apply list-decimal list-inside space-y-2 mb-4;
  }

  /* 行内代码样式 */
  :deep(code) {
    @apply bg-gray-100 text-accent px-2 py-1 rounded text-sm font-mono;
  }

  /* 代码块样式（highlight.js增强） */
  :deep(pre) {
    @apply bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto mb-4;
  }

  :deep(pre code) {
    @apply bg-transparent text-inherit p-0;
  }

  /* 表格样式 */
  :deep(table) {
    @apply w-full border-collapse mb-4;
  }

  :deep(th) {
    @apply bg-accent text-white px-4 py-2 text-left font-semibold;
  }

  :deep(td) {
    @apply border border-border-color px-4 py-2;
  }

  /* 引用块样式 */
  :deep(blockquote) {
    @apply border-l-4 border-accent bg-blue-50 pl-4 py-2 italic text-text-secondary mb-4;
  }

  /* KaTeX数学公式样式 */
  :deep(.katex) {
    @apply text-text-primary;
    font-size: 1.1em;
  }

  :deep(.katex-display) {
    @apply my-4;
  }

  /* 数学公式块样式（居中） */
  :deep(.katex-display > .katex) {
    @apply text-center;
  }
}

/* 水印容器样式 */
.watermark-overlay {
  pointer-events: none;
  user-select: none;
  z-index: 10;
}
</style>
```

### 8.2 响应式适配

```vue
<style scoped>
/* 移动端适配 */
@media (max-width: 768px) {
  .slide-content :deep(h1) {
    @apply text-2xl;
  }

  .slide-content :deep(pre) {
    @apply text-xs;
  }

  .slide-content :deep(.katex) {
    font-size: 0.9em;
  }
}
</style>
```

---

## 8. 性能优化策略

### 8.1 延迟加载（Lazy Loading）
```javascript
// PPTPreviewModal.vue 使用动态导入
const { renderAllSlides } = await import('@/utils/pptRenderer.js')
```

### 8.2 渲染缓存
```javascript
// Store中缓存已渲染的内容
const renderedCache = new Map() // taskId → renderedSlides

const openPPTPreview = async (taskId) => {
  // 检查缓存
  if (renderedCache.has(taskId)) {
    currentPPTContent.value = renderedCache.get(taskId)
    return
  }

  // 获取并缓存
  const content = await getPPTContent(taskId)
  renderedCache.set(taskId, content)
  currentPPTContent.value = content
}
```

### 8.3 虚拟滚动（可选，Phase 2）
如果单个幻灯片内容过长，可使用虚拟滚动优化渲染性能

---

## 9. 安全性考虑

### 9.1 XSS防护
- **必须使用** DOMPurify清理所有HTML
- 白名单策略：只允许安全标签（见pptRenderer.js配置）
- 禁止 `<script>`, `<iframe>`, `<object>` 等危险标签

### 9.2 输入验证
```javascript
// getPPTContent前置检查
if (!taskId || typeof taskId !== 'string') {
  throw new Error('Invalid taskId')
}

if (taskId.length > 100) {
  throw new Error('TaskId too long')
}
```

---

## 10. 可访问性（A11y）

### 10.1 键盘导航
```javascript
// 全局监听键盘事件
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const handleKeydown = (e) => {
  if (!uiStore.pptPreviewOpen) return

  switch(e.key) {
    case 'ArrowLeft':
      prevSlide()
      break
    case 'ArrowRight':
      nextSlide()
      break
    case 'Escape':
      uiStore.closePPTPreview()
      break
    case 'Home':
      currentSlideIndex.value = 0
      break
    case 'End':
      currentSlideIndex.value = renderedSlides.value.length - 1
      break
  }
}
```

### 10.2 ARIA属性
```vue
<div
  role="region"
  aria-label="PPT预览"
  aria-live="polite"
>
  <div role="article" :aria-label="`第${currentSlideIndex + 1}页，共${totalSlides}页`">
    <!-- Slide content -->
  </div>
</div>
```

### 10.3 焦点管理
```javascript
// Modal打开时自动聚焦到关闭按钮
const closeButtonRef = ref(null)

watch(() => uiStore.pptPreviewOpen, (isOpen) => {
  if (isOpen) {
    nextTick(() => {
      closeButtonRef.value?.focus()
    })
  }
})
```

---

## 11. 错误处理

### 11.1 错误场景矩阵
| 场景 | 错误类型 | 用户反馈 | 降级方案 |
|------|---------|---------|---------|
| 网络超时 | TimeoutError | Toast: "加载超时，请重试" | 显示重试按钮 |
| 任务不存在 | NotFoundError | Toast: "未找到PPT内容" | 关闭Modal |
| Markdown语法错误 | ParseError | 显示原始文本 | 降级为纯文本展示 |
| 渲染崩溃 | RenderError | 显示错误提示 | 显示"渲染失败"占位符 |

### 11.2 错误边界实现
```vue
<template>
  <div v-if="renderError" class="text-center py-12">
    <svg class="h-12 w-12 text-error mx-auto mb-4">...</svg>
    <h3 class="text-lg font-semibold text-text-primary mb-2">内容渲染失败</h3>
    <p class="text-sm text-text-secondary mb-4">{{ renderError }}</p>
    <Button @click="retryRender">重新加载</Button>
  </div>
</template>
```

---

## 12. API契约定义

### 12.1 后端接口规范

**Endpoint**: `GET /api/ppt_content`

**Query Parameters**:
```typescript
{
  taskId: string  // 任务UUID
}
```

**Success Response** (200 OK):
```json
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "markdown": "# 论文标题\n---\n## 创新点\n...",
  "metadata": {
    "paperTitle": "论文完整标题",
    "slideCount": 8,
    "generatedAt": "2025-01-15T10:00:00Z",
    "author": "作者姓名",
    "field": "研究领域"
  }
}
```

**Error Responses**:
```json
// 404 Not Found
{
  "error": "TaskNotFound",
  "message": "任务不存在或已过期"
}

// 403 Forbidden
{
  "error": "TaskNotCompleted",
  "message": "该任务尚未完成，无法预览"
}

// 500 Internal Server Error
{
  "error": "ContentGenerationFailed",
  "message": "PPT内容生成失败"
}
```

---

## 总结

### 完整依赖清单

**必需依赖**:
```json
{
  "marked": "^11.0.0",                    // 32KB - Markdown解析器
  "marked-katex-extension": "^5.0.0",    // 8KB - KaTeX扩展
  "katex": "^0.16.9",                    // 340KB - 数学公式渲染（含字体）
  "highlight.js": "^11.9.0",             // 80KB - 代码高亮（按需加载7种语言）
  "dompurify": "^3.0.6"                  // 13KB - HTML清理
}
```

**CSS依赖**:
```javascript
import 'highlight.js/styles/github-dark.css'  // 5KB
import 'katex/dist/katex.min.css'             // 12KB
```

**Total Bundle Size估算**: ~490KB (未gzip) → ~160KB (gzipped)

### 优化策略

1. **按需加载语言**: Highlight.js仅加载7种常用语言（非全量220种）
2. **动态导入**: pptRenderer.js使用 `import()` 延迟加载
3. **字体子集化**: KaTeX字体可后期优化（仅包含常用数学符号）
4. **CDN备选**: 可考虑将KaTeX和Highlight.js从CDN加载（生产环境）

### 设计原则

1. **功能完整**: 支持学术论文场景的核心需求（公式、代码、表格、图表）
2. **架构一致**: 复用现有Pinia Store模式、Modal组件、Mock系统
3. **安全优先**: XSS防护（DOMPurify白名单）、输入验证、错误边界
4. **性能可控**: 延迟加载、渲染缓存、响应式优化
5. **品牌保护**: 水印系统（9宫格分布、防篡改机制）

### 核心创新点

1. **学术场景优化**: 原生支持LaTeX数学公式和代码高亮
2. **水印系统**: 多点分布 + 环境变量配置 + 防篡改保护
3. **渐进式增强**: MVP功能完整，后续可按需添加（缩略图导航、全屏演示等）

下一步：创建任务分解（tasks.md）
