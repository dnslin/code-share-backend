from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api.endpoints import snippets, items

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Code-Share")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(snippets.router, prefix="/api/snippets", tags=["snippets"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Code-Share"}

@app.get("/health")
def health_check():
    return {"status": "healthy"} 