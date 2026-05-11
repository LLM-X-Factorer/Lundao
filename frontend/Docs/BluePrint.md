### **“论导Lite” - 前端开发启动蓝图**

#### **第一部分：UI/UX 设计语言 (Design System) - 简洁学术风格**

我们将定义一套视觉规范，确保整个产品的外观和感觉统一、专业、清爽。

**1. 色彩体系 (Color Palette)**

  * **主背景色 (Primary Background)**: `#FFFFFF` (纯白) 或 `#FDFDFD` (极浅灰)，营造干净、宽敞的感觉。
  * **辅助背景色 (Secondary Background)**: `#F8F9FA` (淡灰色)，用于卡片、输入框等需要与主背景区分的元素。
  * **边框与分割线 (Borders & Dividers)**: `#E9ECEF` (浅灰色)，用于提供柔和的视觉分隔。
  * **主文字色 (Primary Text)**: `#212529` (近黑色)，保证内容的可读性。
  * **次要文字色 (Secondary Text)**: `#6C757D` (中灰色)，用于作者、时间、提示性文字等。
  * **品牌/强调色 (Accent Color)**: `#3A57E8` (一种沉稳而有活力的蓝色)，用于所有可交互元素，如按钮、链接、Tabs的激活状态、图标等。
  * **成功色**: `#198754` (绿色)，用于任务完成状态和成功提示。
  * **失败/错误色**: `#DC3545` (红色)，用于任务失败状态和错误提示。

**2. 字体排印 (Typography)**

  * **UI主字体**: `Inter` (英文/数字)。这是一款专为屏幕设计的无衬线字体，清晰、现代且易于阅读。
  * **中文内容字体**: `Noto Sans SC` (思源黑体)。确保中文字符在各种字重下都有优秀的显示效果。
  * **字号体系**:
      * 主标题 (H1): `28px`
      * 模块标题 (H2): `22px`
      * 卡片/弹窗标题: `18px`
      * 正文内容: `16px`
      * 辅助文字: `14px`

**3. 界面元素风格 (Component Styles)**

  * **按钮 (Buttons)**:
      * 主按钮 (`一键生成PPT`): 使用品牌色 `#3A57E8` 实心填充，白色文字，`6px` 圆角。
      * 次要按钮: 白色背景，品牌色边框和文字。
  * **卡片 (Cards)**:
      * 使用辅助背景色 `#F8F9FA`，`1px` 的浅灰色边框。
      * 默认无阴影，保持界面扁平。鼠标悬浮(Hover)时，添加轻微、柔和的阴影效果，提供交互反馈。
  * **弹窗 (Modals)**:
      * `12px` 圆角，具有清晰的标题区、内容区和操作区。
      * 内部使用充足的留白，避免信息拥挤。
  * **间距 (Spacing)**:
      * 遵循 8px 网格系统。所有元素的内外边距、间距都应是 8px 的倍数（如 8px, 16px, 24px, 32px），以保证布局的和谐与一致性。

-----

#### **第二部分：前端技术栈与架构 (Tech Stack & Architecture)**

基于Vue生态，我们选择一套现代、高效的工具链。

**1. 核心技术栈**

  * **框架 (Framework)**: **Vue 3**。使用其强大的组合式API (Composition API) 来组织逻辑。
  * **构建工具 (Build Tool)**: **Vite**。提供闪电般的启动速度和热更新，极大提升开发体验。
  * **CSS方案**: **Tailwind CSS**。
      * **理由**: 这是实现我们“简洁学术风格”的最佳选择。它让我们能够1:1还原设计稿，而无需与组件库的默认样式作斗争，保证了视觉的独特性和精致度。
  * **组件库 (Headless UI)**: **Headless UI**。
      * **理由**: 它是 Tailwind CSS 的完美搭档。它提供了无样式的、功能完备且符合无障碍标准(a11y)的组件逻辑（如弹窗、Tabs），让我们可以专注于用Tailwind CSS打造我们自己的外观。
  * **状态管理 (State Management)**: **Pinia**。
      * **理由**: Vue 官方推荐的新一代状态管理器，轻量、直观，完美契合Vue 3的组合式API。我们将用它来管理任务列表的状态轮询。
  * **HTTP客户端 (API Client)**: **Axios**。封装后用于与后端API进行通信。

**2. 项目结构规划**

```
/src
|-- /api               # 封装 Axios 请求
|   |-- index.js
|   |-- taskService.js
|-- /assets            # 静态资源 (CSS, fonts, images)
|-- /components        # 可复用的UI组件
|   |-- /common        #   通用组件 (Button.vue, Modal.vue)
|   |-- /core          #   核心业务组件 (PaperCard.vue, UploadDropzone.vue, TaskItem.vue)
|-- /composables       # 存放组合式函数 (逻辑复用)
|   |-- useTaskHistory.js # 封装与 localStorage 交互的逻辑
|-- /stores            # Pinia store 模块
|   |-- tasks.js       # 管理任务列表和状态轮询
|-- /views             # 页面级组件 (虽然是单页，但可将主页视为一个View)
|   |-- HomeView.vue
|-- App.vue            # 根组件
|-- main.js            # 应用入口
```

-----

#### **第三部分：核心功能开发路线图 (Development Roadmap)**

这是一个建议的、循序渐进的开发步骤：

1.  **步骤一：项目初始化与环境搭建 (1-2天)**

      * 使用 `npm create vite@latest` 初始化 Vue 3 + Vite 项目。
      * 集成 Tailwind CSS, Headless UI, Pinia, Axios。
      * 配置好项目结构，定义ESLint等代码规范。

2.  **步骤二：静态页面布局 (2-3天)**

      * 不处理任何逻辑，仅使用 Tailwind CSS 将高保真设计稿转化为静态的 `HomeView.vue` 页面。
      * 构建出 Header, Footer, “发现论文区”, “上传区”, “任务历史区” 的静态外观。

3.  **步骤三：核心组件开发 (3-5天)**

      * 开发 `PaperCard.vue` 组件，并用假数据渲染出列表。
      * 开发 `UploadDropzone.vue` 组件，实现文件的选择和拖拽效果。
      * 开发 `TaskItem.vue` 组件，展示不同状态（生成中、已完成、失败）的样式。
      * 开发 `Modal.vue` 弹窗组件，并构建其内部的静态布局。

4.  **步骤四：核心逻辑与状态管理 (3-4天)**

      * 在 `composables/useTaskHistory.js` 中，封装对 `localStorage` 的增、删、改、查操作，使其成为响应式的。
      * 在 `stores/tasks.js` 中，创建 Pinia store，定义 `tasks` 列表，并编写一个 `action` 来启动/停止对后端API的状态轮询。
      * 将 `useTaskHistory` 与 Pinia store 结合，实现任务历史的持久化和状态的实时更新。

5.  **步骤五：API集成与联调 (2-3天)**

      * 在 `api/` 目录下，根据后端接口文档，封装所有API请求函数。
      * 将所有假数据替换为真实的API调用。
      * 联调文件上传、任务创建、状态查询、PPT下载等全流程。

6.  **步骤六：细节打磨与测试 (2-3天)**

      * 添加所有过渡动画和微交互，提升产品质感。
      * 处理所有边界情况，如API请求失败、上传文件格式错误、任务历史为空等。
      * 进行全面的功能测试，确保流程顺畅。

**总计预估：约13-20个工作日。**

-----