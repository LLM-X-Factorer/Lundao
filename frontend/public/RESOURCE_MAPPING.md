# PPT 资源映射文档

本文档说明每篇每日热门论文所需的 PPT 图片和下载文件资源。

## 目录结构

```
public/
├── ppt-images/          # PPT 截图存放目录
│   ├── daily-0001/      # 论文 1 的截图
│   │   ├── slide-1.png
│   │   ├── slide-2.png
│   │   ├── slide-3.png
│   │   └── ...
│   ├── daily-0002/      # 论文 2 的截图
│   │   └── ...
│   └── ...
└── ppt-files/           # PPTX 文件存放目录
    ├── daily-0001.pptx  # 论文 1 的完整 PPT
    ├── daily-0002.pptx  # 论文 2 的完整 PPT
    └── ...
```

---

## 每日热门论文资源清单

### 论文 1: Hierarchical Reasoning Models
- **论文ID**: `daily-0001`
- **标题**: Hierarchical Reasoning Models: Small-Scale Recursive Reasoning Outperforms LLMs
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0001/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ... (数量不固定)
  - PPTX 文件: `public/ppt-files/daily-0001.pptx`

### 论文 2: OpenTSLM
- **论文ID**: `daily-0002`
- **标题**: OpenTSLM: Time Series as Native Modality in Pretrained Language Models
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0002/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0002.pptx`

### 论文 3: Delethink
- **论文ID**: `daily-0003`
- **标题**: Delethink: Efficient Very Long Reasoning Without Quadratic Overhead
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0003/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0003.pptx`

### 论文 4: RLVR
- **论文ID**: `daily-0004`
- **标题**: RLVR: Reinforcement Learning with Verifiable Rewards for Vision-Language Models
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0004/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0004.pptx`

### 论文 5: Multi-Agent Collaborative Reasoning
- **论文ID**: `daily-0005`
- **标题**: Multi-Agent Collaborative Reasoning: A Survey of Recent Advances
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0005/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0005.pptx`

### 论文 6: Chain of Thought Prompting
- **论文ID**: `daily-0006`
- **标题**: Chain of Thought Prompting: Theoretical Foundations and Learning Dynamics
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0006/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0006.pptx`

### 论文 7: Cultural Understanding in Vision-Language Models
- **论文ID**: `daily-0007`
- **标题**: Cultural Understanding in Vision-Language Models: A Global Perspective
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0007/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0007.pptx`

### 论文 8: Hallucination Detection in Financial AI
- **论文ID**: `daily-0008`
- **标题**: Hallucination Detection in Financial AI: Methods and Benchmarks
- **所需资源**:
  - 图片目录: `public/ppt-images/daily-0008/`
  - 截图命名: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
  - PPTX 文件: `public/ppt-files/daily-0008.pptx`

---

## 图片规格建议

为了确保预览效果最佳，建议按以下规格准备 PPT 截图：

### 图片格式
- **首选格式**: PNG（无损压缩，适合文字清晰度）
- **备选格式**: JPG（有损压缩，文件更小）
- **不推荐**: WebP（部分浏览器兼容性问题）

### 图片尺寸
- **推荐尺寸**: 1920×1080 (16:9, Full HD)
- **备选尺寸**: 1280×720 (16:9, HD)
- **最小尺寸**: 960×540 (避免模糊)

### 文件大小
- **单张图片**: < 500 KB（推荐）
- **最大限制**: < 1 MB（避免加载过慢）
- **压缩工具**: TinyPNG, ImageOptim, Squoosh

### 命名规则
- **格式**: `slide-{序号}.png` (从 1 开始)
- **示例**: `slide-1.png`, `slide-2.png`, `slide-3.png`, ...
- **重要**: 序号必须连续，不能跳号

---

## PPTX 文件要求

### 文件命名
- **格式**: `{论文ID}.pptx`
- **示例**: `daily-0001.pptx`, `daily-0002.pptx`, ...

### 文件大小
- **推荐大小**: < 10 MB
- **最大限制**: < 20 MB（避免下载时间过长）

### 内容要求
- **幻灯片数量**: 与截图数量一致
- **格式**: PowerPoint 2016+ 兼容格式 (.pptx)
- **字体**: 使用常见字体（避免字体缺失问题）

---

## 资源上传检查清单

在上传资源前，请确认：

- [ ] 每篇论文有对应的图片目录（8 个目录）
- [ ] 每个目录包含完整的幻灯片截图（连续编号）
- [ ] 每篇论文有对应的 PPTX 文件（8 个文件）
- [ ] 所有图片格式为 PNG 或 JPG
- [ ] 所有图片尺寸统一（推荐 1920×1080）
- [ ] 单张图片文件小于 500 KB
- [ ] PPTX 文件小于 10 MB
- [ ] 文件命名符合规范（`slide-1.png`, `daily-0001.pptx`）

---

## 前端自动检测逻辑

前端会自动检测每篇论文的截图数量：

1. **扫描目录**: 查找 `public/ppt-images/{paperId}/` 目录
2. **识别截图**: 匹配 `slide-{n}.png` 或 `slide-{n}.jpg` 模式
3. **计算总数**: 根据最大序号确定总幻灯片数
4. **生成 URL**: 自动生成预览和下载 URL

**示例**:
- 如果 `daily-0001/` 包含 `slide-1.png` 到 `slide-12.png`
- 前端会自动识别为 12 张幻灯片
- 预览时显示 "第 X / 12 张"

---

## 故障排除

### 问题 1: 图片无法加载
- **检查**: 文件命名是否正确（`slide-1.png`，不是 `Slide-1.png` 或 `slide_1.png`）
- **检查**: 文件是否放在正确的目录（`public/ppt-images/{paperId}/`）
- **检查**: 文件权限是否正确（可读）

### 问题 2: PPTX 下载失败
- **检查**: 文件命名是否与论文 ID 匹配（`daily-0001.pptx`）
- **检查**: 文件是否放在 `public/ppt-files/` 目录
- **检查**: 文件格式是否为 .pptx（不是 .ppt 或 .pdf）

### 问题 3: 图片显示模糊
- **检查**: 图片分辨率是否足够（最低 960×540）
- **检查**: 图片是否过度压缩（尝试提高质量）
- **检查**: 浏览器缩放设置（应为 100%）

---

## 联系与支持

如有问题，请检查：
1. 本文档的资源规范
2. 前端配置文件 `src/config/pptImages.js`
3. Mock 数据文件 `src/mocks/pptContentData.js`

---

**最后更新**: 2025-01-15
**版本**: Feature #006 - PPT Image Preview
