from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="角色扮演游戏API",
    description="Web角色扮演游戏后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查路由
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 根路由
@app.get("/")
def read_root():
    return {"message": "欢迎使用角色扮演游戏API"}

# 启动事件
@app.on_event("startup")
async def startup_event():
    try:
        from app.database_init import init_db
        init_db()
        print("数据库初始化成功！")
    except Exception as e:
        print(f"数据库初始化失败: {e}")

# 导入路由
from app.api import router as api_router
app.include_router(api_router)
