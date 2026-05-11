# Feature #004: PPT内容预览功能 - 问题分析

## 核心问题矩阵

### Q1: PPT内容从哪里来？
**当前状态**:
- `taskData.js` 只存储任务元数据（taskId, status, downloadUrl等）
- 没有存储PPT的源内容（Markdown或HTML）
- `downloadUrl` 指向二进制 `.pptx` 文件（无法直接渲染）

**解决方案**:
- **短期**（Mock模式）: 创建 `pptContentData.js` 存储Markdown格式的PPT内容
- **长期**（Real API）: 后端提供 `GET /api/ppt_content?taskId={uuid}` 返回Markdown源码

**决策**: 采用Markdown作为中间格式，理由：
1. 易于编写Mock数据（纯文本）
2. 可直接渲染为HTML（marked库）
3. 符合另一个项目的成功实践

---

### Q2: 预览什么格式？
**选项评估**:
| 方案 | 复杂度 | 用户体验 | 可行性 |
|------|--------|---------|--------|
| A. 直接预览.pptx文件 | 高（需pptx解析器） | 好 | 差（库体积大） |
| B. 预览Markdown源码 | 低 | 差（不直观） | 好 |
| C. Markdown→HTML幻灯片 | 中 | 好 | **优选** |

**决策**: 选择方案C
- 使用 `marked` 将Markdown渲染为HTML
- 使用 `---` 分隔符拆分为幻灯片页面
- 提供翻页导航（上一页/下一页/页码）

---

### Q3: 是否需要实时编辑功能？
**对比参考项目**:
- 参考项目: Monaco编辑器 + 实时预览（双面板）
- 当前需求: 只读预览（单面板）

**决策**: **不需要编辑功能**
- 用户角色：研究者（消费者），非内容创作者
- 场景：快速浏览PPT质量，判断是否下载
- 简化实现：降低70%复杂度

---

### Q4: 技术栈如何选择？
**参考项目依赖**:
```
marked + highlight.js + marked-katex-extension + DOMPurify
```

**当前项目需求评估**:
| 依赖 | 参考项目用途 | 当前项目需求 | 是否必需 |
|------|-------------|-------------|---------|
| marked | Markdown→HTML | 同上 | ✅ 必需 |
| DOMPurify | XSS防护 | 同上 | ✅ 必需 |
| highlight.js | 代码语法高亮 | 学术PPT很少有代码 | ❓ 可选（Phase 2） |
| katex | 数学公式 | 学术PPT可能需要 | ❓ 可选（Phase 2） |

**决策**: MVP只包含 `marked + DOMPurify`
- Bundle size控制: +45KB (marked 32KB + DOMPurify 13KB)
- 后续可按需添加highlight.js (100KB+) 和 katex (600KB+)

---

## 技术风险评估

### R1: Bundle Size增长
**风险**: 新增依赖增加首屏加载时间
**缓解**:
- marked + DOMPurify 仅 45KB gzipped（可接受）
- 使用 dynamic import 实现按需加载（仅在打开预览时加载）
```javascript
// 延迟加载方案
const { renderSlides } = await import('@/utils/pptRenderer.js')
```

### R2: Mock数据维护成本
**风险**: 每个任务需手动编写Markdown内容（工作量）
**缓解**:
- MVP阶段只为3个历史任务编写Mock内容
- 使用模板生成器辅助（可选）

### R3: API契约不确定性
**风险**: 后端API格式可能与前端假设不符
**缓解**:
- 在 `contracts/` 目录明确定义API契约
- Mock数据严格遵循契约格式
- 使用环境变量切换Mock/Real模式

---

## 与宪法原则的对齐

### ✅ 符合原则I-III: 工具优先
- 预览功能是**纯工具性**：帮助用户快速判断PPT质量
- 无需登录（与现有架构一致）
- 无gamification（纯信息展示）

### ✅ 符合原则IV: 单页应用
- 使用Modal而非新路由
- 保持所有功能在根路由 `/`

### ✅ 符合原则V: 美学即信任
- 复用现有Design System（Tailwind配置）
- 遵循8px网格间距
- 使用Inter + Noto Sans SC字体

---

## 成功指标

### 功能指标
- [x] 已完成任务显示"预览"按钮
- [x] 点击后<1s内弹出Modal
- [x] 正确渲染Markdown为HTML幻灯片
- [x] 翻页功能正常（键盘/鼠标）
- [x] Mock模式和Real API模式均可切换

### 性能指标
- [x] Modal打开延迟 < 500ms（含渲染时间）
- [x] Bundle size增长 < 50KB gzipped
- [x] 首屏性能无明显下降（FCP < 1.5s）

### 用户体验指标
- [x] 幻灯片布局清晰（标题/内容区分明显）
- [x] 页码指示器清晰（如 "3 / 5"）
- [x] 加载/错误状态有明确反馈
