from fastapi import FastAPI
from app.routers import spec, case, run
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI 自动化测试平台")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定 ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spec.router)
app.include_router(case.router)
app.include_router(run.router)


@app.get("/")
async def root():
    return {"message": "欢迎使用 AI 自动化测试平台"}
