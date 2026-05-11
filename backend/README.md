# Lundao Backend P2P3

学术论文组会分享自动化系统 - 使用 LangGraph 和 Gemini 3 自动生成 PPT 蓝图和演讲材料。

## 功能特性

本系统可以自动化处理学术论文，生成：

1. **P1: Gamma API 就绪的 PPT 蓝图 Markdown** - 符合 Gamma API 格式，可直接生成 PPT
2. **P2: 深度解读文档** - Why-How-Effect 风格的技术白皮书
3. **P3: 技术经验文章** - 面向中高级开发者的通俗技术文章
4. **P4: 演讲逐字稿** - 可直接背诵的中文演讲脚本
5. **Gamma PPT** - 自动调用 Gamma API 生成在线 PPT

## 架构特点

- **LangGraph 工作流编排** - 灵活的有向无环图 (DAG) 执行流程
- **并行执行** - P2/P3/P4 在 P1 完成后并行生成，提高效率
- **多模态支持** - 使用 Gemini 3 处理文本和图片
- **本地图片服务器** - 自动启动临时 HTTP 服务器托管图片
- **双接口** - 提供 CLI 工具和 Web API 两种使用方式

## 系统要求

- Python 3.10+
- Google Gemini API Key
- Gamma API Key

## 安装

### 1. 克隆仓库

```bash
git clone <repository-url>
cd Lundao-Backend-P2P3
```

### 2. 安装依赖

使用 uv（推荐）:

```bash
uv sync
```

或使用 pip:

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GAMMA_API_KEY=your_gamma_api_key_here
```

## 使用方法

### CLI 使用

基本用法：

```bash
# 使用 uv
uv run lundao process examples/2410.05779v3

# 或直接运行
python -m src.cli.main process examples/2410.05779v3
```

指定输出目录：

```bash
lundao process examples/2410.05779v3 --output-dir ./my_outputs
```

### Web API 使用

启动 API 服务器：

```bash
# 使用 uv
uv run python -m src.api.main

# 或直接运行
python -m src.api.main
```

API 文档: http://localhost:8000/docs

使用 API 处理论文：

```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -H "Content-Type: application/json" \
  -d '{
    "paper_id": "2410.05779v3",
    "paper_md": "...",
    "paper_meta": {},
    "image_paths": ["/path/to/image1.jpeg"]
  }'
```

## 输入格式

论文目录应包含以下文件：

```
examples/2410.05779v3/
├── 2410.05779v3.md              # 论文 Markdown 文件
├── 2410.05779v3_meta.json       # 论文元信息（可选）
└── *.jpeg / *.png               # 论文中的图表文件
```

## 输出结构

处理完成后，输出目录结构如下：

```
outputs/
└── 2410.05779v3/
    ├── p1_gamma_markdown.md     # P1: PPT 蓝图
    ├── p2_deep_analysis.md      # P2: 深度解读
    ├── p3_tech_article.md       # P3: 技术文章
    ├── p4_speech_script.md      # P4: 演讲稿
    └── metadata.json            # 元数据（包含 Gamma PPT URL）
```

## 工作流程图

```
论文材料（.md + .json + 图片）
    ↓
启动图片服务器 → 生成图片 URLs
    ↓
[P1] 生成 PPT 蓝图 Markdown
    ↓
    ├─→ 调用 Gamma API → 生成 PPT
    ├─→ [P2] 生成深度解读文档     ┐
    ├─→ [P3] 生成技术文章          ├─ 并行执行
    └─→ [P4] 生成演讲稿           ┘
    ↓
保存所有输出 + 关闭图片服务器
```

## 技术栈

- **LangGraph** - Agent 工作流编排
- **Google Gemini 3** - LLM 推理引擎
- **LangChain** - LLM 应用框架
- **FastAPI** - Web API 框架
- **Typer** - CLI 工具框架
- **Pydantic** - 数据验证
- **Loguru** - 日志管理

## 开发

### 运行测试

```bash
uv run pytest
```

### 代码格式化

```bash
uv run black src tests
uv run ruff check src tests
```

### 类型检查

```bash
uv run mypy src
```

## 配置说明

所有配置项在 `.env` 文件中设置：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `GOOGLE_API_KEY` | Google Gemini API 密钥 | 必填 |
| `GAMMA_API_KEY` | Gamma API 密钥 | 必填 |
| `IMAGE_SERVER_PORT` | 图片服务器端口 | 8001 |
| `API_PORT` | Web API 服务器端口 | 8000 |
| `OUTPUT_DIR` | 输出目录 | ./outputs |
| `LOG_LEVEL` | 日志级别 | INFO |

## 故障排除

### 图片服务器端口被占用

修改 `.env` 中的 `IMAGE_SERVER_PORT` 为其他端口。

### Gemini API 超时

长文档处理可能需要较长时间，系统已配置无超时限制。

### Gamma API 失败

检查：
1. API key 是否正确
2. 网络连接是否正常
3. Markdown 格式是否符合 Gamma 要求

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!

## 致谢

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Gemini](https://ai.google.dev/)
- [Gamma](https://gamma.app/)