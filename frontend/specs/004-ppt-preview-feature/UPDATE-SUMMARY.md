# Feature #004更新总结: 添加LaTeX、代码高亮和水印功能

## 更新概述

**更新时间**: 2025-01-15
**更新原因**: 用户反馈学术论文场景需要数学公式和代码支持，并需要水印保护品牌

---

## 三大核心功能更新

### 1. ✅ LaTeX数学公式支持（KaTeX）

**技术方案**:
- 使用 `marked-katex-extension` 扩展marked
- 支持行内公式 `$...$` 和块级公式 `$$...$$`
- 渲染引擎：KaTeX (轻量级，性能优于MathJax)

**依赖**:
```json
{
  "katex": "^0.16.9",                   // 340KB (含字体)
  "marked-katex-extension": "^5.0.0"    // 8KB
}
```

**示例**:
```markdown
设问题规模为 $n$，分解为 $k$ 个子问题，则：

$$T(n) = k \cdot T(\frac{n}{k}) + O(n)$$
```

**渲染效果**: 数学符号清晰，支持复杂公式（分式、上下标、根号、积分等）

---

### 2. ✅ 代码语法高亮（Highlight.js）

**技术方案**:
- 按需加载7种常用语言（非全量220种）
- 主题：github-dark（适合学术场景）
- 与marked集成，自动检测语言

**依赖**:
```json
{
  "highlight.js": "^11.9.0"  // 80KB (仅7种语言)
}
```

**支持语言**:
1. JavaScript
2. Python
3. Java
4. C++
5. SQL
6. Bash
7. JSON

**示例**:
````markdown
```python
def hierarchical_reasoning(problem, depth=0):
    if is_simple(problem):
        return solve_directly(problem)

    subproblems = decompose(problem)
    results = [hierarchical_reasoning(sub, depth+1) for sub in subproblems]
    return aggregate(results)
```
````

**渲染效果**: 语法着色清晰，行号可选，支持长代码横向滚动

---

### 3. ✅ 水印系统

**目的**:
1. 品牌保护：标识来自论导Lite
2. 防盗用：防止未授权传播截图
3. 用户引导：提示下载完整版

**技术方案**:
- 9宫格分布（防止裁剪）
- 半透明（opacity: 0.08）
- 旋转-30度
- 不阻止交互（pointerEvents: none）

**水印布局**:
```
┌─────────────────────┐
│ [水印] [水印] [水印] │  ← 上排
│                     │
│ [水印] [水印] [水印] │  ← 中排
│                     │
│ [水印] [水印] [水印] │  ← 下排
└─────────────────────┘
```

**环境配置**:
```bash
# .env.development
VITE_WATERMARK_TEXT="论导Lite 预览版 - lundao.com"
VITE_WATERMARK_OPACITY=0.08
VITE_WATERMARK_ENABLED=true
```

**组件实现**:
- 新增 `src/components/common/Watermark.vue`
- 新增 `src/config/watermark.js`
- 集成到 `PPTPreviewModal.vue`

---

## 技术架构变更

### 依赖更新（从2个→5个）

**原方案**:
```bash
npm install marked dompurify
# Total: ~45KB gzipped
```

**新方案**:
```bash
npm install marked marked-katex-extension katex highlight.js dompurify
# Total: ~160KB gzipped
```

**Bundle Size对比**:
| 依赖 | 大小（未压缩） | 大小（gzipped） |
|------|--------------|----------------|
| marked | 32KB | 12KB |
| dompurify | 13KB | 5KB |
| **katex** | **340KB** | **110KB** |
| **highlight.js** | **80KB** | **28KB** |
| **marked-katex-extension** | **8KB** | **3KB** |
| **CSS (hljs+katex)** | **17KB** | **4KB** |
| **Total** | **490KB** | **160KB** |

**性能影响**:
- 首次加载延迟：从 <500ms 调整为 <800ms
- 翻页响应：仍保持 <100ms
- 可接受范围：学术场景的必要代价

---

## 渲染管道更新

### 原渲染流程（简化版）:
```
Markdown → marked.parse() → DOMPurify → HTML
```

### 新渲染流程（完整版）:
```
Markdown
  ↓
marked.parse() (with extensions)
  ├─ KaTeX: 识别 $...$ 和 $$...$$ → 渲染为MathML/HTML
  └─ Highlight.js: 识别 ```language → 语法高亮HTML
  ↓
DOMPurify (扩展白名单)
  ├─ 允许 KaTeX 标签 (<math>, <mrow>, <mi>, etc.)
  ├─ 允许 Highlight.js 类名 (.hljs-*, .katex*)
  └─ 移除危险标签 (<script>, <iframe>, etc.)
  ↓
HTML (with 水印叠加层)
```

---

## 任务列表变更

### 原任务数：18个 (T001-T018)
### 新任务数：20个 (T001-T020)

**新增任务**:
- **T015**: 创建水印组件 (60分钟)
- **T016**: 集成水印到Modal (20分钟)

**修改任务**:
- **T001**: 安装5个依赖（原2个） → 时间从10分钟调整为15分钟
- **T002**: Mock数据包含LaTeX和代码示例 → 时间从60分钟调整为75分钟
- **T003**: 渲染工具集成KaTeX和Highlight.js → 时间从45分钟调整为60分钟
- **T011**: 样式美化包含KaTeX和代码高亮CSS → 时间从60分钟调整为75分钟
- **T017**: 功能测试包含公式和代码验证 → 时间从60分钟调整为75分钟
- **T018**: 安全测试包含LaTeX注入测试 → 时间从30分钟调整为40分钟
- **T019**: 性能测试包含Bundle分析 → 时间从45分钟调整为60分钟
- **T020**: 文档更新包含依赖说明 → 时间从30分钟调整为40分钟

**工时变化**: 8-12小时 → 10-14小时

---

## Mock数据示例更新

### Task 1更新：Hierarchical Reasoning Models

**新增2页幻灯片**:

#### 页面4: 数学原理
```markdown
## 数学原理

### 递归复杂度分析

设问题规模为 $n$，分解为 $k$ 个子问题，则：

$$T(n) = k \cdot T(\frac{n}{k}) + O(n)$$

当 $k=2$ 时，时间复杂度为：

$$T(n) = O(n \log n)$$

相比传统方法的 $O(n^2)$，效率提升显著。
```

#### 页面5: 算法实现
````markdown
## 算法实现

### 伪代码

```python
def hierarchical_reasoning(problem, depth=0):
    # Base case: 简单问题直接求解
    if is_simple(problem):
        return solve_directly(problem)

    # Decompose: 分解为子问题
    subproblems = decompose(problem)

    # Recursive: 递归求解子问题
    results = [
        hierarchical_reasoning(sub, depth+1)
        for sub in subproblems
    ]

    # Aggregate: 聚合子问题结果
    return aggregate(results)
```
````

**总页数变化**: 8页 → 10页

---

## 安全性增强

### DOMPurify白名单扩展

**原白名单**:
```javascript
ALLOWED_TAGS: [
  'h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li', 'code', 'pre',
  'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'a', 'img'
]
```

**新白名单**:
```javascript
ALLOWED_TAGS: [
  // 原有标签
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre', 'span',
  'ul', 'ol', 'li',
  'table', 'thead', 'tbody', 'tr', 'th', 'td',
  'blockquote', 'a', 'img',

  // KaTeX需要的MathML标签
  'annotation', 'math', 'mrow', 'mi', 'mo', 'mn', 'mtext', 'mspace',
  'semantics', 'mstyle', 'msup', 'msub', 'mfrac', 'mover', 'munder'
],
ALLOWED_ATTR: [
  'href', 'src', 'alt', 'title', 'class', 'style',
  // KaTeX需要的属性
  'xmlns', 'encoding', 'data-*'
],
ALLOWED_STYLES: {
  '*': {
    'color': [/^#[0-9a-f]{3,6}$/i],
    'font-size': [/^\d+(?:\.\d+)?(?:px|em|rem|%)$/],
    'margin': [/^\d+(?:\.\d+)?(?:px|em|rem)$/],
    'padding': [/^\d+(?:\.\d+)?(?:px|em|rem)$/]
  }
}
```

**新增测试用例**:
- XSS4: LaTeX公式中的恶意代码被正确转义
- 示例：`$\text{<script>alert('XSS')</script>}$` → 被DOMPurify清理

---

## 样式系统更新

### CSS导入（新增）

```vue
<script setup>
// 原有导入
import PPTPreviewModal from '@/components/core/PPTPreviewModal.vue'

// 新增CSS导入
import 'highlight.js/styles/github-dark.css'  // 代码高亮主题
import 'katex/dist/katex.min.css'             // 数学公式样式
</script>
```

### 新增样式类

```css
/* KaTeX数学公式 */
:deep(.katex) {
  @apply text-text-primary;
  font-size: 1.1em;
}

:deep(.katex-display) {
  @apply my-4;  /* 块级公式上下间距 */
}

/* Highlight.js代码高亮 */
:deep(pre code) {
  @apply bg-transparent text-inherit p-0;
}

/* 水印容器 */
.watermark-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}
```

---

## 文件清单更新

### 新增文件（5个）

1. `src/components/common/Watermark.vue` - 水印组件
2. `src/config/watermark.js` - 水印配置管理
3. `src/utils/watermarkProtection.js` - 防篡改工具（可选，Phase 2）
4. `.env.development` - 新增水印环境变量
5. `.env.production` - 新增水印环境变量

### 修改文件（5个）

1. `src/utils/pptRenderer.js` - 集成KaTeX和Highlight.js
2. `src/mocks/pptContentData.js` - 添加公式和代码示例
3. `src/components/core/PPTPreviewModal.vue` - 集成水印、导入CSS
4. `package.json` - 新增5个依赖
5. `specs/004-ppt-preview-feature/technical-design.md` - 完整更新

---

## 性能优化策略

### Bundle Size控制

1. **按需加载语言**: Highlight.js仅加载7种语言（非全量220种）
   ```javascript
   import hljs from 'highlight.js/lib/core'
   import python from 'highlight.js/lib/languages/python'
   // 仅注册需要的语言，节省 ~150KB
   ```

2. **动态导入**: pptRenderer.js使用 `import()` 延迟加载
   ```javascript
   const { renderAllSlides } = await import('@/utils/pptRenderer.js')
   ```

3. **字体优化（Phase 2）**: KaTeX字体子集化，仅包含常用数学符号
   - 当前: 全量字体 ~280KB
   - 优化后: 子集字体 ~80KB（节省70%）

4. **CDN备选方案**（生产环境）:
   ```html
   <!-- 从CDN加载KaTeX和Highlight.js -->
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
   <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
   ```

---

## 验收标准更新

### 新增检查项

**功能完整性**:
- [ ] LaTeX数学公式正确渲染（行内和块级）
- [ ] 代码语法高亮正常工作（7种语言）
- [ ] 水印正常显示（9宫格分布，半透明）

**性能标准**:
- [ ] Bundle size ≈ 160KB gzipped（实际测量）
- [ ] 首次打开延迟 < 800ms（含KaTeX加载）
- [ ] KaTeX公式渲染 < 50ms
- [ ] Highlight.js代码渲染 < 100ms

**安全标准**:
- [ ] XSS防护测试通过（包含LaTeX注入）
- [ ] DOMPurify白名单配置正确（含KaTeX标签）
- [ ] 水印防篡改（MVP阶段基础防护）

**依赖管理**:
- [ ] package.json包含5个新依赖
- [ ] CSS正确导入（highlight.js + katex）
- [ ] 按需加载语言（hljs仅7种，非全量）

---

## 与原设计的对比

| 维度 | 原设计 | 新设计 | 变化原因 |
|------|-------|--------|---------|
| **依赖数量** | 2个 | 5个 | 学术场景必需 |
| **Bundle Size** | 45KB | 160KB | 功能完整性代价 |
| **首屏延迟** | <500ms | <800ms | 可接受的性能平衡 |
| **任务数量** | 18个 | 20个 | 新增水印系统 |
| **工时预估** | 8-12h | 10-14h | 功能增加 |
| **技术复杂度** | 中 | 中高 | 多依赖集成 |

---

## 下一步行动

### 立即可开始

1. **安装依赖** (T001):
   ```bash
   npm install marked marked-katex-extension katex highlight.js dompurify
   ```

2. **验证渲染**（快速测试）:
   - 创建测试HTML，包含数学公式和代码
   - 验证KaTeX和Highlight.js正常工作
   - 确认Bundle size影响

3. **环境配置**:
   - 创建 `.env.development` 添加水印配置
   - 创建 `.env.production` 添加水印配置

### 开发顺序建议

```
Day 1 (5h):
  T001 安装依赖 (15min)
    ↓
  T002 创建Mock数据 (75min)
    ↓
  T003 实现渲染工具 (60min)
    ↓
  T004 创建API服务 (30min)
    ↓
  T005 扩展Store (30min)
    ↓
  T006 创建Modal组件 (90min)

Day 2 (4h):
  T007-T009 翻页+预览按钮+集成 (90min)
    ↓
  T010 键盘导航 (30min)
    ↓
  T011 样式美化+CSS (75min)
    ↓
  T015 创建水印组件 (60min)
    ↓
  T016 集成水印 (20min)

Day 3 (3h):
  T017 功能测试 (75min)
    ↓
  T018 安全测试 (40min)
    ↓
  T019 性能测试 (60min)
    ↓
  T020 文档更新 (40min)
```

---

## 常见问题解答

### Q1: 为什么Bundle size增长这么多？
**A**: KaTeX字体文件占大头（340KB），这是学术场景的必要代价。可通过以下方式优化：
- Phase 2字体子集化（节省70%）
- 生产环境使用CDN（零Bundle影响）
- 按需动态导入（首屏不加载）

### Q2: 支持更多编程语言吗？
**A**: 当前按需加载7种常用语言。如需更多：
```javascript
import rust from 'highlight.js/lib/languages/rust'
hljs.registerLanguage('rust', rust)
```
每增加1种语言约增加 ~5-10KB。

### Q3: 水印可以去掉吗？
**A**: MVP阶段水印可通过环境变量禁用：
```bash
VITE_WATERMARK_ENABLED=false
```
但建议保留，品牌保护重要性远超开发成本。

### Q4: LaTeX公式渲染失败怎么办？
**A**: 降级策略：
1. KaTeX报错时，marked-katex-extension配置了 `throwOnError: false`
2. 渲染失败会显示原始LaTeX代码
3. 前端日志会记录错误，便于调试

### Q5: 性能影响用户体验吗？
**A**: <800ms首屏延迟在可接受范围内（学术用户容忍度高）。优化建议：
- 使用Service Worker缓存KaTeX字体
- CDN加速（生产环境）
- 渲染缓存（T014）避免重复加载

---

## 总结

### 核心价值

1. **功能完整**: 真正满足学术论文场景（公式+代码）
2. **品牌保护**: 水印系统防止未授权传播
3. **渐进增强**: 基础功能完整，可后续优化（CDN、字体子集化）

### 技术亮点

1. **安全优先**: DOMPurify白名单扩展，XSS防护全面
2. **性能平衡**: 160KB代价换取完整功能，合理trade-off
3. **可维护性**: 环境变量配置灵活，组件化设计清晰

### 风险控制

1. **已知风险**: Bundle size增大 → 缓解：CDN + 字体优化
2. **已知风险**: 首屏延迟增加 → 缓解：动态导入 + 缓存
3. **未知风险**: KaTeX浏览器兼容性 → 缓解：降级策略（显示原始LaTeX）

---

**文档版本**: 2.0
**最后更新**: 2025-01-15
**更新人**: Claude Code
**审批状态**: ⏸️ 待用户确认

---

## 附录：快速命令参考

```bash
# 安装依赖
npm install marked marked-katex-extension katex highlight.js dompurify

# 开发模式（水印启用）
npm run dev

# 生产构建
npm run build

# Bundle分析
npm run build -- --report

# 测试XSS防护
# 在Mock数据中添加 <script>alert('XSS')</script>，验证被清理

# 测试LaTeX渲染
# Mock数据中添加 $E=mc^2$，验证正常渲染

# 测试代码高亮
# Mock数据中添加 ```python\nprint('Hello')\n```，验证语法着色
```
