# 部署参考文档

论导Lite 前端项目支持多种部署方式，包括 Docker 容器化部署、静态托管部署和阿里云 ECS 部署。

## 📋 部署方案概览

| 方案 | 适用场景 | 优势 | 文档 |
|------|---------|------|------|
| **Docker 本地** | 开发/测试 | 环境一致、快速启动 | [DOCKER-DEPLOYMENT.md](../DOCKER-DEPLOYMENT.md) |
| **阿里云 ECS** | 生产环境 | 自托管、完全控制 | [ALIYUN-DEPLOYMENT.md](../ALIYUN-DEPLOYMENT.md) |
| **Netlify** | 演示/分享 | 零配置、自动 CI/CD | [DEPLOYMENT.md](../DEPLOYMENT.md) |
| **GitHub Pages** | 开源项目 | 免费托管 | [DEPLOYMENT.md](../DEPLOYMENT.md) |

---

## 🐳 Docker 部署

### 文件清单

| 文件 | 用途 |
|------|------|
| `Dockerfile` | 多阶段构建配置 (Node.js + Nginx) |
| `docker-compose.yml` | 双环境编排 (生产 + 演示) |
| `.dockerignore` | 构建上下文优化 |
| `nginx.conf` | Nginx 生产配置 |

### 快速启动

```bash
# 使用 Docker Compose（推荐）
docker-compose up -d              # 生产环境 (端口 8080)
docker-compose --profile demo up -d lundao-frontend-demo  # 演示环境 (端口 8081)

# 使用 npm scripts
npm run docker:build:prod         # 构建生产镜像
npm run docker:build:demo         # 构建演示镜像
npm run docker:compose:up         # 启动生产环境
npm run docker:compose:demo       # 启动演示环境
```

### 环境变量

构建时配置（通过 `--build-arg`）：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `VITE_USE_MOCK_DATA` | `false` | 是否使用 Mock 数据 |
| `VITE_API_BASE_URL` | `https://api.lundao.com/api` | 后端 API 地址 |
| `VITE_WATERMARK_ENABLED` | `true` | 是否启用水印 |
| `VITE_WATERMARK_TEXT` | `论导Lite` | 水印文本 |
| `VITE_WATERMARK_OPACITY` | `0.08` | 水印透明度 (0-1) |

### 镜像信息

- **基础镜像**: Node.js 20-alpine (构建阶段), Nginx 1.25-alpine (运行阶段)
- **镜像大小**: ~255 MB (未压缩)
- **构建时间**: 2-5 分钟
- **健康检查**: 每 30 秒检查 `/health` 端点

### 常用命令

```bash
# 查看容器状态
docker ps | grep lundao

# 查看日志
docker logs -f lundao-frontend

# 查看健康状态
docker inspect --format='{{.State.Health.Status}}' lundao-frontend

# 进入容器
docker exec -it lundao-frontend sh

# 重启容器
docker restart lundao-frontend

# 停止和删除
docker-compose down
```

---

## ☁️ 阿里云 ECS 部署

### 文件清单

| 文件 | 用途 |
|------|------|
| `deploy/deploy.sh` | 一键部署脚本 (200+ 行) |
| `deploy/update.sh` | 智能更新脚本 (100+ 行) |
| `deploy/nginx.conf` | Nginx 反向代理配置 |
| `deploy/README.md` | 脚本详细说明 |
| `deploy/QUICKSTART.md` | 快速开始指南 |

### 快速部署（3 步，5 分钟）

```bash
# 步骤 1: 上传项目到 ECS
scp -r Lundao-Lite-FrontEnd ecs-user@your-server-ip:~/

# 步骤 2: 执行部署脚本
ssh ecs-user@your-server-ip
cd ~/Lundao-Lite-FrontEnd
chmod +x deploy/deploy.sh
./deploy/deploy.sh demo  # 演示模式，或用 prod 生产模式

# 步骤 3: 配置 Nginx
sudo cp deploy/nginx.conf /etc/nginx/conf.d/lundao.conf
sudo nano /etc/nginx/conf.d/lundao.conf  # 修改域名
sudo nginx -t && sudo nginx -s reload
```

### 部署脚本功能

**deploy.sh** - 一键部署:
- ✅ 环境检查 (Docker 版本、端口占用)
- ✅ 停止旧容器
- ✅ 构建 Docker 镜像
- ✅ 启动新容器 (端口 8082)
- ✅ 健康检查验证
- ✅ 清理旧镜像

**update.sh** - 智能更新:
- ✅ 拉取最新代码 (Git)
- ✅ 自动备份当前容器
- ✅ 构建并启动新容器
- ✅ 失败自动回滚
- ✅ 成功后清理备份

### 端口配置

- **Docker 容器**: 8082 (避免与现有服务冲突)
- **Nginx 代理**: 80/443 (标准 HTTP/HTTPS)

### Nginx 配置特性

- ✅ 反向代理到 Docker 容器
- ✅ Gzip 压缩 (级别 6)
- ✅ 静态资源缓存 (1 年)
- ✅ 安全头部 (X-Frame-Options, XSS Protection)
- ✅ 健康检查端点 (`/health`)
- ✅ PDF 上传支持 (最大 20MB)
- ✅ HTTPS 配置模板

### HTTPS 配置

```bash
# 安装 Certbot
sudo yum install certbot python3-certbot-nginx

# 自动配置 HTTPS
sudo certbot --nginx -d lundao.yourdomain.com

# 测试自动续期
sudo certbot renew --dry-run
```

---

## 🌐 静态托管部署

### Netlify 部署

**方式 A: Netlify Drop（30 秒）**

1. 构建项目: `npm run build`
2. 访问 https://app.netlify.com/drop
3. 拖放 `dist` 文件夹
4. 获取分享链接

**方式 B: Netlify Git（自动部署）**

1. 连接 GitHub 仓库
2. 配置构建:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. 设置环境变量: `VITE_USE_MOCK_DATA=true`

### GitHub Pages 部署

```bash
# 修改 vite.config.js
export default defineConfig({
  base: '/Lundao-Lite-FrontEnd/',
  // ...
})

# 安装并部署
npm install --save-dev gh-pages
npm run build
npx gh-pages -d dist
```

---

## 🔧 环境配置

### 环境变量文件

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `.env.development` | 开发环境 | 低 |
| `.env.production` | 生产环境 | 中 |
| `.env.production.local` | 本地生产覆盖 (gitignored) | 高 |

### Mock 数据配置

项目支持智能 API Fallback 机制：

- `VITE_USE_MOCK_DATA=true`: 强制使用 Mock 数据
- `VITE_USE_MOCK_DATA=false`: 使用真实 API，失败时自动 Fallback 到 Mock

### 构建命令

```bash
npm run build           # 生产构建
npm run preview         # 预览生产构建
npm run docker:build    # Docker 镜像构建
```

---

## 📊 性能指标

### 构建产物

| 指标 | 数值 |
|------|------|
| 构建时间 | 2.72s |
| JS 产物 (原始) | 240.80 KB |
| JS 产物 (gzip) | 88.50 KB |
| CSS 产物 (原始) | 25.57 KB |
| CSS 产物 (gzip) | 5.34 KB |

### Docker 镜像

| 指标 | 数值 |
|------|------|
| 最终镜像大小 | ~255 MB |
| 构建阶段镜像 | ~1.2 GB (不计入最终镜像) |
| 启动时间 | <5 秒 |
| 健康检查间隔 | 30 秒 |

---

## 🐛 故障排查

### Docker 相关

**问题**: 容器无法启动

```bash
# 查看日志
docker logs lundao-frontend

# 检查端口占用
lsof -i :8082

# 重新构建（不使用缓存）
docker build --no-cache -t lundao-frontend:prod .
```

**问题**: 镜像构建失败

```bash
# 清理 Docker 缓存
docker system prune -a -f

# 检查磁盘空间
df -h
docker system df
```

### 阿里云 ECS 相关

**问题**: 无法访问应用

检查清单:
1. 容器运行: `docker ps | grep lundao`
2. 健康检查: `curl http://localhost:8082/health`
3. Nginx 配置: `sudo nginx -t`
4. 防火墙: `sudo firewall-cmd --list-all`
5. 安全组: 阿里云控制台检查 80/443 端口

**问题**: 部署脚本失败

```bash
# 查看详细错误
bash -x deploy/deploy.sh demo

# 手动执行各步骤
docker build -t lundao-frontend:demo .
docker run -d -p 8082:80 --name lundao-frontend lundao-frontend:demo
docker logs lundao-frontend
```

---

## 📝 最佳实践

### 开发环境

1. 使用 `npm run dev` 本地开发
2. 使用 Mock 数据: `VITE_USE_MOCK_DATA=true`
3. 定期测试 Docker 构建确保环境一致

### 测试环境

1. 使用 Docker Compose 演示模式
2. 启用 Mock 数据和演示水印
3. 验证所有功能正常工作

### 生产环境

1. 使用阿里云 ECS 或其他云服务器
2. 配置 Nginx 反向代理
3. 启用 HTTPS (Let's Encrypt)
4. 配置日志轮转和监控
5. 定期更新和备份

### 安全建议

1. ✅ 配置 HTTPS 证书
2. ✅ 启用安全头部
3. ✅ 限制 Nginx Rate Limiting
4. ✅ 定期更新 Docker 镜像
5. ✅ 配置防火墙规则
6. ✅ 开放必要端口 (80/443)

---

## 📚 相关文档

- **完整 Docker 指南**: [DOCKER-DEPLOYMENT.md](../DOCKER-DEPLOYMENT.md)
- **阿里云部署指南**: [ALIYUN-DEPLOYMENT.md](../ALIYUN-DEPLOYMENT.md)
- **部署方案总结**: [ALIYUN-DEPLOYMENT-SUMMARY.md](../ALIYUN-DEPLOYMENT-SUMMARY.md)
- **静态托管指南**: [DEPLOYMENT.md](../DEPLOYMENT.md)
- **项目架构**: [architecture.md](./architecture.md)

---

**更新时间**: 2025-11-18
**维护者**: DevOps Team
