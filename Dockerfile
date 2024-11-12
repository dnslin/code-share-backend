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

# 安装 Caddy
RUN apt-get update && apt-get install -y \
    curl \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update \
    && apt-get install -y caddy \
    && apt-get remove -y curl debian-keyring debian-archive-keyring apt-transport-https \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 设置工作目录
WORKDIR /app

# 复制应用文件
COPY . /app/

# 复制前端构建文件
COPY frontend-dist /srv

# 复制 Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# 暴露端口
EXPOSE 80

# 使用 JSON 格式的 CMD 指令
CMD ["sh", "-c", "caddy run --config /etc/caddy/Caddyfile --adapter caddyfile & uvicorn main:app --host 0.0.0.0 --port 8000"]