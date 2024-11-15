# 构建阶段
FROM python:3.9-slim-buster AS builder

# 只安装必要的构建依赖
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 最终阶段
FROM python:3.9-slim-buster

# 安装系统依赖和 Caddy
RUN apt-get update && apt-get install -y \
    curl \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update \
    && apt-get install -y caddy \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 设置工作目录
WORKDIR /app

# 创建数据目录
RUN mkdir -p /app/data

# 复制应用文件
COPY . /app/

# 复制前端构建文件
COPY frontend-dist /srv

# 复制 Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 80

# 启动服务
CMD ["sh", "-c", "caddy run --config /etc/caddy/Caddyfile --adapter caddyfile & uvicorn app.main:app --host 0.0.0.0 --port 8000"]