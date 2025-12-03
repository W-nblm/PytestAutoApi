from flask import Blueprint, render_template, request, jsonify, send_file
from datetime import datetime
import os, json, re

from docx import Document
from backend.services.function_generator_cases import (
    generate_test_cases,
    export_to_excel,
)
from backend.utils.response_util import success

function_bp = Blueprint("function", __name__)


DATA_DIR = "backend\data"
CASE_DIR = os.path.join(DATA_DIR, "cases")
INDEX_FILE = os.path.join(DATA_DIR, "index.json")
os.makedirs(CASE_DIR, exist_ok=True)


def extract_text(file):
    if file.filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file.filename.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""


# ========== 路由部分 ==========


@function_bp.route("/")
def index():
    """主页：上传、查看历史"""
    index = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)
    return render_template("function/index.html", cases=index)


@function_bp.route("/cases")
def cases():
    """主页：上传、查看历史"""
    index = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)
    return jsonify(success(data=index))


@function_bp.route("/generate", methods=["POST"])
def generate():
    """AI 生成测试用例"""
    file = request.files.get("file")
    text = request.form.get("text", "")
    title = request.form.get("title", "未命名用例集")

    document_text = extract_text(file) if file else text
    if not document_text.strip():
        return jsonify({"error": "没有输入内容"}), 400

    print("start generate...")
    cases = generate_test_cases(document_text)
    print("generate finished.")

    if not cases:
        return jsonify({"error": "生成失败"}), 500

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_path = os.path.join(CASE_DIR, f"{timestamp}_{title}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)

    index = []
    if os.path.exists(INDEX_FILE):
        index = json.load(open(INDEX_FILE, "r", encoding="utf-8"))
    index.append(
        {"title": title, "timestamp": timestamp, "count": len(cases), "path": json_path}
    )
    json.dump(
        index, open(INDEX_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2
    )

    return jsonify({"title": title, "timestamp": timestamp, "count": len(cases)})


@function_bp.route("/download/<timestamp>")
def download(timestamp):
    """下载 Excel"""
    index = json.load(open(INDEX_FILE, "r", encoding="utf-8"))
    item = next((i for i in index if i["timestamp"] == timestamp), None)
    if not item:
        return "Not Found", 404
    cases = json.load(open(item["path"], "r", encoding="utf-8"))
    buf = export_to_excel(cases)
    return send_file(buf, as_attachment=True, download_name=f"{item['title']}.xlsx")


@function_bp.route("/delete/<timestamp>", methods=["DELETE"])
def delete(timestamp):
    """删除用例"""
    index = json.load(open(INDEX_FILE, "r", encoding="utf-8"))
    new_index = []
    for item in index:
        if item["timestamp"] == timestamp:
            os.remove(item["path"])
        else:
            new_index.append(item)
    json.dump(
        new_index, open(INDEX_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2
    )
    return jsonify({"success": True})

@function_bp.route("/case_detail/<timestamp>")
def case_detail(timestamp):
    """查看单个用例详情"""
    if not os.path.exists(INDEX_FILE):
        return "No records found", 404

    index = json.load(open(INDEX_FILE, "r", encoding="utf-8"))
    item = next((i for i in index if i["timestamp"] == timestamp), None)
    if not item:
        return "Case not found", 404
    with open(item["path"], "r", encoding="utf-8") as f:
        cases = json.load(f)

    return success(data=cases)

@function_bp.route("/view/<timestamp>")
def view_case(timestamp):
    """查看单个用例详情"""
    if not os.path.exists(INDEX_FILE):
        return "No records found", 404

    index = json.load(open(INDEX_FILE, "r", encoding="utf-8"))
    item = next((i for i in index if i["timestamp"] == timestamp), None)
    if not item:
        return "Case not found", 404

    with open(item["path"], "r", encoding="utf-8") as f:
        cases = json.load(f)

    return render_template("function/view_case.html", case_set=item, cases=cases)
