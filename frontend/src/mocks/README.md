# Mock 数据使用说明

## 概述

此目录包含用于开发和演示的 mock 数据。当后端服务不可用时，前端可以使用这些 mock 数据进行开发和测试。

## Mock 数据特点

### 真实性
- 基于 2025年1月 arXiv 真实热门研究主题
- 包含真实的研究领域和关键词
- 模拟真实的论文元数据结构

### 覆盖范围
- **每日热门** (dailyPapers): 8篇最新论文
- **每周热门** (weeklyPapers): 8篇一周内热门论文
- **每月热门** (monthlyPapers): 8篇一月内热门论文

### 研究主题
涵盖以下热门领域：
- 多模态视觉语言模型
- 小规模递归推理
- 时间序列语言模型
- 强化学习与可验证奖励
- 多智能体协作
- 联邦学习
- 量子机器学习
- AI伦理

## Mock 系统架构

### 论文发现 Mock (Feature #001)
- `paperData.js`: 24篇真实研究论文数据
- 自动生成中文分析和创新点
- 模拟 500ms 网络延迟

### PPT 任务 Mock (Feature #003)
- `taskData.js`: 3个历史任务（2完成 + 1失败）
- `taskService.js`: 任务创建和状态轮询模拟
- `utils.js`: Mock 工具函数（ID生成、延迟模拟）

## 使用方法

### 启用 Mock 模式

在 `.env.development` 文件中设置：
```bash
# Enable mock data for PPT tasks and paper analysis
VITE_USE_MOCK_DATA=true
```

### 禁用 Mock 模式（使用真实 API）

在 `.env.development` 文件中设置：
```bash
VITE_USE_MOCK_DATA=false
```

**注意**: 修改环境变量后需要重启开发服务器才能生效。

## 数据结构

### Paper 对象
```javascript
{
  id: String,              // 论文唯一标识
  title: String,           // 论文标题
  authors: Array<String>,  // 作者列表
  abstract: String,        // 摘要
  arxivId: String,         // arXiv ID
  field: String,           // 研究领域
  keywords: Array<String>, // 关键词
  publicationDate: String, // 发布日期 (ISO 8601)
  pdfUrl: String,          // PDF 下载链接
  arxivUrl: String,        // arXiv 页面链接
  source: 'arxiv'          // 来源
}
```

### Analysis 对象
```javascript
{
  paperId: String,              // 关联的论文ID
  chineseSummary: String,       // 中文摘要
  innovationPoints: Array<String>, // 创新点列表
  analysisTimestamp: String,    // 分析时间戳
  analysisStatus: 'completed',  // 分析状态
  errorMessage: null            // 错误信息
}
```

### PPT Task 对象
```javascript
{
  id: String,               // 任务ID (格式: mock-task-{timestamp}-{random})
  paperId: String,          // 关联论文ID
  paperTitle: String,       // 论文标题
  status: String,           // 任务状态: queued | generating | completed | failed
  createdAt: String,        // 创建时间 (ISO 8601)
  completedAt: String|null, // 完成时间 (ISO 8601)
  downloadUrl: String|null, // 下载链接 (/mock/downloads/{taskId}.pptx)
  progress: Number|null,    // 进度 (0-100)
  errorMessage: String|null,// 错误信息
  retryCount: Number        // 重试次数
}
```

## Mock 数据生成

### 自动生成分析数据
使用 `generateMockAnalysis(paper)` 函数可以为任何论文自动生成中文分析：

```javascript
import { generateMockAnalysis } from '@/mocks/paperData'

const analysis = generateMockAnalysis(paper)
```

该函数会根据论文的研究领域自动生成：
- 中文摘要（基于标题和关键词）
- 3个创新点
- 完整的分析元数据

## PPT 任务 Mock 系统

### 状态进度模拟
PPT 任务自动经历以下状态转换（总时长15秒）：

```
┌──────────────────────────────────────────────────┐
│         任务生命周期 (15秒)                        │
└──────────────────────────────────────────────────┘

时间:      0s           5s                   15s
           │            │                     │
           ▼            ▼                     ▼
       ┌──────┐     ┌─────────┐         ┌─────────┐
       │ 排队中│────>│ 生成中   │────────>│ 已完成   │
       └──────┘     └─────────┘         └─────────┘
         │              │                    │
    进度: null     进度: 0-90%           进度: 100%
    下载: null     下载: null           下载: /mock/...
```

### 状态计算机制
- **0-5秒**: `queued` 状态，进度为null
- **5-15秒**: `generating` 状态，进度线性增长 0-90%
- **15秒后**: `completed` 状态，进度100%，提供下载链接

### 页面刷新处理
- 刷新页面会清空内存中的任务创建时间记录
- 所有 `queued` 或 `generating` 状态的任务自动标记为 `failed`
- 错误信息: "页面刷新导致任务中断 (Mock模式)"

### Mock 任务 ID 格式
- **动态创建**: `mock-task-{timestamp}-{random6chars}`
  - 示例: `mock-task-1705300123456-a3f8e9`
- **历史任务**: `mock-task-{nnn}` (三位数字)
  - 示例: `mock-task-001`, `mock-task-002`

### 历史任务数据
首次启动 Mock 模式时，系统会自动加载3个历史任务：
- 2个已完成任务（可下载）
- 1个失败任务（可重试）

## 性能特性

### 模拟延迟
- 论文列表加载: 500ms
- 论文分析加载: 800ms
- PPT 任务创建: 500ms
- 任务状态轮询: 300ms

这些延迟模拟真实 API 调用，确保开发时能够测试加载状态和骨架屏。

### 分页支持
Mock 数据支持分页功能：
- 每页 8 篇论文
- 自动计算总页数
- 支持页面跳转

## 切换到生产环境

当后端 API 准备就绪时：

1. 在 `.env.production` 中设置：
   ```bash
   # IMPORTANT: Never enable mock mode in production
   VITE_USE_MOCK_DATA=false
   VITE_API_BASE_URL=https://api.lundao.com/api
   ```

2. 前端代码无需修改，会自动切换到真实 API

### Mock/真实任务共存
- Mock 任务 ID 以 `mock-task-` 开头
- 真实任务 ID 为 UUID 格式
- 两种任务可以在 localStorage 中共存
- 下载按钮会自动识别并处理 Mock 任务（显示提示而非下载）

## SpecKit 最佳实践

此 mock 实现遵循 SpecKit 最佳实践：

✅ **分离关注点**: Mock 数据独立于业务逻辑
✅ **环境驱动**: 通过环境变量控制行为
✅ **真实数据**: 基于真实研究主题，提供真实的开发体验
✅ **零修改切换**: 前后端集成时无需修改代码
✅ **文档完善**: 提供清晰的使用说明

## 维护说明

### 更新 Mock 数据
定期更新 mock 数据以反映最新的研究趋势：

1. 使用 WebSearch 搜索最新的 arXiv 热门论文
2. 更新 `paperData.js` 中的论文列表
3. 保持数据结构与后端 API 契约一致

### 数据质量
确保 mock 数据：
- 字段完整（所有必需字段都有值）
- 格式正确（日期、ID 等格式符合规范）
- 内容真实（基于实际研究主题）
- 多样化（覆盖不同领域和类型）
