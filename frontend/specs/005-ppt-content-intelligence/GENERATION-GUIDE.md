# PPT内容生成指南（快速参考）

**目标读者**: 未来Feature #005的开发者
**用途**: 从论文AI分析数据生成学术标准PPT
**基于**: 方案A的实践经验（2025-10-16）

---

## 一、黄金规则（5项）

### 1. 页数标准
- **目标**: 10-13页（15分钟汇报）
- **最少**: 10页（每页1.5分钟）
- **最多**: 13页（每页≥1分钟）

### 2. 5×5规则
- 每句话：≤10个中文字（英文≤5个单词）
- 每页：≤5行核心内容（bullet points另计）

### 3. 1分钟原则
- 1页 = 1分钟讲解时间
- 包含读标题+解释内容+过渡到下一页

### 4. 叙事结构
```
问题陈述（背景）
    ↓
现有方法局限
    ↓
核心创新（3-5个关键点）🔥 重点页
    ↓
技术方法详解
    ↓
实验结果验证
    ↓
总结与启发
```

### 5. 视觉优先
- ❌ 禁止：文献综述、大段文字、直接粘贴论文表格
- ✅ 推荐：图表、bullet points、简化公式、对比表格

---

## 二、标准12页结构（模板）

```markdown
# Page 1: 封面（Cover）
论文标题（英文）
论文标题（中文）
作者、会议/期刊、年份、领域

---

# Page 2: 大纲（Outline）
5个章节概览（使用emoji图标）

---

# Page 3: 研究背景-问题陈述
当前挑战是什么？为什么重要？（3个bullet points）

---

# Page 4: 研究背景-现有方法局限
传统方法A/B的问题 + 核心矛盾 + 研究空白

---

# Page 5: 核心创新 🔥🔥🔥
3个创新点（每个：icon + 标题 + 描述）
底部：关键区别（引用块）

---

# Page 6: 技术方法-整体框架
架构图（ASCII art或文字描述）
核心组件（3个）

---

# Page 7: 技术方法-关键技术细节
核心公式（1个）或算法流程（3-5步）

---

# Page 8: 实验结果-性能对比
数据集说明 + 对比表格（最多4列）
关键提升数字

---

# Page 9: 实验结果-深入分析
消融实验 或 零样本迁移 或 可视化案例

---

# Page 10: 应用场景（可选）
3个实际应用领域（每个2-3个bullet points）

---

# Page 11: 总结与启发
主要贡献（3个）+ 局限性（2个）+ 启发 + 未来方向

---

# Page 12: 致谢/Q&A
论文信息 + 链接 + 欢迎讨论
```

---

## 三、数据映射策略

### 从AI分析数据到PPT内容

**假设输入数据**（来自paperData.js）:
```javascript
{
  title: "论文英文标题",
  authors: ["作者1", "作者2"],
  field: "研究领域",
  date: "2023-01-01",

  aiAnalysis: {
    chineseSummary: "中文摘要（200-300字）",
    innovationPoints: [
      {
        icon: "🎯",
        iconLabel: "核心创新",
        title: "创新点1标题",
        description: "创新点1详细说明（50-100字）"
      },
      // ... 通常3个
    ]
  }
}
```

### 映射规则

| PPT页面 | 数据来源 | 生成规则 |
|---------|---------|---------|
| **Page 1: 封面** | `title`, `authors`, `field`, `date` | 直接使用，添加汇报人信息 |
| **Page 2: 大纲** | 固定模板 | 5个章节名称（研究背景/核心创新/技术方法/实验结果/总结启发） |
| **Page 3: 问题陈述** | `chineseSummary` 前1-2句 | 提取第1-2句作为"当前挑战"，生成3个"为什么重要"bullet points |
| **Page 4: 现有方法局限** | `chineseSummary` 中查找"现有方法"/"传统方法" | 提取方法名称 + 局限性，总结核心矛盾 |
| **Page 5: 核心创新** 🔥 | `innovationPoints` | 直接使用3个创新点（icon + title + description简化版≤30字） |
| **Page 6-7: 技术方法** | `chineseSummary` 中提取方法描述 | 查找"框架"/"模型"/"算法"关键词，生成架构图（ASCII）或流程 |
| **Page 8-9: 实验结果** | `chineseSummary` 中提取性能数字 | 查找"提升X%"/"准确率X%"，生成对比表格 |
| **Page 10: 应用场景** | `field` + 常见应用 | 根据领域生成3个应用场景（金融/医疗/工业等） |
| **Page 11: 总结** | `innovationPoints.title` | 复用创新点标题作为贡献，生成启发和未来方向 |
| **Page 12: 致谢** | `title`, `authors` | 生成论文信息和链接 |

### 关键提取函数（伪代码）

```javascript
// 1. 提取背景信息
function extractBackground(chineseSummary) {
  const sentences = chineseSummary.split('。')
  const problem = sentences.slice(0, 2).join('。')  // 前2句

  // 查找"现有方法"相关描述
  const methodKeywords = ['现有方法', '传统方法', '以往研究']
  const limitations = findSentencesWith(chineseSummary, methodKeywords)

  return { problem, limitations }
}

// 2. 简化创新点描述
function simplifyInnovationPoint(description, maxLength = 30) {
  if (description.length <= maxLength) return description

  // 提取第1句
  const firstSentence = description.split('。')[0]
  return firstSentence.substring(0, maxLength - 3) + '...'
}

// 3. 生成对比表格
function generateComparisonTable(chineseSummary) {
  // 从摘要提取性能数字
  const numbers = extractNumbers(chineseSummary)  // 正则匹配"XX%"/"提升XX"

  return `
| 方法 | 指标1 | 指标2 |
|------|-------|-------|
| Baseline | ${numbers[0] || '85.0%'} | 0.78 |
| **本文方法** | **${numbers[1] || '92.0%'}** ✅ | **0.89** ✅ |
  `.trim()
}

// 4. 生成应用场景
function generateApplications(field) {
  const domainMap = {
    '自然语言处理': ['💬 智能客服', '📝 内容生成', '🔍 信息检索'],
    '计算机视觉': ['📷 图像识别', '🎥 视频分析', '🏥 医学影像'],
    '机器学习': ['📊 数据分析', '🤖 智能决策', '🔮 趋势预测'],
    // ... 更多领域
  }

  return domainMap[field] || ['应用场景1', '应用场景2', '应用场景3']
}
```

---

## 四、Markdown模板（可复制）

### 基础模板（12页）

```markdown
# {论文标题}
### {中文标题}

**作者**: {authors}
**发表**: {conference} {year}
**领域**: {field}

---

**汇报人**: 论导Lite AI生成
**日期**: {current_date}

---

## 汇报大纲

1. 🎯 **研究背景** - {背景一句话概括}
2. 💡 **核心创新** - {创新一句话概括}
3. 🔧 **技术方法** - {方法一句话概括}
4. 📊 **实验结果** - {结果一句话概括}
5. 🚀 **总结启发** - {启发一句话概括}

---

## 研究背景：问题是什么？

### 当前挑战
{从chineseSummary提取前1-2句}

### 为什么重要？
- **应用价值**: {生成}
- **理论意义**: {生成}
- **挑战难度**: {生成}

---

## 现有方法的局限

### 传统方法
- **方法A**: {描述} → ❌ {局限性}
- **方法B**: {描述} → ❌ {局限性}

### 核心矛盾
{一句话总结}

> **研究空白**: {本文要填补的gap}

---

## 核心创新：本文提出了什么？

### {innovationPoints[0].icon} {innovationPoints[0].title}
{innovationPoints[0].description简化版}

### {innovationPoints[1].icon} {innovationPoints[1].title}
{innovationPoints[1].description简化版}

### {innovationPoints[2].icon} {innovationPoints[2].title}
{innovationPoints[2].description简化版}

---

**关键区别**: {与已有方法的本质不同}

---

## 技术方法：如何实现？

### 整体框架

```
{ASCII架构图}
```

### 核心组件
- **模块A**: {功能描述}
- **模块B**: {功能描述}
- **模块C**: {功能描述}

---

## 关键技术：{核心算法/技术名称}

### 核心公式/算法

{如果有公式，展示1个最重要的}

{如果是算法，展示伪代码或流程}

---

## 实验结果：效果如何？

### 数据集
- **数据集1**: {规模/特点}
- **数据集2**: {规模/特点}

### 性能对比

| 方法 | 指标1 | 指标2 | 指标3 |
|------|-------|-------|-------|
| Baseline | X.X% | X.X | X.X |
| **本文方法** | **X.X%** ✅ | **X.X** ✅ | **X.X** ✅ |

**关键提升**: {对比baseline提升了多少}

---

## 深入分析

### 消融实验
{或其他分析}

| 配置 | 性能 |
|------|------|
| 完整模型 | X.X% |
| -模块A | X.X% ↓ |

---

## 应用场景（可选）

### {应用1图标} {应用1标题}
- {场景描述1}
- {场景描述2}

### {应用2图标} {应用2标题}
- {场景描述1}
- {场景描述2}

---

## 总结与启发

### 主要贡献
1. ✅ {innovationPoints[0].title}
2. ✅ {innovationPoints[1].title}
3. ✅ {innovationPoints[2].title}

### 局限性
- **{局限1}**: {描述}
- **{局限2}**: {描述}

### 对我们的启发
💡 {可借鉴的方法/思路}

### 未来方向
🔮 {可能的改进/扩展}

---

## Thank You!

### 论文信息
**标题**: {title}
**作者**: {authors}
**会议**: {conference}
**链接**: {arxiv_link}

---

### 欢迎讨论！

💬 如有问题，欢迎提出
📧 {其他信息}

---

*本PPT由论导Lite AI自动生成，符合15分钟组会汇报标准*
```

---

## 五、质量检查清单

生成PPT后，必须检查：

### 结构检查
- [ ] 总页数在10-13页
- [ ] 每页有明确标题（`#`或`##`）
- [ ] 使用`---`正确分隔幻灯片
- [ ] 第1页是封面，最后1页是致谢

### 内容检查
- [ ] 每页文字≤5行（核心内容）
- [ ] 每行文字≤30个中文字
- [ ] 表格≤4列
- [ ] 每页最多1个公式或代码块
- [ ] 创新点页独立且清晰可见

### 叙事检查
- [ ] 有"问题→方法→结果"完整流程
- [ ] 创新点页是整个PPT的重点
- [ ] 总结页呼应创新点

### 视觉检查
- [ ] 使用emoji或图标增强视觉
- [ ] 关键信息用**粗体**或✅标记
- [ ] 重要观点用引用块`>`突出

---

## 六、常见问题（FAQ）

### Q1: 如果创新点只有2个怎么办？
**A**: 可以从方法或结果中提炼第3个，或者只展示2个（保持页面简洁）。

### Q2: 如果摘要中没有明确的"现有方法"描述？
**A**: 根据领域常识生成通用描述，例如：
- NLP领域："传统方法依赖人工特征 → ❌ 泛化能力弱"
- CV领域："CNN模型计算成本高 → ❌ 难以实时部署"

### Q3: 如果摘要中没有性能数字？
**A**: 生成模拟数据（明确标注为"示例"），或用定性描述代替：
- "性能显著提升" 而非 "提升10%"

### Q4: 如何处理多模态论文（图像+文本）？
**A**: 架构图中体现多模态融合，应用场景页突出跨模态能力。

### Q5: 10页vs.12页如何选择？
**A**:
- **10页**: 方法简单、结果明确的论文
- **12页**: 复杂系统、多个实验、强调应用的论文

---

## 七、未来扩展方向

### Phase 2: 智能内容生成（Feature #005）

1. **后端API设计**
   ```javascript
   POST /api/generate_ppt_content
   Body: { paperId: "xxx" }  // 或 arxivId
   Response: {
     slides: [
       { type: "cover", title: "...", content: "..." },
       { type: "outline", title: "...", content: "..." },
       { type: "background", title: "...", content: "..." },
       // ... 10-13个slides
     ],
     metadata: { slideCount: 12, estimatedTime: "15min" }
   }
   ```

2. **LLM提示词模板**
   ```
   你是学术PPT生成专家。基于以下论文信息，生成符合15分钟组会汇报标准的PPT内容。

   论文标题：{title}
   中文摘要：{chineseSummary}
   创新点：{innovationPoints}

   要求：
   1. 总共10-13页
   2. 遵循5×5规则（每页≤5行，每行≤10中文字）
   3. 完整叙事结构（问题→方法→结果→意义）
   4. Markdown格式输出

   生成结构：...
   ```

3. **前端增强**
   - 实时预览生成过程
   - 支持用户编辑（修改标题、调整内容）
   - 导出为PPTX文件（使用pptxgenjs库）

---

**文档版本**: v1.0
**创建日期**: 2025-10-16
**状态**: ✅ 可直接用于开发
**参考**: 基于方案A的实践（demo-default, mock-task-001, mock-task-002）
