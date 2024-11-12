FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Caddy
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && \
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list && \
    apt-get update && \
    apt-get install -y caddy && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制后端代码
COPY . /app/

# 复制前端构建文件
COPY frontend-dist /srv

# 复制 Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# 升级 pip
RUN pip install --no-cache-dir --upgrade pip

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 80

# 启动服务
CMD caddy run --config /etc/caddy/Caddyfile --adapter caddyfile & uvicorn main:app --host 0.0.0.0 --port 8000 