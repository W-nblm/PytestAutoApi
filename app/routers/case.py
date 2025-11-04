from fastapi import APIRouter, Query, HTTPException
from app.services.case_generator import generate_basic_cases
from app.services.spec_parser import parse_openapi_spec
from app.utils.response_util import success, fail
import os

UPLOAD_DIR = "app/uploads/specs"

router = APIRouter(prefix="/case", tags=["case"])


@router.post("/generate")
async def generate():
    # 找到对应文件
    try:
        matched_files = [f for f in os.listdir(UPLOAD_DIR)]

        if not matched_files:
            raise HTTPException(status_code=404, detail="Spec file not found")

        file_path = os.path.join(UPLOAD_DIR, matched_files[0])

        # 解析并生成用例
        apis = parse_openapi_spec(open(file_path, "rb").read())
        print(apis)
        path = generate_basic_cases(apis)
        return success({"generated_case_file": path})
    except Exception as e:
        return fail(str(e))
