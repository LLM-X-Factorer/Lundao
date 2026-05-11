# PPT内容策略与结构模板

**版本**: v1.0
**创建日期**: 2025-10-16
**目标场景**: 15分钟组会论文汇报
**目标页数**: 10-13页

---

## 一、整体设计原则

### 1.1 核心约束

| 规则 | 具体要求 | 理由 |
|------|---------|------|
| **5×5规则** | 每句≤10中文字，每页≤5行 | 避免信息过载 |
| **1分钟原则** | 1页=1分钟讲解 | 15分钟汇报=10-13页 |
| **视觉优先** | 图表>文字，公式简化 | 提升理解效率 |
| **叙事连贯** | 问题→方法→结果→意义 | 提升30%留存率 |
| **字号规范** | 标题≥36pt，正文≥28pt | 确保可读性 |

### 1.2 内容来源（论导Lite已有数据）

我们的独特优势：**无需用户输入，直接利用AI分析结果**

```javascript
// 已有数据结构（来自paperData.js和AI分析）
{
  "paperId": "2301.00001",
  "title": "论文标题（英文）",
  "chineseTitle": "论文标题（中文翻译）",  // 可选
  "authors": ["作者1", "作者2"],
  "field": "研究领域",
  "date": "2023-01-01",
  "arxivId": "2301.00001",

  // AI分析结果（核心数据源）
  "aiAnalysis": {
    "chineseSummary": "中文摘要（200-300字）",
    "innovationPoints": [
      {
        "icon": "🎯",
        "iconLabel": "核心创新",
        "title": "创新点1标题",
        "description": "创新点1详细说明（50-100字）"
      },
      // ... 通常3个创新点
    ]
  }
}
```

### 1.3 PPT类型识别（未来扩展）

当前MVP阶段：统一使用**实验型论文**结构

未来可根据论文特征自动识别：
- **实验型**（Experimental）：背景→方法→实验→结果（80%的ML/CV论文）
- **理论型**（Theoretical）：问题→定理→证明→应用
- **综述型**（Survey）：分类→对比→趋势→展望

---

## 二、标准结构模板（10-13页）

### Page 1: 封面页（Cover）

**目的**: 建立第一印象，传达论文基本信息

**内容组成**:
```markdown
# [论文英文标题]
### [论文中文标题]（如有）

**作者**: [作者列表]
**发表**: [会议/期刊] [年份]
**领域**: [研究领域]

---

**汇报人**: 论导Lite AI生成
**日期**: [当前日期]
```

**设计规范**:
- 标题：36-42pt，加粗
- 副标题（中文）：28pt，常规
- 元信息：24pt，浅灰色
- 背景：纯色或微妙渐变（避免花哨）

**示例（Markdown）**:
```markdown
# Hierarchical Reasoning in Large Language Models
### 大语言模型中的层次化推理

**作者**: John Doe, Jane Smith
**发表**: NeurIPS 2023
**领域**: 自然语言处理

---

**汇报人**: 论导Lite AI生成
**日期**: 2025-10-16
```

---

### Page 2: 大纲页（Outline）

**目的**: 让听众预知汇报结构，建立预期

**内容组成**:
```markdown
## 汇报大纲

1. **研究背景** - 问题是什么？为何重要？
2. **核心创新** - 本文提出了什么新方法？
3. **技术方法** - 如何实现？
4. **实验结果** - 效果如何？
5. **总结启发** - 对我们的研究有何借鉴？
```

**设计规范**:
- 使用编号列表（1, 2, 3...）
- 每项不超过15个中文字
- 可添加emoji图标增强视觉效果

**Markdown模板**:
```markdown
## 汇报大纲

1. 🎯 **研究背景** - [问题陈述]
2. 💡 **核心创新** - [关键方法]
3. 🔧 **技术方法** - [实现方式]
4. 📊 **实验结果** - [性能提升]
5. 🚀 **总结启发** - [启发意义]
```

---

### Page 3-4: 研究背景（Background，2页）

**目的**: 让听众理解问题的重要性和现有方法的局限

**Page 3: 问题陈述**

**内容slot**:
```markdown
## 研究背景：问题是什么？

### 当前挑战
[从chineseSummary提取前1-2句，描述核心问题]

### 为什么重要？
- **应用价值**: [实际场景]
- **理论意义**: [学术价值]
- **挑战难度**: [技术瓶颈]
```

**生成规则**:
```javascript
// 伪代码
background_page1 = {
  title: "研究背景：问题是什么？",
  challenge: extractFirstSentence(chineseSummary), // 提取摘要第1句
  importance: [
    generateImportancePoint("应用价值"),
    generateImportancePoint("理论意义"),
    generateImportancePoint("挑战难度")
  ]
}
```

**Page 4: 现有方法与局限**

**内容slot**:
```markdown
## 现有方法的局限

### 传统方法
- **方法A**: [简短描述] → ❌ [局限性]
- **方法B**: [简短描述] → ❌ [局限性]

### 核心矛盾
[用一句话总结：理想目标 vs. 现实困境]

> **研究空白**: [本文要填补的gap]
```

**生成规则**:
```javascript
background_page2 = {
  title: "现有方法的局限",
  existingMethods: extractMethodsFromSummary(chineseSummary), // 从摘要提取
  coreConflict: "现有方法A无法同时满足X和Y",
  researchGap: innovationPoints[0].description // 用第1个创新点反推gap
}
```

---

### Page 5: 核心创新点（Innovation，1页）🔥

**目的**: PPT的核心，必须清晰、震撼

**内容组成**:
```markdown
## 核心创新：本文提出了什么？

### 💡 [创新点1标题]
[创新点1描述]（20-30字）

### 💡 [创新点2标题]
[创新点2描述]（20-30字）

### 💡 [创新点3标题]
[创新点3描述]（20-30字）

---

**关键区别**: [与已有方法的本质不同]
```

**数据映射**:
```javascript
// 直接使用innovationPoints数据
innovation_page = {
  title: "核心创新：本文提出了什么？",
  points: innovationPoints.map(point => ({
    icon: point.icon,
    title: point.title,
    description: simplify(point.description, maxLength: 30) // 简化到30字
  })),
  keyDifference: generateKeyDifference(innovationPoints) // 提炼关键区别
}
```

**设计规范**:
- 使用大图标（emoji或SVG）
- 每个创新点：图标 + 标题（加粗） + 描述（1行）
- 底部突出"关键区别"（引用块或高亮框）

---

### Page 6-7: 技术方法（Method，2-3页）

**目的**: 讲清楚"怎么做"，但避免过度细节

**Page 6: 方法概览**

**内容slot**:
```markdown
## 技术方法：如何实现？

### 整体框架
[简化的系统架构描述，50字内]

```
[架构图ASCII art或占位符]
输入 → [模块A] → [模块B] → 输出
```

### 核心组件
- **[模块A]**: [功能描述]（10字）
- **[模块B]**: [功能描述]（10字）
```

**生成策略**:
- 从chineseSummary提取方法关键词
- 如果有"框架"、"模型"、"算法"等关键词，尝试生成简化架构图
- 最多3个核心组件

**Page 7: 关键技术细节（可选）**

**内容slot**:
```markdown
## 关键技术：[核心算法名称]

### 核心公式（简化版）
$$
[最重要的一个公式]
$$

### 算法流程
1. **步骤1**: [描述]
2. **步骤2**: [描述]
3. **步骤3**: [描述]
```

**生成规则**:
- 如果论文是算法类，生成此页
- 如果是系统类，用系统流程图替代
- 公式：仅保留1个最核心的（从论文中提取）

---

### Page 8-9: 实验结果（Results，2-3页）

**目的**: 用数据证明方法有效性

**Page 8: 性能对比**

**内容slot**:
```markdown
## 实验结果：效果如何？

### 数据集
- **[数据集1]**: [规模/特点]
- **[数据集2]**: [规模/特点]

### 性能对比

| 方法 | 指标1 | 指标2 | 指标3 |
|------|-------|-------|-------|
| Baseline | X.X% | X.X | X.X |
| Method A | X.X% | X.X | X.X |
| **本文方法** | **X.X%** ✅ | **X.X** ✅ | **X.X** ✅ |

**关键提升**: [对比baseline提升了多少]
```

**生成策略**:
- 从chineseSummary提取性能数字（如"提升10%"）
- 表格最多4列（方法名 + 3个核心指标）
- 本文方法加粗，最佳结果用✅标记

**Page 9: 消融实验/可视化（可选）**

**内容slot**:
```markdown
## 深入分析

### 消融实验
[验证各模块的贡献]

| 配置 | 性能 |
|------|------|
| 完整模型 | X.X% |
| -模块A | X.X% ↓ |
| -模块B | X.X% ↓↓ |

### 可视化案例
[如有图片/示例，添加占位符或ASCII art]
```

---

### Page 10: 总结与启发（Conclusion，1页）

**目的**: 强化记忆，引发思考

**内容组成**:
```markdown
## 总结与启发

### 主要贡献
1. ✅ [贡献1]（从创新点提炼）
2. ✅ [贡献2]
3. ✅ [贡献3]

### 局限性
- **[局限1]**: [描述]
- **[局限2]**: [描述]

### 对我们的启发
💡 [可借鉴的方法/思路]

### 未来方向
🔮 [可能的改进/扩展]
```

**生成规则**:
```javascript
conclusion_page = {
  contributions: innovationPoints.map(p => p.title), // 复用创新点
  limitations: generateLimitations(chineseSummary), // 从摘要推断
  inspiration: "可将该方法应用于[相关领域]",
  future: "进一步优化[某个模块]"
}
```

---

### Page 11: 致谢/Q&A（End，1页）

**内容组成**:
```markdown
## Thank You!

### 论文信息
**标题**: [论文标题]
**作者**: [作者列表]
**链接**: [arXiv链接]

---

### 欢迎讨论！

📧 [联系方式]
💬 [问题与反馈]

---

*本PPT由论导Lite AI自动生成*
```

---

## 三、Markdown格式规范

### 3.1 幻灯片分隔符

使用`---`（三个连字符）分隔幻灯片：

```markdown
# 第1页标题
内容...

---

# 第2页标题
内容...
```

### 3.2 标题层级

| Markdown | 用途 | 示例 |
|----------|------|------|
| `#` | 页面主标题 | `# 研究背景` |
| `##` | 小节标题 | `## 核心挑战` |
| `###` | 子标题 | `### 数据集说明` |

**注意**: 每页最多用到`###`三级标题，避免层级过深。

### 3.3 内容元素

#### Bullet Points
```markdown
- **要点1**: 描述
- **要点2**: 描述
  - 子要点（缩进2空格）
```

#### 表格（精简版）
```markdown
| 方法 | 指标1 | 指标2 |
|------|-------|-------|
| Baseline | 85.3% | 0.72 |
| **本文** | **92.1%** ✅ | **0.89** ✅ |
```

**规则**:
- 最多4列
- 表头加粗
- 最佳结果用粗体+✅

#### 公式（简化）
```markdown
行内公式：损失函数为 $L = \sum_{i=1}^{n} \ell(y_i, \hat{y}_i)$

块级公式（居中）：
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
```

**原则**: 每页最多1个块级公式

#### 引用块（重点标注）
```markdown
> **核心观点**: 本文首次提出了X方法，解决了Y问题。
```

#### 代码（谨慎使用）
```markdown
```python
# 仅当算法核心逻辑简单时使用
def core_algorithm(x):
    return transform(x)
```
```

**建议**: 组会PPT中避免大段代码，用伪代码或流程图替代。

### 3.4 视觉增强元素

#### Emoji图标
```markdown
- 🎯 **目标**: ...
- 💡 **创新**: ...
- 📊 **结果**: ...
- 🚀 **展望**: ...
```

**常用emoji**:
- 问题/挑战：❓ ⚠️ 🔍
- 方法/创新：💡 🎯 ⚡
- 结果/成功：✅ 📊 📈
- 总结/展望：🚀 🔮 💬

#### ASCII图（架构/流程）
```markdown
```
输入数据
    ↓
[Encoder] → 特征表示
    ↓
[Decoder] → 输出结果
```
```

---

## 四、内容生成算法（伪代码）

### 4.1 主流程

```javascript
function generatePPTContent(paper) {
  const { title, authors, field, date, aiAnalysis } = paper
  const { chineseSummary, innovationPoints } = aiAnalysis

  const slides = []

  // Page 1: 封面
  slides.push(generateCoverPage(title, authors, field, date))

  // Page 2: 大纲
  slides.push(generateOutlinePage())

  // Page 3-4: 背景（2页）
  slides.push(...generateBackgroundPages(chineseSummary))

  // Page 5: 核心创新（1页）
  slides.push(generateInnovationPage(innovationPoints))

  // Page 6-7: 方法（2-3页）
  slides.push(...generateMethodPages(chineseSummary, innovationPoints))

  // Page 8-9: 结果（2-3页）
  slides.push(...generateResultPages(chineseSummary))

  // Page 10: 总结
  slides.push(generateConclusionPage(innovationPoints, chineseSummary))

  // Page 11: 致谢
  slides.push(generateEndPage(title, authors))

  return slides.join('\n\n---\n\n') // 用---分隔
}
```

### 4.2 关键函数

#### 提取背景信息
```javascript
function extractBackground(chineseSummary) {
  // 规则1: 提取第1-2句作为问题陈述
  const sentences = chineseSummary.split('。')
  const problem = sentences.slice(0, 2).join('。')

  // 规则2: 查找"现有方法"、"传统方法"等关键词
  const methodKeywords = ['现有方法', '传统方法', '以往研究']
  const limitations = findSentencesWith(chineseSummary, methodKeywords)

  return { problem, limitations }
}
```

#### 简化创新点描述
```javascript
function simplifyInnovationPoint(description, maxLength = 30) {
  // 如果描述≤30字，直接返回
  if (description.length <= maxLength) return description

  // 否则，提取第1句
  const firstSentence = description.split('。')[0]

  // 如果第1句仍然太长，截断并加省略号
  return firstSentence.length <= maxLength
    ? firstSentence
    : firstSentence.substring(0, maxLength - 3) + '...'
}
```

#### 生成对比表格
```javascript
function generateComparisonTable(chineseSummary) {
  // 从摘要中提取性能数字
  const numbers = extractNumbers(chineseSummary) // 如"提升10%"

  // 生成模拟数据（MVP阶段）
  const baseline = numbers[0] || '85.0%'
  const ourMethod = numbers[1] || '92.0%'

  return `
| 方法 | 准确率 | F1分数 |
|------|--------|--------|
| Baseline | ${baseline} | 0.78 |
| **本文方法** | **${ourMethod}** ✅ | **0.89** ✅ |
  `.trim()
}
```

---

## 五、质量检查清单

生成PPT后，自动检查以下项：

### 5.1 结构检查

- [ ] 总页数在10-13页之间
- [ ] 每页都有明确的标题（`#`或`##`）
- [ ] 使用`---`正确分隔幻灯片
- [ ] 第1页是封面，最后1页是致谢

### 5.2 内容检查

- [ ] 每页文字不超过5行（bullet points除外）
- [ ] 每行文字不超过30个中文字
- [ ] 表格不超过4列
- [ ] 每页最多1个公式或代码块

### 5.3 叙事检查

- [ ] 有明确的"问题→方法→结果"流程
- [ ] 创新点独立成页且清晰可见
- [ ] 总结页呼应创新点

### 5.4 视觉检查

- [ ] 使用了emoji或图标增强视觉效果
- [ ] 关键信息用**粗体**或✅标记
- [ ] 重要观点用引用块`>`突出

---

## 六、示例：完整PPT（简化版）

```markdown
# Hierarchical Reasoning in Large Language Models
### 大语言模型中的层次化推理

**作者**: John Doe, Jane Smith
**发表**: NeurIPS 2023
**领域**: 自然语言处理

---

**汇报人**: 论导Lite AI生成
**日期**: 2025-10-16

---

## 汇报大纲

1. 🎯 **研究背景** - 复杂推理任务的挑战
2. 💡 **核心创新** - 层次化推理框架
3. 🔧 **技术方法** - 自底向上的推理机制
4. 📊 **实验结果** - 多个任务上的性能提升
5. 🚀 **总结启发** - 对多步推理的启发

---

## 研究背景：问题是什么？

### 当前挑战
大语言模型在复杂多步推理任务中容易出错，尤其是需要层次化思考的问题。

### 为什么重要？
- **应用价值**: 数学推理、代码生成、逻辑推导
- **理论意义**: 理解模型的推理能力边界
- **挑战难度**: 如何让模型"分而治之"

---

## 现有方法的局限

### 传统方法
- **Chain-of-Thought**: 顺序推理 → ❌ 难以处理复杂分支
- **Tree-of-Thought**: 树形搜索 → ❌ 计算成本高

### 核心矛盾
需要强推理能力，但又要保持高效率

> **研究空白**: 缺少轻量级的层次化推理框架

---

## 核心创新：本文提出了什么？

### 💡 层次化推理框架
将复杂问题分解为多层子问题，自底向上求解

### 💡 动态子问题生成
根据问题特点自动调整分解粒度

### 💡 轻量级验证机制
每层推理结果自我验证，减少错误累积

---

**关键区别**: 相比CoT的顺序推理，本文实现了真正的层次化分治

---

## 技术方法：如何实现？

### 整体框架

```
问题输入 → [子问题生成] → [分层求解] → [结果聚合] → 最终答案
```

### 核心组件
- **分解器**: 将问题拆解为子问题
- **求解器**: 逐层求解各子问题
- **聚合器**: 整合各层结果

---

## 实验结果：效果如何？

### 数据集
- **GSM8K**: 小学数学应用题（8,000题）
- **MATH**: 高中数学竞赛题（12,500题）

### 性能对比

| 方法 | GSM8K | MATH | 平均 |
|------|-------|------|------|
| GPT-4 | 92.0% | 52.9% | 72.5% |
| CoT | 85.0% | 45.2% | 65.1% |
| **本文** | **95.3%** ✅ | **58.7%** ✅ | **77.0%** ✅ |

**关键提升**: 相比GPT-4基线提升3.3%，相比CoT提升10%+

---

## 总结与启发

### 主要贡献
1. ✅ 提出轻量级层次化推理框架
2. ✅ 实现动态子问题生成机制
3. ✅ 在多个任务上达到SOTA性能

### 局限性
- **适用范围**: 主要针对数学/逻辑推理，其他领域待验证
- **计算开销**: 比CoT增加约20%推理时间

### 对我们的启发
💡 可将层次化思想应用于其他需要多步决策的任务

### 未来方向
🔮 扩展到开放域问答、代码生成等场景

---

## Thank You!

### 论文信息
**标题**: Hierarchical Reasoning in Large Language Models
**作者**: John Doe, Jane Smith
**链接**: https://arxiv.org/abs/2301.00001

---

### 欢迎讨论！

💬 如有问题，欢迎提出

---

*本PPT由论导Lite AI自动生成*
```

---

## 七、下一步实施

### 7.1 今天（2小时）

1. **重写pptContentData.js**
   - 将demo-default改为上述12页结构
   - 基于Hierarchical Reasoning论文生成内容

2. **优化mock-task-001和mock-task-002**
   - 应用相同的结构和内容策略
   - 确保所有mock PPT符合学术标准

### 7.2 明天（1小时）

3. **测试预览效果**
   - 检查页面布局、字体大小
   - 确认5×5规则和1分钟原则

4. **创建内容生成指南文档**
   - 为未来Feature #005提供参考
   - 记录设计决策和最佳实践

### 7.3 后天（30分钟）

5. **提交代码并更新README**
   - Git commit with detailed message
   - 更新Mock系统文档

---

**文档版本**: v1.0
**最后更新**: 2025-10-16
**状态**: ✅ 设计完成，准备实施
