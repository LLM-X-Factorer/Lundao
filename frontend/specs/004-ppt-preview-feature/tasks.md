# Feature #004: PPT内容预览功能 - 任务分解

## 任务概览

**总任务数**: 20 (T001-T020)
**预计工时**: 10-14小时
**分阶段实施**: 4个Phase

**核心新增功能**:
- ✅ LaTeX数学公式支持（KaTeX）
- ✅ 代码语法高亮（Highlight.js）
- ✅ 水印系统（9宫格 + 环境配置）

---

## Phase 1: 基础设施 (Foundation)

### T001: 安装完整依赖包
**优先级**: P0 (Critical)
**预计时间**: 15分钟
**描述**: 安装Markdown渲染、代码高亮、数学公式和安全清理所需的完整依赖

**验收标准**:
- [x] `marked` 已安装 (^11.0.0)
- [x] `marked-katex-extension` 已安装 (^5.0.0)
- [x] `katex` 已安装 (^0.16.9)
- [x] `highlight.js` 已安装 (^11.9.0)
- [x] `dompurify` 已安装 (^3.0.6)
- [x] package.json中包含所有新依赖
- [x] `npm install` 无错误

**实施步骤**:
```bash
npm install marked marked-katex-extension katex highlight.js dompurify
```

**Bundle Size影响**: +160KB (gzipped)

---

### T002: 创建Mock PPT内容数据
**优先级**: P0
**预计时间**: 60分钟
**描述**: 为3个历史任务编写Markdown格式的PPT内容

**验收标准**:
- [x] 创建 `src/mocks/pptContentData.js`
- [x] `mock-task-001` 包含8页幻灯片（Hierarchical Reasoning）
- [x] `mock-task-002` 包含4页幻灯片（OpenTSLM）
- [x] `mock-task-003` 设置为null（失败任务）
- [x] 包含 `getMockPPTContent()` 和 `hasPPTContent()` 函数
- [x] Markdown内容包含标题、列表、表格、代码块

**依赖**: 无

---

### T003: 创建渲染工具函数
**优先级**: P0
**预计时间**: 45分钟
**描述**: 实现Markdown → HTML渲染和安全清理逻辑

**验收标准**:
- [x] 创建 `src/utils/pptRenderer.js`
- [x] `parseSlides()` 正确拆分幻灯片
- [x] `renderSlide()` 使用marked渲染
- [x] `renderSlide()` 使用DOMPurify清理
- [x] 处理空输入和错误情况
- [x] 单元测试通过（可选）

**依赖**: T001

**测试用例**:
```javascript
// 测试拆分功能
expect(parseSlides("A\n---\nB")).toEqual(["A", "B"])

// 测试渲染功能
expect(renderSlide("# Hello")).toContain("<h1>Hello</h1>")

// 测试安全清理
expect(renderSlide("<script>alert('XSS')</script>")).not.toContain("<script>")
```

---

### T004: 创建API服务模块
**优先级**: P0
**预计时间**: 30分钟
**描述**: 实现PPT内容获取服务，支持Mock和Real API模式

**验收标准**:
- [x] 创建 `src/api/pptContentService.js`
- [x] `getPPTContent(taskId)` 实现Mock模式分支
- [x] `getPPTContent(taskId)` 实现Real API分支
- [x] 环境变量控制 (`VITE_USE_MOCK_DATA`)
- [x] 错误处理完善（网络超时、404、500）

**依赖**: T002

---

## Phase 2: 核心组件 (Core Components)

### T005: 扩展ui.js Store
**优先级**: P0
**预计时间**: 30分钟
**描述**: 添加PPT预览相关的状态管理

**验收标准**:
- [x] 添加 `pptPreviewOpen`, `currentPPTContent`, `pptContentLoading`, `pptContentError` state
- [x] 实现 `openPPTPreview(taskId)` action
- [x] 实现 `closePPTPreview()` action
- [x] 集成 `getPPTContent()` API调用
- [x] 错误处理和Toast提示

**依赖**: T004

**代码骨架**:
```javascript
// ui.js
const pptPreviewOpen = ref(false)
const currentPPTContent = ref(null)
const pptContentLoading = ref(false)
const pptContentError = ref(null)

const openPPTPreview = async (taskId) => {
  pptPreviewOpen.value = true
  pptContentLoading.value = true
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
```

---

### T006: 创建PPTPreviewModal组件（基础结构）
**优先级**: P0
**预计时间**: 90分钟
**描述**: 实现预览Modal的基础布局和渲染逻辑

**验收标准**:
- [x] 创建 `src/components/core/PPTPreviewModal.vue`
- [x] 使用Modal.vue作为容器
- [x] 实现幻灯片内容渲染区域
- [x] 实现页码指示器（1 / 8）
- [x] 实现关闭按钮
- [x] 响应uiStore状态变化
- [x] 加载态和错误态显示

**依赖**: T003, T005

**布局结构**:
```vue
<Modal :open="uiStore.pptPreviewOpen" size="6xl" @close="uiStore.closePPTPreview">
  <div class="h-[80vh] flex flex-col">
    <!-- Header -->
    <div class="flex justify-between items-center p-4 border-b">
      <h3>{{ paperTitle }}</h3>
      <button @click="close">×</button>
    </div>

    <!-- Loading State -->
    <div v-if="pptContentLoading">加载中...</div>

    <!-- Error State -->
    <div v-else-if="pptContentError">{{ pptContentError }}</div>

    <!-- Slide Content -->
    <div v-else class="flex-1 overflow-y-auto p-8 bg-gray-50">
      <div class="slide-content" v-html="currentSlideHTML"></div>
    </div>

    <!-- Footer -->
    <div class="flex justify-between items-center p-4 border-t">
      <span>{{ currentSlideIndex + 1 }} / {{ totalSlides }}</span>
    </div>
  </div>
</Modal>
```

---

### T007: 实现幻灯片翻页逻辑
**优先级**: P1
**预计时间**: 45分钟
**描述**: 添加上一页/下一页按钮和翻页逻辑

**验收标准**:
- [x] 添加"上一页"和"下一页"按钮
- [x] 实现 `nextSlide()` 和 `prevSlide()` 方法
- [x] 边界处理（第一页禁用上一页，最后一页禁用下一页）
- [x] 翻页时内容正确更新
- [x] 按钮使用现有Button组件

**依赖**: T006

**实现示例**:
```javascript
const currentSlideIndex = ref(0)

const nextSlide = () => {
  if (currentSlideIndex.value < renderedSlides.value.length - 1) {
    currentSlideIndex.value++
  }
}

const prevSlide = () => {
  if (currentSlideIndex.value > 0) {
    currentSlideIndex.value--
  }
}

const currentSlideHTML = computed(() => {
  return renderedSlides.value[currentSlideIndex.value] || ''
})
```

---

### T008: 修改TaskItem组件添加预览按钮
**优先级**: P0
**预计时间**: 30分钟
**描述**: 为completed状态的任务添加"预览"按钮

**验收标准**:
- [x] 在"下载PPT"按钮旁添加"预览"按钮
- [x] 仅当 `task.status === 'completed'` 时显示
- [x] 按钮样式使用 `variant="secondary"`, `size="small"`
- [x] 点击触发 `uiStore.openPPTPreview(task.id)`
- [x] 使用眼睛图标（Heroicons: eye）

**依赖**: T005

**代码修改位置**: `src/components/core/TaskItem.vue:169-191`

---

### T009: 集成PPTPreviewModal到App.vue
**优先级**: P0
**预计时间**: 15分钟
**描述**: 在App根组件中引入预览Modal

**验收标准**:
- [x] 在App.vue中导入PPTPreviewModal
- [x] 添加到template中（与PaperModal并列）
- [x] 确认Modal可正常打开和关闭
- [x] 不影响现有PaperModal功能

**依赖**: T006

**代码修改**:
```vue
<!-- App.vue -->
<template>
  <div id="app">
    <Toast />
    <PaperModal />
    <PPTPreviewModal />  <!-- 新增 -->
    <router-view />
  </div>
</template>

<script setup>
import PPTPreviewModal from '@/components/core/PPTPreviewModal.vue'
</script>
```

---

## Phase 3: 增强功能 (Enhancements)

### T010: 实现键盘导航
**优先级**: P1
**预计时间**: 30分钟
**描述**: 支持方向键翻页和ESC关闭

**验收标准**:
- [x] ← 键触发上一页
- [x] → 键触发下一页
- [x] ESC键关闭Modal
- [x] Home键跳转第一页（可选）
- [x] End键跳转最后一页（可选）
- [x] 仅当Modal打开时监听键盘事件
- [x] 组件卸载时移除监听器

**依赖**: T007

**实现示例**:
```javascript
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const handleKeydown = (e) => {
  if (!uiStore.pptPreviewOpen) return
  if (e.key === 'ArrowLeft') prevSlide()
  if (e.key === 'ArrowRight') nextSlide()
  if (e.key === 'Escape') uiStore.closePPTPreview()
}
```

---

### T011: 添加幻灯片样式美化（包含代码和公式）
**优先级**: P0 (Critical)
**预计时间**: 75分钟
**描述**: 优化幻灯片内容的排版和样式，包含代码高亮和数学公式渲染

**验收标准**:
- [x] 导入highlight.js和katex的CSS文件
- [x] 使用Tailwind Typography插件 (`@tailwindcss/typography`)
- [x] 自定义标题样式（h1, h2, h3）
- [x] 优化列表、表格、代码块样式
- [x] 添加KaTeX数学公式样式（行内和块级）
- [x] 添加highlight.js代码高亮样式（github-dark主题）
- [x] 添加幻灯片背景和阴影效果
- [x] 确保中文字体正确渲染（Noto Sans SC）
- [x] 遵循8px网格间距

**依赖**: T001, T006

**样式参考**:
```vue
<script setup>
import 'highlight.js/styles/github-dark.css'
import 'katex/dist/katex.min.css'
</script>

<style scoped>
.slide-content :deep(h1) {
  @apply text-3xl font-bold text-text-primary mb-6 pb-3 border-b-2 border-accent;
}

.slide-content :deep(pre) {
  @apply bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto mb-4;
}

.slide-content :deep(.katex) {
  @apply text-text-primary;
  font-size: 1.1em;
}
</style>
```

---

### T012: 实现加载骨架屏
**优先级**: P2
**预计时间**: 30分钟
**描述**: 为加载状态添加骨架屏动画

**验收标准**:
- [x] 创建幻灯片加载骨架
- [x] 包含标题、段落、列表的占位符
- [x] 使用脉冲动画 (`animate-pulse`)
- [x] 与实际内容布局一致

**依赖**: T006

---

### T013: 添加错误状态UI
**优先级**: P1
**预计时间**: 30分钟
**描述**: 优化错误展示和重试交互

**验收标准**:
- [x] 显示错误图标和描述性文案
- [x] 提供"重新加载"按钮
- [x] 区分不同错误类型（网络错误、内容不存在、渲染失败）
- [x] 错误信息中英文友好

**依赖**: T006

---

### T014: 实现渲染缓存
**优先级**: P2
**预计时间**: 30分钟
**描述**: 避免重复渲染相同taskId的内容

**验收标准**:
- [x] 在uiStore中添加 `renderedCache` Map
- [x] 首次加载后缓存渲染结果
- [x] 再次打开时直接使用缓存
- [x] 缓存最多保留10个任务（LRU策略）

**依赖**: T005

**实现示例**:
```javascript
const renderedCache = new Map() // taskId → { content, renderedSlides }

const openPPTPreview = async (taskId) => {
  if (renderedCache.has(taskId)) {
    currentPPTContent.value = renderedCache.get(taskId)
    pptPreviewOpen.value = true
    return
  }

  // ... 正常加载流程 ...
  renderedCache.set(taskId, content)

  // LRU清理
  if (renderedCache.size > 10) {
    const firstKey = renderedCache.keys().next().value
    renderedCache.delete(firstKey)
  }
}
```

---

### T015: 创建水印组件
**优先级**: P0 (Critical)
**预计时间**: 60分钟
**描述**: 实现Watermark组件，支持9宫格分布和环境变量配置

**验收标准**:
- [x] 创建 `src/components/common/Watermark.vue`
- [x] 实现9宫格水印位置分布（含旋转）
- [x] 支持props配置（text, opacity, fontSize, color）
- [x] 创建 `src/config/watermark.js` 配置文件
- [x] 添加环境变量支持（.env.development / .env.production）
- [x] 水印不阻止用户交互（pointerEvents: none）
- [x] 水印不可选中（userSelect: none）

**依赖**: 无

**环境变量配置**:
```bash
# .env.development
VITE_WATERMARK_TEXT="论导Lite 预览版 - lundao.com"
VITE_WATERMARK_OPACITY=0.08
VITE_WATERMARK_ENABLED=true
```

**组件代码骨架**:
```vue
<template>
  <div class="watermark-container" :style="containerStyle">
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
const watermarkPositions = [
  { top: '10%', left: '10%', rotate: -30 },
  { top: '10%', left: '50%', rotate: -30 },
  // ... 共9个位置
]
</script>
```

---

### T016: 集成水印到预览Modal
**优先级**: P0 (Critical)
**预计时间**: 20分钟
**描述**: 将Watermark组件集成到PPTPreviewModal中

**验收标准**:
- [x] 在PPTPreviewModal中导入Watermark组件
- [x] 将Watermark添加到幻灯片内容区域（relative定位容器内）
- [x] 水印覆盖整个幻灯片区域
- [x] 水印不影响内容可读性
- [x] 使用环境变量中的配置

**依赖**: T006, T015

**集成代码**:
```vue
<!-- PPTPreviewModal.vue -->
<div class="max-w-4xl mx-auto bg-white shadow-lg rounded-lg p-12 relative">
  <div class="slide-content" v-html="renderedSlides[currentSlideIndex]"></div>

  <!-- 水印叠加层 -->
  <Watermark
    :text="watermarkConfig.text"
    :opacity="watermarkConfig.opacity"
  />
</div>
```

---

## Phase 4: 测试与优化 (Testing & Optimization)

### T017: 功能测试（包含水印和公式代码）
**优先级**: P1
**预计时间**: 75分钟
**描述**: 手动测试所有功能点，包含新增的水印、数学公式和代码高亮

**测试用例**:
- [x] TC1: 点击completed任务的"预览"按钮，Modal正常打开
- [x] TC2: Markdown正确渲染为HTML（标题、列表、表格、代码、公式）
- [x] TC3: 代码高亮正常工作（Python, JavaScript等7种语言）
- [x] TC4: LaTeX数学公式正常渲染（行内 `$...$` 和块级 `$$...$$`）
- [x] TC5: 翻页功能正常（按钮和键盘）
- [x] TC6: 关闭功能正常（按钮和ESC键）
- [x] TC7: 水印正常显示（9个位置，半透明，旋转-30度）
- [x] TC8: 水印不影响用户交互（可点击、可选中内容）
- [x] TC9: 失败任务（mock-task-003）显示错误提示
- [x] TC10: 加载态正常显示
- [x] TC11: Mock模式和Real API模式切换正常
- [x] TC12: 响应式布局在移动端正常

**依赖**: T001-T016

---

### T018: 安全性测试
**优先级**: P0 (Critical)
**预计时间**: 40分钟
**描述**: 验证XSS防护和输入验证

**测试用例**:
- [x] XSS1: Markdown包含 `<script>alert('XSS')</script>` → 渲染后无<script>标签
- [x] XSS2: Markdown包含 `<iframe src="evil.com">` → 渲染后无<iframe>
- [x] XSS3: Markdown包含 `<img onerror="alert('XSS')">` → onerror事件被移除
- [x] XSS4: LaTeX公式中的恶意代码被正确转义
- [x] Input1: taskId为空字符串 → 显示错误提示
- [x] Input2: taskId超长（>100字符） → 正常处理或显示错误
- [x] Water1: 通过DevTools尝试删除水印 → 功能正常（MVP阶段允许）

**依赖**: T003

---

### T019: 性能测试与优化
**优先级**: P2
**预计时间**: 60分钟
**描述**: 测量并优化性能指标，包含新依赖的影响评估

**测试场景**:
- [x] Perf1: 首次打开预览的延迟（目标 < 800ms，含KaTeX加载）
- [x] Perf2: 翻页响应速度（目标 < 100ms）
- [x] Perf3: Bundle size增长（实际约160KB gzipped）
- [x] Perf4: 内存占用（10次打开/关闭后无明显泄漏）
- [x] Perf5: KaTeX渲染性能（复杂公式 < 50ms）
- [x] Perf6: Highlight.js渲染性能（长代码块 < 100ms）

**优化策略**:
- 使用 `import()` 动态加载 pptRenderer.js
- 启用渲染缓存（T014）
- KaTeX字体CDN加载（可选）
- 图片懒加载（如果幻灯片包含图片）

**Bundle Size分析**:
```bash
npm run build
# 使用 webpack-bundle-analyzer 分析
# 预期：marked (32KB) + katex (340KB) + hljs (80KB) + dompurify (13KB) ≈ 160KB gzipped
```

**依赖**: T014

---

### T020: 文档更新
**优先级**: P1
**预计时间**: 40分钟
**描述**: 更新项目文档，包含水印、公式、代码高亮功能说明

**验收标准**:
- [x] 更新 `CLAUDE.md` 添加Feature #004介绍
- [x] 更新 `README.md` 添加预览功能说明（含依赖列表）
- [x] 创建 `specs/004-ppt-preview-feature/README.md`
- [x] 更新Mock系统文档 `src/mocks/README.md`
- [x] 记录水印配置方法（环境变量）
- [x] 记录支持的代码语言列表（7种）
- [x] 提供LaTeX公式示例文档

**依赖**: T017

**文档内容**:
- 功能概述（强调学术场景优化）
- 使用方法
- 技术架构图
- 完整依赖清单（5个npm包 + 2个CSS）
- API契约
- 水印配置指南
- 常见问题（公式渲染、代码高亮、水印修改）

---

## 任务依赖图

```
Phase 1 (Foundation)
T001 (安装完整依赖: marked+katex+hljs+dompurify)
  ↓
T002 (Mock数据+公式代码) → T004 (API服务)
  ↓                         ↓
T003 (渲染工具+KaTeX+hljs)─┘
  ↓
Phase 2 (Core Components)
T005 (Store扩展)
  ↓
T006 (Modal组件) → T007 (翻页) → T010 (键盘导航)
  ↓                  ↓              ↓
T008 (预览按钮)     T011 (样式+CSS导入)
  ↓                  ↓
T009 (集成App)      T012 (骨架屏)
  ↓                  ↓
Phase 3 (Enhancements + Watermark)
T013 (错误UI) → T014 (缓存) → T015 (水印组件)
                                ↓
                              T016 (水印集成)
                                ↓
Phase 4 (Testing & Optimization)
T017 (功能测试+水印公式代码) → T018 (安全测试+XSS)
                                 ↓
                              T019 (性能测试+Bundle分析)
                                 ↓
                              T020 (文档更新+依赖说明)
```

---

## 实施建议

### 最小可行产品（MVP）
**必须完成**: T001-T009, T011, T015-T016（核心功能 + 水印）
**增强功能**: T010, T012-T014（键盘、骨架屏、缓存）
**测试优化**: T017-T020（测试、文档）

### 工作节奏（更新后）
- **第1天** (5小时): Phase 1 + Phase 2基础 (T001-T009)
- **第2天** (4小时): Phase 2完善 + Phase 3 (T010-T016)
- **第3天** (3小时): Phase 4测试文档 (T017-T020)
- **总计**: 10-14小时（含缓冲）

### 关键里程碑
1. **里程碑1** (完成T001-T006): 基础渲染功能可用
2. **里程碑2** (完成T001-T009): 核心预览流程打通
3. **里程碑3** (完成T001-T016): 完整功能（含水印）
4. **里程碑4** (完成T001-T020): 生产就绪

### 风险管理
- **高风险任务**:
  - T003 (渲染工具): KaTeX和Highlight.js集成复杂，预留额外30分钟调试
  - T006 (Modal组件): 多依赖集成，预留20%缓冲时间
  - T019 (性能测试): Bundle size可能超预期，准备CDN备选方案

- **依赖风险**:
  - KaTeX字体加载慢: 考虑CDN或字体子集化
  - 如果后端API延迟，确保Mock模式功能完整

- **技术验证建议**:
  - 先完成T001-T003，验证渲染管道正常后再继续
  - T015完成后立即测试水印效果，确认不影响交互

---

## 验收检查清单

### 功能完整性
- [ ] 已完成任务显示"预览"按钮
- [ ] 点击预览打开Modal
- [ ] Markdown正确渲染为HTML
- [ ] **LaTeX数学公式正确渲染**（行内和块级）
- [ ] **代码语法高亮正常工作**（7种语言）
- [ ] **水印正常显示**（9宫格分布，半透明）
- [ ] 幻灯片翻页功能正常
- [ ] 键盘导航支持（← → ESC）
- [ ] 关闭功能正常
- [ ] 加载态/错误态显示正常

### 代码质量
- [ ] ESLint无错误
- [ ] 无console.error（除捕获的错误）
- [ ] 组件可复用性良好
- [ ] 注释完整（关键逻辑，尤其渲染管道）
- [ ] 水印组件Props清晰

### 性能标准
- [ ] Bundle size增长 ≈ 160KB gzipped（实际测量）
- [ ] 首次打开延迟 < 800ms（含KaTeX加载）
- [ ] 翻页响应 < 100ms
- [ ] 无内存泄漏（10次开关测试）
- [ ] KaTeX公式渲染 < 50ms
- [ ] Highlight.js代码渲染 < 100ms

### 安全标准
- [ ] XSS防护测试通过（包含LaTeX注入）
- [ ] DOMPurify白名单配置正确（含KaTeX标签）
- [ ] 输入验证测试通过
- [ ] 敏感数据无泄露
- [ ] 水印防篡改（MVP阶段基础防护）

### 依赖管理
- [ ] package.json包含5个新依赖
- [ ] 依赖版本锁定（package-lock.json）
- [ ] CSS正确导入（highlight.js + katex）
- [ ] 按需加载语言（hljs仅7种，非全量）

### 文档完整性
- [ ] CLAUDE.md已更新（含依赖清单）
- [ ] API契约已定义
- [ ] 代码注释清晰
- [ ] 使用指南完整（水印配置、LaTeX语法、代码语言列表）
- [ ] 环境变量文档完整

---

**任务状态**: ⏸️ 待开始
**最后更新**: 2025-01-15 (Updated)
**负责人**: 待分配
**预计交付**: 10-14小时后
