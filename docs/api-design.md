# Lundao — API 设计

> Phase 1 产物。把后端现有的同步大端点 `POST /api/v1/process` 拆成 6 个**异步任务**端点，与前端已实现的 service 模块一致。Phase 2 后端按此实现。

## 1. 整体原则

### 1.1 为什么改？

后端现状是单一同步端点：
```
POST /api/v1/process   →   阻塞 5–7 分钟   →   一次性返回全部产物
```

问题：
- HTTP 长连接易被 Nginx/CDN/浏览器 60–300s 超时杀掉
- 用户无法看到中间进度
- 一次失败要全跑一遍
- 前端已实现的是 6 个分步端点 + 5s 轮询，没法对接

### 1.2 新的模型

```
GET  /api/arxiv_papers      ←  浏览热门论文（24h 缓存）
POST /api/upload_pdf        ←  上传 PDF，得到 fileId
GET  /api/analyze_paper     ←  AI 中文分析（可 202 异步）
POST /api/generate_ppt      ←  创建生成任务，立刻返回 taskId
GET  /api/task_status       ←  前端 5s 轮询查进度
GET  /api/ppt_content       ←  完成后取 PPT 预览内容
```

任务生命周期：`queued → generating → completed | failed`，由后端 SQLite 表 + asyncio 任务队列驱动。

## 2. 公共约定

| 项 | 值 |
|---|---|
| Base URL（dev） | `http://localhost:8000/api` |
| Base URL（prod） | `https://api.lundao.example/api` |
| API 版本 | URL 不含版本号；如需要 breaking change，新版本走 `/api/v2/...` |
| 请求内容类型 | `application/json`；上传 PDF 用 `multipart/form-data` |
| 响应内容类型 | `application/json` |
| CORS | 开发期 `allow_origins=["*"]`；生产期白名单 |
| 字段命名 | **camelCase**（与前端 JS 一致）。Pydantic 用 `alias_generator=to_camel` + `populate_by_name=True` |
| 时间戳 | ISO 8601 UTC（`2026-05-11T08:00:00.000Z`） |
| ID 风格 | 任务 ID = UUIDv4；文件 ID = UUIDv4；论文 ID = `{period}-{4位序号}`（如 `daily-0001`，与前端 mock 一致） |

### 2.1 统一错误响应

非 2xx 响应均为：

```json
{
  "error": {
    "code": "PAPER_NOT_FOUND",
    "message": "Paper with arxivId 2501.99999 not found",
    "details": { "arxivId": "2501.99999" }
  }
}
```

`code` 是稳定枚举（前端拿来分支），`message` 是人读的，`details` 可空。

### 2.2 速率限制

- arXiv 上游有 3 秒/请求的硬限制 → 后端 `/api/arxiv_papers` 做 24h 缓存
- Gemini / Gamma 上游配额由后端集中管理（429 转 502 `UPSTREAM_RATE_LIMITED`）
- 本身的 API 不强制限流，但 `/api/task_status` 建议前端 ≥ 5s 间隔

## 3. 数据模型

### 3.1 `Paper`

```json
{
  "id": "daily-0001",
  "title": "Addressing Corner Cases in Autonomous Driving...",
  "authors": ["Haicheng Liao", "Bonan Wang", "..."],
  "abstract": "We introduce WM-MoE, a framework...",
  "arxivId": "2510.21867",
  "uploadedFileId": null,
  "field": "Computer Vision",
  "keywords": ["autonomous driving", "world models"],
  "publicationDate": "2024-10-29",
  "pdfUrl": "https://arxiv.org/pdf/2510.21867.pdf",
  "arxivUrl": "https://arxiv.org/abs/2510.21867",
  "source": "arxiv"
}
```

- `id`：列表里的稳定标识，发现接口和分析接口都用它
- `source`: `"arxiv"` | `"upload"`（前端目前只见过 `"arxiv"`）
- `uploadedFileId` 与 `arxivId` 互斥：源自 arXiv 的 `arxivId` 必填，源自上传的 `uploadedFileId` 必填

### 3.2 `Analysis`

```json
{
  "paperId": "daily-0001",
  "chineseSummary": "本研究聚焦于...",
  "innovationPoints": [
    {
      "icon": "🚀",
      "iconLabel": "Performance breakthrough",
      "title": "27M参数超越大型LLM",
      "description": "在Sudoku和ARC-AGI等硬推理任务上..."
    }
  ],
  "analysisTimestamp": "2026-05-11T08:00:00.000Z",
  "analysisStatus": "completed",
  "errorMessage": null
}
```

- `innovationPoints` 支持**两种格式**（前端有 backward compat）：
  - 新：`Array<{ icon, iconLabel, title, description }>`（前端 v0.2 起的格式）
  - 旧：`Array<string>`（仅纯文本，前端会自动包装显示）
  - **后端必须返回新格式**，旧格式只是为了允许其他来源数据
- `analysisStatus`: `"completed"` | `"pending"` | `"failed"`
- `errorMessage` 仅在 `analysisStatus="failed"` 时非空

### 3.3 `PPTTask`

```json
{
  "id": "f7a8b2c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "paperId": "daily-0001",
  "paperTitle": "Hierarchical Reasoning Models: ...",
  "status": "completed",
  "createdAt": "2026-05-11T08:00:00.000Z",
  "completedAt": "2026-05-11T08:03:15.000Z",
  "progress": 100,
  "downloadUrl": "/api/ppt_download?taskId=f7a8b2c1-...",
  "errorMessage": null,
  "retryCount": 0
}
```

- `status`: `"queued" | "generating" | "completed" | "failed"`
- `progress`：0–100，`queued` 时为 `null`，`completed` 时为 `100`
- `downloadUrl`：`completed` 时可下载；后端可返回相对路径或绝对 URL；为空表示 PPT 文件尚未导出（如 Gamma 失败但 P2/P3/P4 成功）

### 3.4 `PPTContent`

后端可任选一种格式返回，前端两种都支持：

**Markdown 模式**（适合 prompt 直出的场景）：
```json
{
  "taskId": "f7a8b2c1-...",
  "paperId": "daily-0001",
  "type": "markdown",
  "markdown": "# 标题\n\n---\n\n## 第二页\n\n$$E = mc^2$$\n\n---\n\n...",
  "totalSlides": 14,
  "metadata": {
    "paperTitle": "Hierarchical Reasoning Models: ...",
    "generatedAt": "2026-05-11T08:03:15.000Z",
    "author": "...",
    "field": "..."
  }
}
```

**Images 模式**（Gamma 导出 PDF 后切图，或 Feature #006 风格）：
```json
{
  "taskId": "f7a8b2c1-...",
  "paperId": "daily-0001",
  "type": "images",
  "slides": [
    "/api/ppt_image?taskId=f7a8b2c1-...&slide=1",
    "/api/ppt_image?taskId=f7a8b2c1-...&slide=2"
  ],
  "totalSlides": 14,
  "metadata": { /* 同上 */ }
}
```

约定：
- `markdown` 模式下，`---` 是幻灯片分隔符（与 Gamma 一致），`totalSlides` 是 `---` 分隔后段数
- `images` 模式下，`slides[i]` 是第 `i+1` 张幻灯片的图片 URL；前端只渲染，不再切割

## 4. 端点详情

### 4.1 `GET /api/arxiv_papers`

拉取 trending 论文列表。后端代理 arXiv API + LLM 中文摘要 + 24h SQLite 缓存。

**Query 参数**：

| 名 | 类型 | 必填 | 默认 | 取值 |
|---|---|---|---|---|
| `period` | string | 否 | `daily` | `daily` \| `weekly` \| `monthly` |
| `page` | int | 否 | `1` | ≥1 |
| `limit` | int | 否 | `20` | 1–50 |

**响应 200**：
```json
{
  "papers": [ /* Paper[] */ ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "totalCount": 100,
    "totalPages": 5
  },
  "cachedAt": "2026-05-11T07:00:00.000Z"
}
```

**错误**：
- `502 UPSTREAM_ERROR` — arXiv API 不可用
- `429 RATE_LIMITED` — 触发上游限流

**实现注**：Phase 2 加 `src/services/arxiv_client.py`。缓存键 `(period, page, limit)`，TTL 24h。**LLM 中文摘要在 list 端点不生成，按需通过 `/analyze_paper` 才生成**（节省 token）。

---

### 4.2 `POST /api/upload_pdf`

上传 PDF，得到 `fileId`，后续以 `fileId` 替代 `arxivId`。

**Body**：`multipart/form-data` 包含 `file` 字段（PDF 二进制）

**约束**：
- Content-Type 必须是 `application/pdf`
- 大小 ≤ 20 MB
- 文件名 UTF-8，长度 ≤ 255

**响应 200**：
```json
{
  "fileId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "paper.pdf",
  "fileSize": 1234567,
  "uploadedAt": "2026-05-11T08:00:00.000Z"
}
```

**错误**：
- `400 BAD_REQUEST_NO_FILE` — 没有 `file` 字段
- `413 PAYLOAD_TOO_LARGE` — 超过 20 MB
- `415 UNSUPPORTED_MEDIA_TYPE` — 非 PDF

**实现注**：上传后存 `uploads/{fileId}.pdf`，记录到 SQLite `uploads` 表（含 mime、size、md5）。文件 24 小时未关联任务自动清理。

---

### 4.3 `GET /api/analyze_paper`

返回某篇论文的 AI 中文分析。**`arxivId` 和 `fileId` 二选一**。

**Query 参数**：

| 名 | 类型 | 互斥组 |
|---|---|---|
| `arxivId` | string | A |
| `fileId` | string | A |

**响应 200**：完整 `Analysis` 对象（见 3.2）

**响应 202**（分析进行中，前端会按 `Retry-After` 重试，最多 3 次）：
```json
{
  "paperId": "daily-0001",
  "analysisStatus": "pending",
  "retryAfter": 5
}
```
- HTTP 头：`Retry-After: 5`

**错误**：
- `400 BAD_REQUEST_INVALID_PARAM` — 两个 ID 都没传 / 都传了
- `404 PAPER_NOT_FOUND` / `404 FILE_NOT_FOUND`
- `502 UPSTREAM_ERROR` — Gemini 失败

**实现注**：
- 同样走 SQLite 缓存（key = `arxivId` 或 `fileId`），命中即返回
- 缓存未命中：触发后台 LLM 调用，立即返回 202；下次调用如完成则 200
- LLM prompt 复用 backend/docs/Prompt-*.md 里某个简化版（生成 `chineseSummary` + 3 个 `innovationPoints`）

---

### 4.4 `POST /api/generate_ppt`

创建一个 PPT 生成任务，**立刻**返回 `taskId`。

**Body**（二选一）：
```json
{ "arxivId": "2510.21867" }
```
或
```json
{ "fileId": "550e8400-e29b-..." }
```

**响应 202**：
```json
{
  "taskId": "f7a8b2c1-...",
  "status": "queued",
  "createdAt": "2026-05-11T08:00:00.000Z"
}
```

**错误**：
- `400 BAD_REQUEST_INVALID_PARAM` — 两个 ID 都没传 / 都传了
- `404 PAPER_NOT_FOUND` / `404 FILE_NOT_FOUND`
- `429 TOO_MANY_TASKS` — 后端任务队列已满（保护性限流）

**实现注**：
- 在 SQLite `tasks` 表插入一行，状态 `queued`
- 把 taskId 推到 `asyncio.Queue`，后台 worker 取出后跑现有 LangGraph workflow
- Worker 数量按 `MAX_CONCURRENT_TASKS` 配置（默认 2）

---

### 4.5 `GET /api/task_status`

前端 5s 轮询此端点查询任务进度。

**Query 参数**：

| 名 | 类型 | 必填 |
|---|---|---|
| `taskId` | string | 是 |

**响应 200**：完整 `PPTTask` 对象（见 3.3）

**错误**：
- `404 TASK_NOT_FOUND`

**实现注**：
- 状态/进度直接读 SQLite，不触发任何重操作
- `progress` 字段在 `generating` 阶段由 worker 写入（按工作流节点完成度估算：execute_p1=20%, p2=40%, p3=60%, p4=80%, finalize=100%）

---

### 4.6 `GET /api/ppt_content`

任务完成后，拿可预览的内容（markdown 或 images）。

**Query 参数**：

| 名 | 类型 | 必填 |
|---|---|---|
| `taskId` | string | 是 |

**响应 200**：`PPTContent` 对象（见 3.4），`type` 字段决定模式

**错误**：
- `404 TASK_NOT_FOUND`
- `409 TASK_NOT_COMPLETED` — 任务还未到 `completed`
- `410 CONTENT_GONE` — 任务完成超过 7 天，文件已清理

**实现注**：
- 短期返回 `markdown` 模式（P1 工作流产物即 markdown）
- 中期增加 `images` 模式（用 pdf2image 把 Gamma 导出的 PDF 切图）

---

### 4.7 配套小端点

- `GET /api/health` — 健康检查，返回 `{ status: "ok", version: "0.2.0" }`
- `GET /api/ppt_download?taskId=...` — 下载 PPT 文件（PDF/PPTX）。响应 `Content-Disposition: attachment; filename="..."`
- `GET /api/ppt_image?taskId=...&slide=N` — 取第 N 张幻灯片图片（用于 `images` 模式）

## 5. 任务生命周期

```
                  ┌────────────────────┐
   POST /generate │       queued       │
   ─────────────→ │  (排队中，未开始)   │
                  └─────────┬──────────┘
                            │  worker 取走
                            ▼
                  ┌────────────────────┐
                  │     generating     │
                  │ progress 0 → 100   │
                  └─────┬──────────┬───┘
                        │          │
                  全部成功         任一致命错误
                        │          │
                        ▼          ▼
                  ┌──────────┐ ┌──────────┐
                  │completed │ │  failed  │
                  └──────────┘ └──────────┘
                       ▲
                       └── 容忍非致命错误（如 Gamma 失败但 P2-P4 成功），
                           成功标志按"P1 必须成功"判定，其余存到 errors 字段
```

**状态转移规则**：
- 状态只能前进，不能回退
- `failed` 是终态，不能恢复（前端可点"重试"，但那是创建新任务）
- `completed` 后 7 天自动归档输出文件（保留任务元数据）

## 6. 错误码总表

| HTTP | `code` | 含义 | 触发场景 |
|---|---|---|---|
| 400 | `BAD_REQUEST_INVALID_PARAM` | 参数缺失/冲突 | 必填项缺失、二选一冲突 |
| 400 | `BAD_REQUEST_NO_FILE` | 上传缺 file 字段 | `/upload_pdf` |
| 404 | `PAPER_NOT_FOUND` | arxivId 找不到 | 大部分 paper 端点 |
| 404 | `FILE_NOT_FOUND` | fileId 找不到（含已过期） | `/analyze_paper`、`/generate_ppt` |
| 404 | `TASK_NOT_FOUND` | taskId 找不到 | `/task_status`、`/ppt_content` |
| 409 | `TASK_NOT_COMPLETED` | 任务未完成就取内容 | `/ppt_content` |
| 410 | `CONTENT_GONE` | 内容已过期清理 | `/ppt_content` 在归档后 |
| 413 | `PAYLOAD_TOO_LARGE` | 超过 20 MB | `/upload_pdf` |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | 非 PDF | `/upload_pdf` |
| 429 | `RATE_LIMITED` | 触发本服务限流 | 罕见 |
| 429 | `TOO_MANY_TASKS` | 任务队列满 | `/generate_ppt` |
| 500 | `INTERNAL_ERROR` | 未捕获异常 | 兜底 |
| 502 | `UPSTREAM_ERROR` | 上游服务（arXiv/Gemini/Gamma）失败 | 所有依赖外部 API 的端点 |
| 503 | `SERVICE_UNAVAILABLE` | 服务在启动/关闭 | 维护期 |

特殊：

| HTTP | `code`（在 body） | 含义 |
|---|---|---|
| 202 | `analysisStatus: "pending"` | 分析进行中，前端按 `Retry-After` 重试 |
| 202 | `status: "queued"` | 任务已创建排队中 |

## 7. 端点 vs 现状对比表

| 端点 | 现状 | Phase 2 要做的事 |
|---|---|---|
| `GET /api/arxiv_papers` | ❌ 不存在 | 新增 `src/services/arxiv_client.py` + 缓存表 |
| `POST /api/upload_pdf` | ❌ 不存在 | 新增端点 + `uploads/` 目录 + SQLite `uploads` 表 |
| `GET /api/analyze_paper` | ❌ 不存在 | 新增简化 prompt 走 Gemini + SQLite 缓存 |
| `POST /api/generate_ppt` | ⚠️ 部分（旧的 `/process` 同步） | 拆为创建任务 + 后台 worker |
| `GET /api/task_status` | ❌ 不存在 | 新增端点 + SQLite `tasks` 表 |
| `GET /api/ppt_content` | ❌ 不存在 | 新增端点 + 读 `outputs/{taskId}/` |
| `GET /api/ppt_download` | ❌ 不存在 | 新增端点 |
| `GET /api/health` | ✅ 已有 `/api/v1/health` | 改路径：`/api/v1/health` → `/api/health` |
| `POST /api/v1/process` | ✅ 已有 | **删除**或保留为兼容（推荐删，未发布过） |

## 8. 与前端的对齐

前端 `src/api/*Service.js` 5 个 service 模块的现有签名**保持不变**，本设计的字段名/路径完全对得上，前端只需把 `VITE_USE_MOCK_DATA=false` 切到真实 API 即可。

具体 mapping：

| 前端 service 函数 | 对应端点 |
|---|---|
| `fetchArxivPapers(period, page, limit)` | `GET /api/arxiv_papers` |
| `analyzePaper(paperId, isArxiv)` | `GET /api/analyze_paper` |
| `uploadPDF(file, onProgress)` | `POST /api/upload_pdf` |
| `createPPTTask(paperId, isArxiv)` | `POST /api/generate_ppt` |
| `pollTaskStatus(taskId)` | `GET /api/task_status` |
| `getPPTContent(taskId)` | `GET /api/ppt_content` |

## 9. Phase 2 实施清单

后端工作量按优先级：

1. **基础设施**
   - [ ] 加 `src/db/` 模块：SQLite + alembic 迁移 + 三张表（`tasks`、`papers_cache`、`uploads`）
   - [ ] 加 `src/services/task_queue.py`：asyncio.Queue + 后台 worker
   - [ ] FastAPI app 改 `lifespan` 启动 worker、关闭时优雅退出

2. **路由重构**
   - [ ] 删除 `/api/v1/` 前缀，改用 `/api/`
   - [ ] 新增 6 个端点（4.1–4.6）+ 3 个配套小端点（4.7）
   - [ ] 统一 `error` 包装中间件
   - [ ] Pydantic schemas 加 `alias_generator=to_camel`

3. **arXiv 集成**
   - [ ] `src/services/arxiv_client.py` — 调 arXiv API + parser
   - [ ] 24h SQLite 缓存

4. **任务队列接入现有 workflow**
   - [ ] `generate_ppt` 端点把 taskId 推队列
   - [ ] worker 调用 `run_workflow()`，逐节点写 `progress` 到 SQLite
   - [ ] 输出文件落到 `outputs/{taskId}/`

5. **PPT 内容服务**
   - [ ] `/ppt_content` 默认返回 markdown 模式
   - [ ] `/ppt_download` 流式返回 PDF/PPTX

预计工作量：1.5–2 天（不含测试）。

---

*Last updated: 2026-05-11. Next phase: backend implementation per this contract.*
