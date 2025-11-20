import json
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime
from backend.utils.response_util import success, fail
from backend.services.spec_parser import parse_openapi_spec
from flask import Blueprint, request, jsonify, render_template
from backend.services.api_generator_cases import generate_basic_cases

api_bp = Blueprint("api", __name__)

UPLOAD_DIR = Path("backend/uploads")
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

        file_path = UPLOAD_DIR / file.filename

        # # ✅ 可选：清空旧文件
        # for f in UPLOAD_DIR.iterdir():
        #     try:
        #         f.unlink()
        #     except Exception as e:
        #         print(f"⚠️ 删除旧文件失败：{f}, 错误: {e}")

        # ✅ 保存文件
        file.save(file_path)
        print(f"📄 文件已保存: {file_path}")

        # ✅ 解析内容
        try:
            parsed_result = parse_openapi_spec(file_path)
            print(f"✅ 成功解析 {len(parsed_result)} 个接口")
            print(f"接口列表: {parsed_result}")
        except Exception as e:
            return jsonify(fail(f"解析失败: {str(e)}"))

        # ✅ 返回结果
        return jsonify(
            success(
                {
                    "file_id": 1,
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
        print(os.getcwd())
        case_dir = "test_case\interface_case"

        if not os.path.exists(case_dir):
            return jsonify(fail(f"Case directory not found: {case_dir}")), 404

        print(f"🚀 开始执行目录下的测试用例：{case_dir}")

        start_time = time.time()
        reports = []

        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = report_dir / f"report_{timestamp}.json"
        latest_path = report_dir / "latest_report.json"


        # 设置环境变量
        os.environ["PYTHONPATH"] = "D:\\PytestAutoApi"

        # 执行Python脚本
        subprocess.run(["python", ".\\run_test.py"])

        # 更新 latest_report.json
        if report_path.exists():
            latest_path.write_text(report_path.read_text(), encoding="utf-8")
            print(f"✅ 测试完成，报告已生成：{latest_path}")
        else:
            print("❌ 未生成报告，请检查 pytest-json-report 插件是否安装")

        elapsed = round(time.time() - start_time, 2)
        print(f"✅ 所有测试执行完成，用时：{elapsed}s")

        test_files = []
        for root, dirs, files in os.walk(case_dir):
            for f in files:
                if f.endswith(".py"):
                    test_files.append(
                        {
                            "name": os.path.join(root, f),
                            "status": "成功",
                            "duration": elapsed,
                            "message": "成功",
                        }
                    )
                    print(os.path.join(root, f))
        # 解析测试报告
        report_json = json.loads(latest_path.read_text(encoding='utf-8'))

        summary = report_json.get("summary", {})


        return jsonify(
            success(
                {
                    "case_name": "AI生成测试用例执行结果",
                    "total_files": len(reports),
                    "test_files": test_files,
                    "summary": summary,

                }
            )
        )

    except Exception as e:
        return jsonify(fail(f"执行阶段错误: {str(e)}")), 500


@api_bp.route("/generate/<file_name>", methods=["GET"])
def generate_cases(file_name):
    """生成测试用例"""
    try:
        print(f"📄 生成测试用例，使用文件：{file_name}")
        # 检查文件是否存在
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if not os.path.exists(file_path):
            return jsonify(fail(f"文件 {file_name} 不存在")), 404

        # 解析接口文档
        apis = parse_openapi_spec(file_path)

        # 设置输出目录
        output_dir = os.path.join("data\interface_data", os.path.splitext(file_name)[0])
        print(f"📁 测试用例输出目录：{output_dir}")

        # 生成用例
        path = generate_basic_cases(apis, output_dir)
        return jsonify(success({"generated_case_file": path}))

    except Exception as e:
        return jsonify(fail(f"Error generating test cases: {str(e)}")), 500


@api_bp.route("/files", methods=["GET"])
def get_files():
    """获取上传文件列表"""
    try:
        files = []
        for f in os.listdir(UPLOAD_DIR):
            if f.endswith((".yaml", ".yml")):
                files.append(
                    {
                        "file_name": f,
                        "file_path": str(UPLOAD_DIR / f),
                        "upload_time": os.path.getmtime(UPLOAD_DIR / f),
                    }
                )
        return jsonify(success({"files": files}))
    except Exception as e:
        return jsonify(fail(f"Error getting file list: {str(e)}")), 500


@api_bp.route("/delete_file/<file_name>", methods=["DELETE"])
def delete_file(file_name):
    """删除上传文件"""
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify(success(f"文件 {file_name} 删除成功"))
        else:
            return jsonify(fail(f"文件 {file_name} 不存在"))
    except Exception as e:
        return jsonify(fail(f"Error deleting file: {str(e)}")), 500


@api_bp.route("/case_content", methods=["GET"])
def get_case_content():
    """
    获取单个 YAML 文件内容
    参数:file_path=/xxx/xxx.yaml
    """

    file_path = request.args.get("file_path")
    if not file_path or not os.path.exists(file_path):
        return jsonify(fail("File not found")), 404

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify(success({"content": content}))


@api_bp.route("/cases", methods=["GET"])
def get_cases():
    """
    获取测试用例列表（支持：分页、排序、按文档筛选）
    参数示例：
        ?page=1&size=10&sort_by=update_time&order=desc&source_file=auth-ali.yaml
    """

    try:
        case_dir = "data/interface_data"
        if not os.path.exists(case_dir):
            return jsonify(fail(f"Case directory not found: {case_dir}")), 404

        # ----- 获取查询参数 -----
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
        sort_by = request.args.get("sort_by", "update_time")  # file_name / update_time
        order = request.args.get("order", "desc")  # asc / desc
        source_file = request.args.get("source_file")  # 对应文档来源

        cases = []

        # ----- 遍历所有 YAML 文件 -----
        for root, _, files in os.walk(case_dir):
            for f in files:
                if not f.endswith(".yaml"):
                    continue

                full_path = os.path.join(root, f)
                stat = os.stat(full_path)

                case_info = {
                    "file_name": f,
                    "file_path": full_path.replace("\\", "/"),
                    "update_time": stat.st_mtime,
                    "update_time_str": datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }

                # 解析来源文档：如 xxx_auth-ali.yaml → auth-ali.yaml
                if "_" in f:
                    case_info["source_file"] = f.split("_")[0] + ".yaml"
                else:
                    case_info["source_file"] = None

                # 如果前端筛选来源文档
                if source_file and case_info["source_file"] != source_file:
                    continue

                cases.append(case_info)

        # ----- 排序 -----
        reverse = True if order == "desc" else False
        if sort_by == "file_name":
            cases.sort(key=lambda x: x["file_name"], reverse=reverse)
        elif sort_by == "update_time":
            cases.sort(key=lambda x: x["update_time"], reverse=reverse)

        # ----- 分页 -----
        total = len(cases)
        start = (page - 1) * size
        end = start + size
        paged_cases = cases[start:end]

        return jsonify(
            success(
                {
                    "total": total,
                    "page": page,
                    "size": size,
                    "cases": paged_cases,
                }
            )
        )

    except Exception as e:
        return jsonify(fail(f"Error getting case list: {str(e)}")), 500


@api_bp.route("/generate_case", methods=["GET"])
def generate_case():
    """
    生成测试用例
    参数：
        file_path: 接口文档路径
        output_dir: 输出目录
    """
    from backend.utils.case_control import TestCaseAutomaticGeneration

    try:
        print("开始生成测试用例...")
        TestCaseAutomaticGeneration().get_case_automatic(
            yaml_files_dir="data\interface_data", cases_dir="test_case\interface_case"
        )
        print("生成测试用例成功")
        return jsonify(success("生成测试用例成功"))
    except Exception as e:
        return jsonify(fail(f"Error generating test case: {str(e)}")), 500
