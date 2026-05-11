# Feature #004 实施指南 (SpecKit方法论)

## SpecKit工作流概览

```
规格说明 (Specification) → 实施计划 (Planning) → 执行实施 (Implementation) → 验证交付 (Verification)
     ✅                          ✅                        ⏳                           ⏸️
```

**当前阶段**: Implementation (执行实施)

---

## 第一步：环境准备与验证

### 1.1 确认开发环境

```bash
# 1. 检查Node版本
node --version  # 应 >= v18.0.0
npm --version   # 应 >= v9.0.0

# 2. 确认当前分支
git status
git branch  # 建议创建feature分支: 004-ppt-preview

# 3. 确认开发服务器运行中
# 已有dev server在后台运行 (Bash 2690c0)
```

### 1.2 创建功能分支（推荐）

```bash
# 从main分支创建新功能分支
git checkout main
git pull origin main
git checkout -b 004-ppt-preview

# 或从当前分支创建（如果已在003-ppt-task-mock）
git checkout -b 004-ppt-preview
```

### 1.3 备份关键文件

```bash
# 备份可能被修改的文件（可选，谨慎操作）
cp package.json package.json.backup
cp src/stores/ui.js src/stores/ui.js.backup
```

---

## 第二步：Phase 1 - 基础设施搭建 (T001-T004)

### 里程碑1目标
✅ 完成后可独立测试渲染功能（公式、代码、Markdown）

---

### T001: 安装完整依赖包 (15分钟)

**操作步骤**:

```bash
# 1. 安装5个依赖
npm install marked marked-katex-extension katex highlight.js dompurify

# 2. 验证安装成功
npm list marked marked-katex-extension katex highlight.js dompurify

# 3. 检查package.json
cat package.json | grep -A 5 "dependencies"

# 预期输出包含：
# "marked": "^11.0.0"
# "marked-katex-extension": "^5.0.0"
# "katex": "^0.16.9"
# "highlight.js": "^11.9.0"
# "dompurify": "^3.0.6"
```

**验收标准**:
- [ ] package.json包含5个新依赖
- [ ] node_modules下存在对应包
- [ ] npm install 无错误警告

**如遇问题**:
```bash
# 清除缓存重试
rm -rf node_modules package-lock.json
npm install
```

**更新Todo**:
```bash
# 完成后在Claude Code中运行
# "标记T001为completed"
```

---

### T002: 创建Mock PPT内容数据 (75分钟)

**文件位置**: `src/mocks/pptContentData.js`

**操作步骤**:

```bash
# 1. 创建文件
touch src/mocks/pptContentData.js

# 2. 复制以下完整内容到文件
```

**文件内容** (复制到 `pptContentData.js`):

```javascript
/**
 * Mock PPT Content Data
 * 包含LaTeX数学公式和代码高亮示例
 */

export const mockPPTContents = {
  // Task 1: Hierarchical Reasoning Models (10页，含公式和代码)
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

  // Task 3: Failed task (null content)
  'mock-task-003': null
}

/**
 * 获取Mock PPT内容
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
 */
export function hasPPTContent(taskId) {
  return mockPPTContents[taskId] !== undefined &&
         mockPPTContents[taskId] !== null
}
```

**验收标准**:
- [ ] 文件创建成功
- [ ] 包含3个任务数据（2个有内容，1个null）
- [ ] Task 1包含LaTeX公式 (`$...$` 和 `$$...$$`)
- [ ] Task 1包含Python代码块 (````python`)
- [ ] 包含导出函数 (`getMockPPTContent`, `hasPPTContent`)

**测试建议**:
```bash
# 检查文件语法
node -c src/mocks/pptContentData.js

# 预期输出：无错误
```

---

### T003: 创建渲染工具函数 (60分钟)

**文件位置**: `src/utils/pptRenderer.js`

**操作步骤**:

```bash
# 1. 创建utils目录（如不存在）
mkdir -p src/utils

# 2. 创建文件
touch src/utils/pptRenderer.js
```

**文件内容** (复制完整代码，见technical-design.md第6节):

<details>
<summary>点击展开完整代码 (约100行)</summary>

```javascript
import { marked } from 'marked'
import markedKatex from 'marked-katex-extension'
import hljs from 'highlight.js/lib/core'
import DOMPurify from 'dompurify'

// 按需导入常用语言
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

// 配置KaTeX扩展
marked.use(markedKatex({
  throwOnError: false,
  output: 'html',
  displayMode: false,
  strict: false
}))

// 配置代码高亮
marked.setOptions({
  gfm: true,
  breaks: true,
  headerIds: false,
  highlight: (code, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.warn('Highlight.js error:', err)
      }
    }
    return code
  }
})

/**
 * 将Markdown拆分为幻灯片数组
 */
export function parseSlides(markdown) {
  if (!markdown || typeof markdown !== 'string') {
    return []
  }

  return markdown
    .split(/^---$/m)
    .map(slide => slide.trim())
    .filter(slide => slide.length > 0)
}

/**
 * 渲染单个幻灯片
 */
export function renderSlide(slideMarkdown) {
  if (!slideMarkdown || typeof slideMarkdown !== 'string') {
    return '<p class="text-gray-400">空白页</p>'
  }

  try {
    const rawHtml = marked.parse(slideMarkdown)

    const sanitizedHtml = DOMPurify.sanitize(rawHtml, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre', 'span',
        'ul', 'ol', 'li',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'blockquote', 'a', 'img',
        // KaTeX MathML tags
        'annotation', 'math', 'mrow', 'mi', 'mo', 'mn', 'mtext', 'mspace',
        'semantics', 'mstyle', 'msup', 'msub', 'mfrac', 'mover', 'munder'
      ],
      ALLOWED_ATTR: [
        'href', 'src', 'alt', 'title', 'class', 'style',
        'xmlns', 'encoding', 'data-*'
      ],
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
 */
export function renderAllSlides(markdown) {
  const slides = parseSlides(markdown)
  return slides.map(slide => renderSlide(slide))
}
```

</details>

**验收标准**:
- [ ] 文件创建成功
- [ ] 导入5个依赖（marked, katex, hljs, dompurify）
- [ ] 注册7种编程语言
- [ ] 配置KaTeX扩展
- [ ] 实现3个函数 (`parseSlides`, `renderSlide`, `renderAllSlides`)
- [ ] DOMPurify白名单包含KaTeX标签

**快速测试**:
```javascript
// 在浏览器Console测试
import { renderSlide } from '@/utils/pptRenderer'

// 测试数学公式
console.log(renderSlide('设 $n=10$，则 $T(n)=O(n \\log n)$'))
// 预期：包含 <span class="katex">

// 测试代码高亮
console.log(renderSlide('```python\nprint("Hello")\n```'))
// 预期：包含 <span class="hljs-built_in">
```

---

### T004: 创建API服务模块 (30分钟)

**文件位置**: `src/api/pptContentService.js`

**操作步骤**:

```bash
# 1. 确认api目录存在
ls src/api/

# 2. 创建文件
touch src/api/pptContentService.js
```

**文件内容**:

```javascript
import apiClient from './index'
import { getMockPPTContent } from '@/mocks/pptContentData'

// Mock模式检测
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

/**
 * 获取PPT内容（Markdown格式）
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>} PPTContent对象
 */
export async function getPPTContent(taskId) {
  if (USE_MOCK_DATA) {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    return getMockPPTContent(taskId)
  }

  // Real API
  const response = await apiClient.get('/ppt_content', {
    params: { taskId }
  })
  return response.data
}
```

**验收标准**:
- [ ] 文件创建成功
- [ ] 导入apiClient和getMockPPTContent
- [ ] 实现getPPTContent函数
- [ ] 支持Mock/Real API模式切换
- [ ] Mock模式有500ms延迟

**测试建议**:
```bash
# 检查语法
node -c src/api/pptContentService.js
```

---

### ✅ Phase 1 里程碑验证

完成T001-T004后，运行以下验证：

```bash
# 1. 依赖检查
npm list | grep -E "marked|katex|highlight|dompurify"

# 2. 文件检查
ls -lh src/mocks/pptContentData.js
ls -lh src/utils/pptRenderer.js
ls -lh src/api/pptContentService.js

# 3. 语法检查
node -c src/mocks/pptContentData.js
node -c src/utils/pptRenderer.js
node -c src/api/pptContentService.js

# 4. 构建测试（可选）
npm run build

# 预期：无错误，Bundle size增加约160KB
```

**如果验证通过**:
- 更新Todo清单（标记T001-T004为completed）
- 提交Phase 1代码
- 进入Phase 2

**如果有错误**:
- 检查依赖版本是否正确
- 查看浏览器Console错误
- 回溯到对应任务重新执行

---

## 第三步：Phase 2 - 核心组件开发 (T005-T009)

### 里程碑2目标
✅ 完成后核心预览流程可端到端运行

（下一步骤内容见后续section）

---

## SpecKit最佳实践提醒

### 1. 分阶段提交
```bash
# 每完成一个Phase，提交一次
git add .
git commit -m "feat(feature-004): complete Phase 1 - foundation (T001-T004)

- Install 5 dependencies (marked, katex, hljs, dompurify, extension)
- Create Mock PPT content with LaTeX formulas and code examples
- Implement pptRenderer.js with KaTeX and Highlight.js integration
- Create pptContentService.js with Mock/Real API support

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 2. 持续验证
- 每完成一个任务，立即测试
- 遇到错误，立即修复，不要累积
- 使用浏览器DevTools验证渲染效果

### 3. 文档同步
- 在tasks.md中标记已完成任务
- 遇到设计变更，立即更新technical-design.md
- 记录重要决策到CHANGELOG（可选）

### 4. 风险管理
- T003是高风险任务（KaTeX+Highlight.js集成），预留缓冲时间
- 如果Bundle size超预期，考虑CDN方案
- 遇到阻塞问题，及时寻求帮助（GitHub Issues, Stack Overflow）

---

## 下一步行动

### 立即执行
1. **确认环境** → 运行环境准备清单（第一步）
2. **安装依赖** → 执行T001（15分钟）
3. **验证安装** → 运行`npm list`检查
4. **更新Todo** → 标记T001为completed

### 后续节奏
- **今天**: 完成T001-T004（Phase 1，约2.5小时）
- **明天**: 完成T005-T009（Phase 2基础，约3小时）
- **第3天**: 完成T010-T016（Phase 2+3，约3.5小时）
- **第4天**: 完成T017-T020（Phase 4测试，约3小时）

---

**文档版本**: 1.0
**创建时间**: 2025-01-15
**适用范围**: Feature #004实施全流程
**方法论**: SpecKit + Todo Tracking + Milestone Verification
