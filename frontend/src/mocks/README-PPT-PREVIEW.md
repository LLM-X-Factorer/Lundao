# PPT预览Mock数据使用指南

## 📚 概述

PPT预览功能使用**默认演示PPT回退机制**，确保任何completed状态的任务都能预览内容，无需为每个taskId单独配置mock数据。

---

## 🎯 实现逻辑

### 数据流

```
用户点击"预览"按钮
    ↓
uiStore.openPPTPreview(task.id)
    ↓
pptContentService.getPPTContent(taskId)
    ↓
getMockPPTContent(taskId)
    ↓
检查 mockPPTContents[taskId]
    ├─ 精确匹配 → 返回对应PPT
    ├─ null（失败任务） → 抛出错误
    └─ undefined（未匹配） → 返回 demo-default
```

### 回退策略（方案A）

```javascript
export function getMockPPTContent(taskId) {
  const content = mockPPTContents[taskId]

  // 1. 失败任务：抛出错误
  if (content === null) {
    throw new Error('该任务未成功生成PPT，无法预览')
  }

  // 2. 精确匹配：返回对应内容
  if (content !== undefined) {
    return content
  }

  // 3. 未匹配：回退到默认演示PPT
  console.log(`[Mock] taskId "${taskId}" 未找到精确匹配，使用默认演示PPT`)
  return mockPPTContents['demo-default']
}
```

---

## 📦 当前Mock数据

### 1. 默认演示PPT (`demo-default`)

**用途**: 通用演示内容，任何未匹配的taskId都会使用

**内容亮点**:
- ✅ 11页完整PPT
- ✅ LaTeX公式示例（行内 `$E=mc^2$` + 块级 `$$...$$`）
- ✅ Python代码高亮（快速排序算法）
- ✅ 性能对比表格
- ✅ 技术架构ASCII图
- ✅ Markdown引用块和嵌套列表
- ✅ 水印保护说明

**适用场景**:
- 产品演示
- 功能展示
- 新生成任务的临时预览
- 开发测试

### 2. 特定任务PPT

| taskId | 论文主题 | 页数 | 特点 |
|--------|---------|------|------|
| `mock-task-001` | Hierarchical Reasoning Models | 10 | 数学公式 + Python代码 |
| `mock-task-002` | OpenTSLM | 4 | 时间序列预测 |
| `mock-task-003` | Federated Learning | - | ❌ 失败任务（null） |

---

## 🎬 使用场景示例

### 场景1：已有历史任务

```javascript
// 用户点击 mock-task-001 的预览按钮
uiStore.openPPTPreview('mock-task-001')
// ✅ 显示：Hierarchical Reasoning Models（10页）
```

### 场景2：新生成的任务

```javascript
// 用户生成新任务，taskId为动态UUID
const newTaskId = 'mock-task-1737123456789-a3f8e9'
uiStore.openPPTPreview(newTaskId)
// ✅ 显示：论导Lite PPT预览功能演示（11页）
// 💡 控制台输出：[Mock] taskId "mock-task-..." 未找到精确匹配，使用默认演示PPT
```

### 场景3：失败任务

```javascript
// 用户点击 mock-task-003（failed状态）
uiStore.openPPTPreview('mock-task-003')
// ❌ 显示错误：该任务未成功生成PPT，无法预览
// ✅ 用户看到错误UI，可以选择"重试"
```

### 场景4：产品演示

```javascript
// 演示给客户或团队看
// 使用任意completed任务都能看到完整功能展示
uiStore.openPPTPreview('demo-任意ID')
// ✅ 显示演示PPT，展示所有功能（LaTeX、代码、表格等）
```

---

## 🔧 如何扩展

### 添加新的特定PPT

如果你想为某个特定论文添加定制PPT内容：

```javascript
// src/mocks/pptContentData.js

export const mockPPTContents = {
  'demo-default': { /* ... */ },
  'mock-task-001': { /* ... */ },
  'mock-task-002': { /* ... */ },

  // 新增特定PPT
  'mock-task-004': {
    taskId: 'mock-task-004',
    markdown: `# 你的论文标题
这是第一页内容

---

## 第二页标题
...`,
    metadata: {
      paperTitle: '你的论文标题',
      slideCount: 5,
      generatedAt: '2025-01-15T10:00:00.000Z',
      author: '作者名',
      field: '研究领域'
    }
  }
}
```

### 修改默认演示PPT

如果你想自定义演示内容：

```javascript
// 编辑 demo-default 的 markdown 字段
mockPPTContents['demo-default'].markdown = `# 你的演示标题
自定义演示内容...

---

## 第二页
...`
```

### 添加智能匹配（可选）

如果未来需要根据论文主题智能匹配演示PPT：

```javascript
export function getMockPPTContent(taskId) {
  const content = mockPPTContents[taskId]

  if (content === null) {
    throw new Error('该任务未成功生成PPT，无法预览')
  }

  if (content !== undefined) {
    return content
  }

  // 智能匹配逻辑（根据taskId或其他信息）
  if (taskId.includes('ml') || taskId.includes('machine-learning')) {
    return mockPPTContents['mock-task-001']  // 返回机器学习相关PPT
  }

  if (taskId.includes('time-series')) {
    return mockPPTContents['mock-task-002']  // 返回时间序列PPT
  }

  // 默认回退
  return mockPPTContents['demo-default']
}
```

---

## 📊 演示PPT完整内容

### 11页幻灯片结构

1. **封面页** - 论导Lite PPT预览功能介绍
2. **功能亮点** - LaTeX、代码高亮、Markdown、水印
3. **数学公式示例** - 行内公式、块级公式（傅里叶变换、泰勒级数）
4. **代码高亮示例** - Python快速排序算法
5. **数据可视化** - 性能对比表格、关键优势
6. **技术架构** - 系统组件ASCII图
7. **Markdown渲染示例** - 引用块、嵌套列表
8. **性能指标** - Bundle优化、安全防护
9. **使用场景** - 学术研究者、教育工作者、企业团队
10. **总结** - 功能亮点、立即体验
11. **致谢** - 功能特性说明

### 演示内容覆盖

- ✅ **LaTeX公式**: `$E=mc^2$`, `$$\mathcal{F}(\omega) = \int...$$`
- ✅ **代码高亮**: Python快速排序（完整实现）
- ✅ **表格**: 性能对比表（4列×4行）
- ✅ **引用块**: 用户评价
- ✅ **列表嵌套**: 使用流程（3步骤）
- ✅ **ASCII图**: 技术架构
- ✅ **Emoji**: 功能图标

---

## 🧪 测试建议

### 手动测试

1. **启动开发服务器**:
   ```bash
   npm run dev
   ```

2. **测试场景**:
   - [ ] 点击 mock-task-001 预览 → 应显示 Hierarchical Reasoning PPT
   - [ ] 点击 mock-task-002 预览 → 应显示 OpenTSLM PPT
   - [ ] 点击 mock-task-003 预览 → 应显示错误提示
   - [ ] 生成新任务后预览 → 应显示演示PPT
   - [ ] 检查演示PPT内容：
     - [ ] LaTeX公式正确渲染
     - [ ] Python代码有语法高亮
     - [ ] 表格格式正确
     - [ ] 水印显示在9个位置

### 控制台日志

在Mock模式下，当使用默认演示PPT时，控制台会输出：

```
[Mock] taskId "mock-task-xxx" 未找到精确匹配，使用默认演示PPT
```

这有助于调试和确认回退逻辑是否生效。

---

## 📝 环境配置

### 启用Mock模式

```bash
# .env.development
VITE_USE_MOCK_DATA=true  # 默认启用
```

### 切换到真实API

```bash
# .env.production
VITE_USE_MOCK_DATA=false  # 生产环境使用真实API
```

---

## 🎯 优势总结

### 用户体验
- ✅ **零配置**: 任何completed任务都能预览
- ✅ **演示友好**: 完整展示所有功能
- ✅ **错误处理**: Failed任务有明确错误提示

### 开发效率
- ✅ **无需维护**: 新任务自动回退到演示PPT
- ✅ **易于扩展**: 只需添加特定taskId映射
- ✅ **调试方便**: 控制台日志显示匹配状态

### 代码质量
- ✅ **架构简洁**: 保持现有流程不变
- ✅ **向后兼容**: 现有特定PPT仍正常工作
- ✅ **性能影响**: 仅+3KB bundle size

---

## 🚀 未来增强方向

### Phase 2 (可选)

1. **多套演示PPT**:
   - `demo-default`: 通用演示
   - `demo-academic`: 学术研究主题
   - `demo-tech`: 技术类主题
   - `demo-business`: 商业应用主题

2. **智能匹配**:
   - 根据论文标题/领域自动选择最匹配的演示PPT
   - 根据taskId模式（如`ml-*`, `cv-*`）智能路由

3. **动态生成**:
   - 基于论文metadata动态生成演示PPT
   - 使用模板+占位符系统

4. **A/B测试**:
   - 随机展示不同版本的演示PPT
   - 收集用户反馈数据

---

## 📞 联系方式

如有问题或建议，请：
- 查看主README: `/README.md`
- 查看Feature #004文档: `/specs/004-ppt-preview-feature/README.md`
- 查看Mock系统文档: `/src/mocks/README.md`

---

**最后更新**: 2025-10-16
**功能状态**: ✅ 已完成并测试
**相关Commit**: `efe1277` - feat(mock): add universal demo PPT for preview feature
