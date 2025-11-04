from fastapi import APIRouter
from app.services.runner import run_yaml_cases
import os

router = APIRouter(prefix="/run", tags=["run"])


@router.post("/execute")
async def execute_cases():
    """执行 AI 生成的测试用例"""
    case_dir = "interface_data"
    print(f"开始执行目录下的测试用例：{case_dir}")
    report_path = ""
    # 便利生成的测试用例
    for f in os.listdir(case_dir):
        if f.endswith(".py"):
            file_path = os.path.join(case_dir, f)
            print(f"执行测试用例：{file_path}")
            report_path = run_yaml_cases(file_path)
        
    return {"report_path": report_path}
