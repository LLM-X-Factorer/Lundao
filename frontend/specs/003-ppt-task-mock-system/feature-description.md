# Feature Description: PPT任务Mock系统

## Feature ID
003-ppt-task-mock-system

## Problem Statement

当前的PPT生成和任务历史功能缺少mock数据支持，导致纯前端开发环境下无法展示完整的业务流程：

1. **PPT生成功能**：点击"一键生成组会PPT"后直接调用真实API，在mock模式下会弹框报错
2. **任务历史功能**：TaskHistory组件空空如也，无法展示任务状态演进过程
3. **开发体验断裂**：Paper discovery有完善的mock支持（paperData.js），但PPT功能没有，导致前端开发体验不一致
4. **产品演示受阻**：无法在没有后端的情况下完整演示PPT生成流程

## Goals

### Primary Goals
1. 实现完整的PPT任务Mock系统，支持任务创建、状态轮询、历史展示
2. 模拟真实的任务状态演进：queued → generating → completed
3. 提供历史任务mock数据，展示不同状态的任务（completed, failed）
4. 与现有mock系统保持架构一致性（参考paperData.js模式）

### Success Metrics
- ✅ 点击"生成PPT"在mock模式下不报错，能创建任务
- ✅ 任务状态能自动演进（15秒内从queued到completed）
- ✅ 任务历史展示至少3条历史任务+动态创建的任务
- ✅ 进度条平滑增长（0% → 100%）
- ✅ 刷新页面后任务持久化存在（localStorage）

## User Stories

### US1: 开发者 - Mock模式下创建PPT任务
**As a** 前端开发者
**I want to** 在mock模式下点击"生成PPT"能成功创建任务
**So that** 我可以独立于后端开发和测试PPT生成功能

**Acceptance Criteria:**
- [ ] 点击"一键生成组会PPT"后不报错
- [ ] 显示Toast提示"PPT生成任务已创建"
- [ ] Modal自动关闭
- [ ] TaskHistory中出现新任务，状态为queued
- [ ] 任务信息包含论文标题、创建时间

### US2: 用户 - 观察任务状态演进
**As a** 用户
**I want to** 看到任务状态从排队到生成中到完成的过程
**So that** 我能了解PPT生成的进度

**Acceptance Criteria:**
- [ ] 任务创建后初始状态为queued（0-5秒）
- [ ] 5秒后状态变为generating，显示进度条（0-90%）
- [ ] 15秒后状态变为completed，进度条100%
- [ ] completed状态显示"下载PPT"按钮
- [ ] 状态变化无需手动刷新（轮询自动更新）

### US3: 用户 - 查看历史任务
**As a** 用户
**I want to** 看到之前创建的PPT任务历史
**So that** 我可以下载之前生成的PPT或查看失败原因

**Acceptance Criteria:**
- [ ] 首次进入mock模式时显示3条历史任务
- [ ] 历史任务包含：2条completed + 1条failed
- [ ] 每条任务显示论文标题、状态、创建时间
- [ ] completed任务显示"下载PPT"按钮
- [ ] failed任务显示错误信息和"重试"按钮
- [ ] 刷新页面后历史任务仍然存在

### US4: 开发者 - Mock/Real模式切换
**As a** 开发者
**I want to** 通过环境变量控制使用mock还是真实API
**So that** 我可以轻松在开发和生产环境之间切换

**Acceptance Criteria:**
- [ ] `VITE_USE_MOCK_DATA=true` 使用mock任务系统
- [ ] `VITE_USE_MOCK_DATA=false` 使用真实API
- [ ] 切换环境变量后无需修改代码
- [ ] Mock模式下在console显示警告信息

## Technical Context

### Existing Architecture
- **Mock系统**: `src/mocks/paperData.js` 提供论文mock数据
- **API层**: `src/api/taskService.js` - createPPTTask, pollTaskStatus
- **Store**: `src/stores/tasks.js` - 任务状态管理和轮询
- **Components**:
  - `PaperModal.vue` - 包含"生成PPT"按钮
  - `TaskHistory.vue` - 任务历史列表
  - `TaskItem.vue` - 单个任务展示

### Constraints
1. 必须与现有mock系统架构保持一致（参考paperData.js模式）
2. 不能修改API契约（taskId格式、响应结构等）
3. 必须支持localStorage持久化
4. 轮询间隔保持5秒（与现有逻辑一致）

## Out of Scope
- 生成真实的PPTX文件（mock模式只提供下载链接占位符）
- 任务重试逻辑优化（使用现有retryTask方法）
- 任务过期自动删除（>24小时，当前已有清理机制）
- 高级配置（自定义状态演进时间）

## Dependencies
- Pinia store (tasks.js)
- Axios API client
- localStorage composable (useTaskHistory)
- 现有mock系统 (paperData.js)

## References
- Design document: `docs/ppt-task-mock-design.md`
- Current implementation: `src/stores/tasks.js`, `src/api/taskService.js`
- Mock pattern reference: `src/mocks/paperData.js`
