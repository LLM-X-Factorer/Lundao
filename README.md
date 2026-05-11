# 论导 Lundao

> AI 助你三分钟搞定组会 PPT —— 面向中文学术研究者的论文发现、解读与汇报自动化工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Status: Pre-1.0](https://img.shields.io/badge/Status-Pre--1.0-orange)](./docs/PRODUCT.md)

研究生/博士生的组会汇报，传统流程要花 3–5 小时：找论文、读论文、做 PPT、写讲稿。**Lundao 把这套流程压缩到 3 分钟**——你只需要选一篇论文（或上传 PDF），系统会自动给你：

1. 📊 **PPT 蓝图**（Gamma 风格 Markdown，可直接出图）
2. 📝 **深度解读**（Why-How-Effect 风格的技术白皮书）
3. 📰 **技术文章**（面向中高级开发者的通俗稿）
4. 🎤 **演讲逐字稿**（能直接背的中文讲稿）

零注册、零配置（除了 API key），开源 MIT。

---

## 仓库结构

```
Lundao/
├── backend/    # FastAPI + LangGraph + Gemini 2.5 Flash 工作流
├── frontend/   # Vue 3 + Vite 单页应用
├── docs/       # 产品定位、架构设计、API 合约
└── Makefile    # 常用命令封装
```

- **后端**：Python 3.10+，参考 [`backend/README.md`](./backend/README.md)
- **前端**：Node 18+，参考 [`frontend/README.md`](./frontend/README.md)
- **产品定位**：[`docs/PRODUCT.md`](./docs/PRODUCT.md)
- **架构设计**：[`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)

---

## 快速开始

### 前置条件

- Python ≥ 3.10、Node ≥ 18
- Google Gemini API Key（[领取](https://aistudio.google.com/apikey)）
- Gamma API Key（[官网申请](https://gamma.app/)，可选）

### 本地开发

```bash
# 1. 克隆
git clone https://github.com/<your-org>/Lundao.git && cd Lundao

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 填入 GOOGLE_API_KEY 等

# 3. 安装依赖
make install         # 同时装 backend 和 frontend 依赖

# 4. 启动开发环境
make dev             # 后端 :8000 + 前端 :5173 同时起
```

打开 http://localhost:5173 ，挑一篇论文，三分钟后取走结果。

### Docker 部署（一键启动）

```bash
# 配好 backend/.env 之后
make docker-build    # 构建前后端镜像（首次约 2-3 分钟）
make docker-up       # 启动（后端 :8000，前端 :8080）
make docker-logs     # 看日志
make docker-down     # 停止
```

前端通过 Nginx 反代到后端容器，浏览器访问 **http://localhost:8080** 即可（无需单独暴露后端端口）。任务数据持久化到宿主 `./data/`。

---

## 路线图

当前状态：**Phase 0 — Monorepo 基础设施 + 技术栈现代化**

- [x] 合并 frontend/backend 为 monorepo
- [x] 升级 LangChain v1 / LangGraph 1.x / Gemini 2.5 Flash / Vite 7 / Pinia 3 / ESLint 9
- [ ] Phase 1：异步任务 API contract 重设计
- [ ] Phase 2：后端 arXiv 接入 + 任务队列（SQLite）
- [ ] Phase 3：前端切换到真实 API（不再用 mock）
- [ ] Phase 4：docker-compose 一键启动
- [ ] Phase 5：CI、ISSUE/PR 模板、社区治理

详见 [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) 的路线图章节。

---

## 贡献

欢迎 PR。开始之前请读 [`CONTRIBUTING.md`](./CONTRIBUTING.md) 了解开发流程、代码风格、commit 规范。

## License

[MIT](./LICENSE) © 2026 Lundao Project Contributors
