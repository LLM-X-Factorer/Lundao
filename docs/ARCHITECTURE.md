# Lundao — 系统架构

## 全景图

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Browser (User)                              │
│  Vue 3 SPA — paper discovery, upload, task tracking, PPT preview     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │  REST + 5s polling
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Backend (FastAPI)                              │
│                                                                      │
│  ┌────────────────┐  ┌──────────────────┐  ┌──────────────────────┐ │
│  │  arXiv Proxy   │  │  Task Queue      │  │  LangGraph Workflow  │ │
│  │  + 24h cache   │  │  (asyncio + SQL) │  │  P1 → P2/P3/P4/Gamma │ │
│  └────────────────┘  └──────────────────┘  └──────────────────────┘ │
│         │                    │                       │              │
│         ▼                    ▼                       ▼              │
└─────────┼────────────────────┼───────────────────────┼──────────────┘
          │                    │                       │
          ▼                    ▼                       ▼
   ┌────────────┐       ┌────────────┐         ┌─────────────┐
   │ arXiv API  │       │  SQLite    │         │ Gemini 2.5  │
   │            │       │  + outputs/│         │   Flash     │
   └────────────┘       └────────────┘         └─────────────┘
                                                       │
                                                       ▼
                                                ┌─────────────┐
                                                │  Gamma API  │
                                                └─────────────┘
```

## 核心数据流

1. 用户在前端选一篇 arXiv 论文（或上传 PDF）
2. 前端 `POST /api/generate_ppt` → 后端返回 `taskId`
3. 后端把任务塞进队列，立即返回；后台 worker 跑 LangGraph 工作流
4. 前端每 5 秒 `GET /api/task_status?taskId=...` 查进度
5. 任务完成后，前端可 `GET /api/ppt_content?taskId=...` 拿 Markdown 在浏览器预览
6. 也可 `GET /api/download?taskId=...` 拿 PDF/PPTX 下载

## 后端工作流（LangGraph）

工作流 7 节点：

```
prepare_images
     ↓
execute_p1 (Gemini: paper → PPT blueprint markdown)
     ↓
     ├─→ call_gamma  (Gamma API: markdown → PPT PDF/PPTX)   ┐
     ├─→ execute_p2  (Gemini: paper → deep analysis)        ├─ parallel
     ├─→ execute_p3  (Gemini: paper → technical article)    │
     └─→ execute_p4  (Gemini: paper → speech script)        ┘
                     ↓
                  finalize (cleanup + persist)
```

执行时间约 5-7 分钟，其中 P2 是关键路径（95-186 秒）。

## 技术栈（2026-05 现代化后）

### 后端
- **Python** ≥ 3.10
- **FastAPI** ≥ 0.118 — Web API
- **LangGraph** 1.x — 工作流编排，1.0 稳定承诺
- **LangChain v1** — Tool calling + middleware
- **langchain-google-genai** 4.x — 统一的 google-genai SDK
- **Gemini 2.5 Flash** — thinking 模式，性价比高
- **Pydantic** ≥ 2.10 — 数据校验
- **SQLite** — 任务元数据持久化
- **Typer + Rich** — CLI

### 前端
- **Node** ≥ 18，推荐 20
- **Vue 3.5** — Composition API + `<script setup>`
- **Vite 7** — 构建
- **Pinia 3** — 状态管理（3 stores: papers/tasks/ui）
- **Tailwind CSS 3.4** — 样式（暂不升 v4，避免扫全部样式）
- **Headless UI 1.7** — 无障碍组件
- **marked + KaTeX + highlight.js + DOMPurify** — PPT 预览渲染管线
- **ESLint 9** — flat config

## 关键设计决策

### 为什么把同步大接口拆成 6 个异步端点？

原后端是单一 `POST /api/v1/process` 同步阻塞 5-7 分钟。问题：
- HTTP 超时风险（Nginx/CDN 默认 60-300 秒）
- 用户无法看到中间进度
- 失败要全跑一遍

改成异步任务模型：

| 端点 | 用途 |
|---|---|
| `GET /api/arxiv_papers?period=daily` | 拉热门论文列表（24h 缓存） |
| `POST /api/upload_pdf` | 上传 PDF，返回 fileId |
| `GET /api/analyze_paper?arxivId=...` | 论文 AI 分析（中文摘要 + 创新点） |
| `POST /api/generate_ppt` | 创建生成任务，返回 taskId |
| `GET /api/task_status?taskId=...` | 查任务状态（前端 5s 轮询） |
| `GET /api/ppt_content?taskId=...` | 拿生成的 markdown 供预览 |

详见 `docs/api-design.md`（Phase 1 输出）。

### 为什么用 SQLite 不用 Redis？

开源用户优先：能 `docker-compose up` 一条命令跑起来，不要额外的 Redis 依赖。SQLite 单文件、零运维、性能对单机 MVP 足够。横向扩展再换 Redis/Postgres，那是另一个里程碑。

### 为什么 Gemini 2.5 Flash 不是 3.1 Pro？

性价比。Flash 已经支持 thinking + 1M context，足够覆盖论文场景。3.1 Pro 是 preview、贵、不稳定，作为可选项（用户能在 `.env` 里覆盖模型名）。

### 为什么前端用 Pinia 而不是 Vuex？

Vue 官方已废弃 Vuex，Pinia 是 Vue 3 默认。Pinia 3 也是 boring major release，没踩坑成本。

### 为什么不上 Tailwind v4？

性能确实强（rebuild 100×），但 breaking changes 太多（CSS-first 配置、shadow 重命名、border 默认色变化）。前端已有自定义 design system，全扫一遍的 ROI 不划算。留 v3 待 v4 生态成熟再升。

---

## 路线图

### ✅ Phase 0（完成中）— Monorepo 基础设施 + 技术栈现代化

- monorepo 重构（frontend/ + backend/）
- 顶层 README / LICENSE / CONTRIBUTING / docs / Makefile
- 后端：LangGraph 0.2 → 1.x、LangChain → v1、langchain-google-genai 2 → 4、Gemini 模型升级
- 前端：Vite 5 → 7、Pinia 2 → 3、ESLint 8 → 9 flat config

### ⏳ Phase 1 — API contract 重设计

- `docs/api-design.md`：6 个异步端点的 request/response schema
- 任务生命周期定义（queued → generating → completed/failed）
- 错误码、重试、超时策略

### ⏳ Phase 2 — 后端改造（核心工作量）

- 加 `src/services/arxiv_client.py`（代理 arXiv + 24h SQLite 缓存）
- 加 `src/db/`（SQLite + 任务表 schema）
- 加 `src/services/task_queue.py`（asyncio.Queue + 后台 worker）
- 拆 `/api/v1/process` 为 6 个端点
- 现有 LangGraph 工作流接入任务队列（异步触发）

### ⏳ Phase 3 — 前端接通

- `.env.development`: `VITE_USE_MOCK_DATA=false`
- 抹平 mock vs 真实 API 的 schema 差异
- 端到端测试

### ⏳ Phase 4 — 一键部署

- 顶层 `docker-compose.yml`：前端 nginx + 后端 fastapi
- 镜像构建 + 推 GHCR

### ⏳ Phase 5 — 开源完整度

- GitHub Actions CI（lint + build + test）
- ISSUE / PR 模板
- 社区文档（行为准则、Maintainer 指南）

---

## 文件结构

```
Lundao/
├── README.md, LICENSE, CONTRIBUTING.md, Makefile
├── docs/
│   ├── PRODUCT.md           ← 产品定位
│   ├── ARCHITECTURE.md      ← 本文档
│   └── api-design.md        ← (Phase 1)
├── backend/
│   ├── pyproject.toml, requirements.txt, .env.example
│   ├── src/
│   │   ├── agents/          # P1–P4 prompts
│   │   ├── api/             # FastAPI app
│   │   ├── cli/             # Typer CLI
│   │   ├── core/            # workflow.py, state.py, config.py
│   │   ├── services/        # gemini_client, gamma_client, arxiv_client (Phase 2)
│   │   ├── db/              # SQLite layer (Phase 2)
│   │   └── utils/
│   ├── docs/                # Prompt-P1..P4 模板
│   └── ref/                 # 后端参考文档
└── frontend/
    ├── package.json, vite.config.js, tailwind.config.js, eslint.config.js
    ├── src/
    │   ├── api/             # axios 客户端 + service 模块
    │   ├── components/
    │   │   ├── common/      # Button, Modal, Toast, Badge, ...
    │   │   └── core/        # PaperCard, PaperModal, PPTPreviewModal, ...
    │   ├── composables/     # useTaskHistory, useTaskPolling, useFileUpload
    │   ├── mocks/           # 开发期 mock 数据
    │   ├── stores/          # papers, tasks, ui
    │   └── views/
    └── ref/                 # 前端参考文档
```
