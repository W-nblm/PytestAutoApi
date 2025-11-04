from fastapi import APIRouter, UploadFile
from app.services.spec_parser import parse_openapi_spec
import os, uuid

UPLOAD_DIR = "app/uploads/specs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/spec", tags=["spec"])


@router.post("/upload")
async def upload_spec(file: UploadFile):
    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    # 清空上传目录旧文件（可选）
    for f in os.listdir(UPLOAD_DIR):
        os.remove(os.path.join(UPLOAD_DIR, f))

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 解析文件内容
    result = parse_openapi_spec(open(file_path, "rb").read())

    return {
        "file_id": file_id,
        "file_name": file.filename,
        "file_path": file_path,
        "parsed_paths": result,
    }
