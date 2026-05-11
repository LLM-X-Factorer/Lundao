# Feature #004 快速启动卡片

## 🚀 3分钟开始

```bash
# 1. 安装依赖 (1分钟)
npm install marked marked-katex-extension katex highlight.js dompurify

# 2. 验证安装 (30秒)
npm list | grep -E "marked|katex|highlight|dompurify"

# 3. 创建第一个文件 (1分钟)
touch src/mocks/pptContentData.js
# 复制内容从 IMPLEMENTATION-GUIDE.md → T002

# 4. 开始开发！
npm run dev
```

---

## 📋 今日待办 (Phase 1)

```
[ ] T001: 安装依赖 (15min) ← 从这里开始
[ ] T002: 创建Mock数据 (75min)
[ ] T003: 创建渲染工具 (60min)
[ ] T004: 创建API服务 (30min)

预计时间: 2.5小时
里程碑: 渲染管道可独立测试
```

---

## 🎯 关键命令

```bash
# 环境检查
node --version && npm --version

# 语法检查
node -c src/mocks/pptContentData.js
node -c src/utils/pptRenderer.js

# 构建测试
npm run build

# 开发调试
npm run dev
```

---

## 📚 文档导航

| 需要... | 查看文档 | 位置 |
|---------|---------|------|
| 开始实施 | IMPLEMENTATION-GUIDE.md | 详细步骤 |
| 理解设计 | technical-design.md | 完整架构 |
| 查看任务 | tasks.md | 20个任务清单 |
| 了解变更 | UPDATE-SUMMARY.md | 更新总结 |

---

## ⚡ 常见问题

**Q: 依赖安装失败？**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Q: 如何测试渲染？**
```javascript
// 浏览器Console
import { renderSlide } from '@/utils/pptRenderer'
console.log(renderSlide('设 $E=mc^2$'))
```

**Q: Bundle太大怎么办？**
- Phase 2再优化（CDN、字体子集化）
- MVP阶段160KB可接受

---

## ✅ 验收检查（Phase 1）

```bash
# 全部通过才能进入Phase 2
✓ npm list 显示5个新依赖
✓ src/mocks/pptContentData.js 存在
✓ src/utils/pptRenderer.js 存在
✓ src/api/pptContentService.js 存在
✓ node -c 所有文件无语法错误
✓ npm run build 成功
```

---

## 📞 需要帮助？

- 阻塞问题: 查看technical-design.md第11节错误处理
- API问题: 查看contracts/ppt-content-api.md
- 技术细节: 查看IMPLEMENTATION-GUIDE.md对应任务

---

**开始时间**: ___________
**预计完成**: ___________ (+2.5h)
**实际完成**: ___________
