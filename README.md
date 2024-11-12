# Code Share

一个在线代码分享平台，支持多种编程语言的代码片段分享和在线预览。

## 项目架构

### 前端 ([code-share](https://github.com/dnslin/code-share))
- 框架：Vue 3
- 构建工具：Vite
- 包管理器：pnpm
- Node 版本：20.x

### 后端 ([code-share-backend](https://github.com/dnslin/code-share-backend))
- 框架：FastAPI
- 数据库：SQLite
- Python 版本：3.9

### 部署架构

```ascii
┌─────────────┐ ┌─────────────┐
│ Caddy │ --> │ FastAPI │
│ 反向代理 │ │ 后端服务 │
└─────────────┘ └─────────────┘
│ │
│ │
▼ ▼
┌─────────────┐ ┌─────────────┐
│ 静态文件 │ │ SQLite │
│ (前端) │ │ 数据库 │
└─────────────┘ └─────────────┘
```



## 技术依赖

### 后端依赖

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.1
pydantic-settings==2.0.3
python-dotenv==1.0.0
shortuuid==1.0.11
```



## API 接口

### 代码片段相关
- `POST /api/code` - 创建新的代码片段
- `GET /api/code/{id}` - 获取指定代码片段
- `GET /api/codes` - 获取代码片段列表
- `DELETE /api/code/{id}` - 删除指定代码片段

### 用户相关
- `POST /api/user/register` - 用户注册
- `POST /api/user/login` - 用户登录
- `GET /api/user/profile` - 获取用户信息

## 构建和部署

### 本地开发

1. 克隆前端仓库

```bash
git clone https://github.com/dnslin/code-share.git
cd code-share
pnpm install
pnpm dev
```

2. 克隆后端仓库

```bash
git clone https://github.com/dnslin/code-share-backend.git
cd code-share-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```


### Docker 部署
1. 拉取镜像

```bash
docker pull dnslin/code-share:latest
```

2. 运行容器

```bash
docker run -d -p 80:80 dnslin/code-share:latest
```


### 自动构建

项目使用 GitHub Actions 进行自动构建和发布：
- 当代码推送到 main 分支时自动触发构建
- 构建完成后自动推送到 Docker Hub
- 支持多平台部署

## 项目结构

```bash
code-share-backend/
├── app/
│ ├── api/
│ │ └── endpoints/
│ ├── core/
│ ├── crud/
│ ├── models/
│ ├── schemas/
│ └── main.py
├── .github/
│ └── workflows/
│ └── ci.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 环境变量

创建 `.env` 文件：

```env
DATABASE_URL=sqlite:///./code_share.db
SECRET_KEY=your-secret-key
DEBUG=True
```


## 开发指南

1. 代码规范
   - 使用 Black 格式化 Python 代码
   - 使用 ESLint 和 Prettier 格式化前端代码

2. 提交规范
   - feat: 新功能
   - fix: 修复问题
   - docs: 文档修改
   - style: 代码格式修改
   - refactor: 代码重构
   - test: 测试用例修改
   - chore: 其他修改

## 许可证

[MIT License](LICENSE)

## 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交代码
4. 创建 Pull Request

## 联系方式

- 作者：[dnslin](https://github.com/dnslin)
- 邮箱：[dnslin@outlook.com](mailto:i@dnsl.in)
- 项目地址：[GitHub Repository URL](https://github.com/dnslin/code-share)