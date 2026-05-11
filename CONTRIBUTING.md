# Contributing to Lundao

感谢有兴趣一起把它做完。这份文档帮你 5 分钟搞清楚怎么贡献。

## 开始之前

- 读 [`docs/PRODUCT.md`](./docs/PRODUCT.md) — 知道这个产品是什么、给谁用、不做什么
- 读 [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — 了解前后端怎么协作、数据怎么流转
- 跑通本地开发环境（顶层 `make install && make dev`）

## 工作流

1. **找 issue 或开 issue**
   - bug：贴复现步骤、期望、实际、环境
   - feature：先开 issue 讨论再写代码，避免做了不被合并
2. **fork + branch**：`feat/...`、`fix/...`、`docs/...`、`refactor/...`
3. **写代码 + 测试**：见下面"代码风格"
4. **提 PR**：标题用约定式 commit 格式（`feat: ...`、`fix: ...`），描述里说"为什么改"而不只是"改了什么"
5. **CI 跑过 + 至少一个 reviewer approve** → 合并

## 代码风格

### 后端（Python）

- Formatter：`black`（line-length 100）
- Linter：`ruff`
- 类型检查：`mypy`（宽松模式）
- 跑一遍：`cd backend && uv run black src/ && uv run ruff check src/ && uv run mypy src/`

### 前端（Vue 3 + JS）

- Linter：ESLint 9（flat config，`eslint.config.js`）
- Composition API + `<script setup>` 是强约束
- 跑一遍：`cd frontend && npm run lint`

### Commit 信息

约定式 commit（[Conventional Commits](https://www.conventionalcommits.org/)）：

```
feat(backend): add arxiv client with 24h cache
fix(frontend): handle 202 retry edge case in paper analysis
docs: clarify Gemini API key requirement in QUICKSTART
refactor(backend): extract task queue from workflow.py
```

英文，1-2 句话，说清"为什么"。

## 测试

- 后端：`cd backend && uv run pytest`
- 前端：（暂未配置 Vitest，欢迎贡献）

PR 涉及代码改动的，至少跑一遍现有测试不要回归。

## 设计原则（前端非协商）

前端遵循 5 条 constitutional principles（详见 [`frontend/.specify/memory/constitution.md`](./frontend/.specify/memory/constitution.md)）：

1. **Tool-First** — 无账户、无 gamification
2. **Single-Page** — 所有功能在 `/` 一个页面
3. **Zero Friction** — 没有登录墙
4. **Value-First** — AI 洞察前置展示
5. **Aesthetics as Trust** — 严格遵循设计系统

违反这 5 条需要在 PR 里写明 constitutional amendment 理由。

## 行为准则

互相尊重，对事不对人。有问题先开 issue 聊清楚再动手。

## License

提交 PR 即同意你的贡献以 [MIT License](./LICENSE) 发布。
