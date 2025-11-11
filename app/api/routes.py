from time import time
from flask import Blueprint, request, jsonify, render_template
from services.spec_parser import parse_openapi_spec
from utils.response_util import success, fail
from pathlib import Path
import uuid
import os
from services.runner import run_yaml_cases
from services.case_generator import generate_basic_cases
from services.spec_parser import parse_openapi_spec

api_bp = Blueprint("api", __name__)

UPLOAD_DIR = Path("app/uploads/specs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@api_bp.route("/")
def api():
    return render_template("api/api_case.html")


@api_bp.route("/upload", methods=["POST"])
def upload_api():
    """上传并解析 OpenAPI 文件"""
    try:
        # ✅ 检查是否有文件上传
        if "file" not in request.files:
            return jsonify(fail("未检测到文件"))

        file = request.files["file"]
        if file.filename == "":
            return jsonify(fail("文件名不能为空"))

        # ✅ 检查文件类型
        if not file.filename.endswith((".yaml", ".yml", ".json")):
            return jsonify(fail("仅支持 YAML 或 JSON 文件"))

        # ✅ 生成唯一文件名
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"

        # ✅ 可选：清空旧文件
        for f in UPLOAD_DIR.iterdir():
            try:
                f.unlink()
            except Exception as e:
                print(f"⚠️ 删除旧文件失败：{f}, 错误: {e}")

        # ✅ 保存文件
        file.save(file_path)
        print(f"📄 文件已保存: {file_path}")

        # ✅ 解析内容
        try:
            content = file_path.read_bytes()
            parsed_result = parse_openapi_spec(content)
            print(f"✅ 成功解析 {len(parsed_result)} 个接口")
        except Exception as e:
            return jsonify(fail(f"解析失败: {str(e)}"))

        # ✅ 返回结果
        return jsonify(
            success(
                {
                    "file_id": file_id,
                    "file_name": file.filename,
                    "file_path": str(file_path),
                    "total_endpoints": len(parsed_result),
                    "parsed_paths": parsed_result,
                }
            )
        )

    except Exception as e:
        return jsonify(fail(f"文件上传失败: {str(e)}"))


@api_bp.route("/execute", methods=["POST"])
def execute_cases():
    """执行 AI 生成的测试用例"""
    try:
        case_dir = "interface_data"
        if not os.path.exists(case_dir):
            return jsonify(fail(f"Case directory not found: {case_dir}")), 404

        print(f"🚀 开始执行目录下的测试用例：{case_dir}")
        start_time = time.time()
        reports = []

        for f in os.listdir(case_dir):
            if f.endswith(".py"):
                file_path = os.path.join(case_dir, f)
                print(f"▶️ 执行测试用例：{file_path}")
                try:
                    report_path = run_yaml_cases(file_path)
                    reports.append(
                        {"file": f, "report_path": report_path, "status": "success"}
                    )
                except Exception as e:
                    print(f"❌ 执行失败：{file_path}, 错误：{e}")
                    reports.append(
                        {
                            "file": f,
                            "report_path": None,
                            "status": "failed",
                            "error": str(e),
                        }
                    )

        elapsed = round(time.time() - start_time, 2)
        print(f"✅ 所有测试执行完成，用时：{elapsed}s")

        return jsonify(
            success(
                {
                    "total_files": len(reports),
                    "elapsed_time": elapsed,
                    "reports": reports,
                }
            )
        )

    except Exception as e:
        return jsonify(fail(f"执行阶段错误: {str(e)}")), 500


@api_bp.route("/generate", methods=["POST"])
def generate_cases():
    """生成测试用例"""
    try:
        # 检查文件是否存在
        matched_files = [
            f for f in os.listdir(UPLOAD_DIR) if f.endswith((".yaml", ".yml"))
        ]
        if not matched_files:
            return jsonify(fail("No spec file found in upload directory")), 404

        file_path = os.path.join(UPLOAD_DIR, matched_files[0])

        # 解析接口文档
        with open(file_path, "rb") as f:
            apis = parse_openapi_spec(f.read())

        # 生成用例
        path = generate_basic_cases(apis)
        return jsonify(success({"generated_case_file": path}))

    except Exception as e:
        return jsonify(fail(f"Error generating test cases: {str(e)}")), 500


# @api_bp.route("/execute", methods=["POST"])
# def execute_cases():
#     """执行 AI 生成的测试用例"""
#     try:
#         case_dir = "interface_data"
#         if not os.path.exists(case_dir):
#             return jsonify(fail(f"Case directory not found: {case_dir}")), 404

#         print(f"🚀 开始执行目录下的测试用例：{case_dir}")
#         start_time = time.time()
#         reports = []

#         for f in os.listdir(case_dir):
#             if f.endswith(".py"):
#                 file_path = os.path.join(case_dir, f)
#                 print(f"▶️ 执行测试用例：{file_path}")
#                 try:
#                     report_path = run_yaml_cases(file_path)
#                     reports.append(
#                         {"file": f, "report_path": report_path, "status": "success"}
#                     )
#                 except Exception as e:
#                     print(f"❌ 执行失败：{file_path}, 错误：{e}")
#                     reports.append(
#                         {
#                             "file": f,
#                             "report_path": None,
#                             "status": "failed",
#                             "error": str(e),
#                         }
#                     )

#         elapsed = round(time.time() - start_time, 2)
#         print(f"✅ 所有测试执行完成，用时：{elapsed}s")

#         return jsonify(
#             success(
#                 {
#                     "total_files": len(reports),
#                     "elapsed_time": elapsed,
#                     "reports": reports,
#                 }
#             )
#         )

#     except Exception as e:
#         return jsonify(fail(f"执行阶段错误: {str(e)}")), 500
