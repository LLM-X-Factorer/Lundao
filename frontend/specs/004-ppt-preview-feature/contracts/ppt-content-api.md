# API Contract: PPT Content Retrieval

## Endpoint

```
GET /api/ppt_content
```

## Purpose

获取已完成的PPT任务的Markdown源内容，用于前端预览功能。

---

## Request

### Query Parameters

| 参数名 | 类型 | 必需 | 描述 | 示例 |
|--------|------|------|------|------|
| `taskId` | string | ✅ Yes | PPT任务的唯一标识符（UUID格式） | `550e8400-e29b-41d4-a716-446655440000` |

### Headers

| Header | 值 | 必需 | 描述 |
|--------|-----|------|------|
| `Accept` | `application/json` | ✅ Yes | 指定响应格式 |

### Request Example

```bash
GET /api/ppt_content?taskId=550e8400-e29b-41d4-a716-446655440000
Host: api.lundao.com
Accept: application/json
```

---

## Response

### Success Response (200 OK)

**场景**: 任务存在且已完成，内容成功获取

**Response Body**:

```json
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "markdown": "# Hierarchical Reasoning Models\n小规模递归推理超越大语言模型\n\n---\n\n## 研究背景\n\n### 当前挑战\n- 大语言模型（LLM）在复杂推理任务上表现受限\n- 计算成本高昂...",
  "metadata": {
    "paperTitle": "Hierarchical Reasoning Models: Small-Scale Recursive Reasoning Outperforms LLMs",
    "slideCount": 8,
    "generatedAt": "2025-01-15T10:03:15.000Z",
    "author": "Chen et al.",
    "field": "机器学习"
  }
}
```

**字段说明**:

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `taskId` | string | ✅ Yes | 任务UUID，与请求参数一致 |
| `markdown` | string | ✅ Yes | PPT内容的Markdown源码，使用 `---` 作为幻灯片分隔符 |
| `metadata` | object | ✅ Yes | PPT元数据 |
| `metadata.paperTitle` | string | ✅ Yes | 论文完整标题 |
| `metadata.slideCount` | number | ✅ Yes | 幻灯片页数 |
| `metadata.generatedAt` | string | ✅ Yes | PPT生成完成时间（ISO 8601格式） |
| `metadata.author` | string | ❌ No | 论文作者（可选） |
| `metadata.field` | string | ❌ No | 研究领域（可选） |

**Markdown格式规范**:

1. **幻灯片分隔符**: 使用独立行的 `---` 分割不同幻灯片
2. **标题层级**:
   - `#` (H1): 幻灯片主标题
   - `##` (H2): 二级标题
   - `###` (H3): 三级标题
3. **支持元素**:
   - 列表（有序/无序）
   - 表格
   - 代码块
   - 引用块
   - 强调（粗体/斜体）
4. **字符编码**: UTF-8

**示例Markdown结构**:

```markdown
# 第一页标题

这是第一页的内容

---

## 第二页标题

### 子标题

- 要点1
- 要点2

---

## 第三页标题

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |
```

---

### Error Responses

#### 400 Bad Request

**场景**: 请求参数无效

```json
{
  "error": "InvalidRequest",
  "message": "taskId参数缺失或格式不正确",
  "details": {
    "taskId": "必须是有效的UUID格式"
  }
}
```

---

#### 403 Forbidden

**场景**: 任务未完成，无法预览

```json
{
  "error": "TaskNotCompleted",
  "message": "该任务尚未完成，无法预览内容",
  "details": {
    "taskId": "550e8400-e29b-41d4-a716-446655440000",
    "currentStatus": "generating"
  }
}
```

---

#### 404 Not Found

**场景**: 任务不存在或已过期

```json
{
  "error": "TaskNotFound",
  "message": "任务不存在或内容已过期",
  "details": {
    "taskId": "550e8400-e29b-41d4-a716-446655440000",
    "suggestion": "内容保留期为24小时，请及时下载"
  }
}
```

---

#### 500 Internal Server Error

**场景**: 服务器内部错误

```json
{
  "error": "ContentGenerationFailed",
  "message": "PPT内容生成或读取失败",
  "details": {
    "taskId": "550e8400-e29b-41d4-a716-446655440000",
    "internalError": "Storage service unavailable"
  }
}
```

---

#### 503 Service Unavailable

**场景**: 服务暂时不可用

```json
{
  "error": "ServiceUnavailable",
  "message": "服务暂时不可用，请稍后重试",
  "retryAfter": 30
}
```

**Headers**:
```
Retry-After: 30
```

---

## Security Considerations

### 1. 认证与授权
- **当前版本**: 无需认证（符合MVP零摩擦原则）
- **未来版本**: 如引入用户系统，需验证taskId所有权

### 2. 速率限制
- **建议**: 每IP每分钟最多10次请求
- **超限响应**: 429 Too Many Requests

### 3. 数据保护
- **传输**: HTTPS强制加密
- **存储**: Markdown内容不包含敏感信息
- **过期策略**: 内容保留24小时后自动删除

### 4. 输入验证
- **taskId**: 严格验证UUID格式，拒绝注入攻击
- **长度限制**: taskId长度限制36-50字符

---

## Performance Requirements

| 指标 | 目标值 | 测量方法 |
|------|--------|---------|
| 响应时间 (P95) | < 500ms | 服务端日志 |
| 吞吐量 | > 100 req/s | 负载测试 |
| 可用性 | 99.5% | 监控系统 |

---

## Versioning

- **当前版本**: v1
- **版本策略**: URL路径版本化（如需变更API格式，使用 `/api/v2/ppt_content`）
- **向后兼容**: v1版本至少支持6个月

---

## Frontend Integration

### Mock Mode Implementation

```javascript
// src/api/pptContentService.js
import { getMockPPTContent } from '@/mocks/pptContentData'

export async function getPPTContent(taskId) {
  if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
    await new Promise(resolve => setTimeout(resolve, 500)) // 模拟网络延迟
    return getMockPPTContent(taskId)
  }

  const response = await apiClient.get('/ppt_content', {
    params: { taskId }
  })
  return response.data
}
```

### Error Handling

```javascript
try {
  const content = await getPPTContent(taskId)
  // 使用content.markdown和content.metadata
} catch (error) {
  if (error.response?.status === 404) {
    showToast('PPT内容已过期', 'error')
  } else if (error.response?.status === 403) {
    showToast('任务尚未完成', 'warning')
  } else {
    showToast('加载失败，请重试', 'error')
  }
}
```

---

## Change Log

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2025-01-15 | 初始版本，定义基础契约 |

---

## Related Endpoints

- `POST /api/generate_ppt` - 创建PPT生成任务
- `GET /api/task_status` - 轮询任务状态
- `GET /api/download_ppt` - 下载PPT文件（二进制）

---

## Questions & Answers

**Q: 为什么使用Markdown而非直接返回HTML？**
A: Markdown作为中间格式更灵活，前端可根据需要定制渲染样式，且体积更小（约50%节省）。

**Q: 幻灯片数量有限制吗？**
A: 建议单个PPT不超过20页，Markdown内容不超过50KB。

**Q: 是否支持图片和多媒体？**
A: MVP版本暂不支持，未来可通过图片URL嵌入（`![alt](url)`）。

**Q: 内容更新后如何通知前端？**
A: 当前为一次性生成，不支持更新。如需重新生成，请创建新任务。

---

**文档版本**: 1.0
**最后更新**: 2025-01-15
**维护者**: 论导Lite团队
