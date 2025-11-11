import json
from pathlib import Path

def load_test_report(report_path: str):
    """
    加载 pytest 或自定义执行报告，返回统一结构的 dict
    支持 JSON 格式报告
    """
    path = Path(report_path)
    if not path.exists():
        raise FileNotFoundError(f"报告文件不存在: {path}")

    # 读取文件
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"报告文件格式错误（应为JSON）: {path}")

    # 标准化结构（确保包含 tests 列表）
    if "tests" not in data:
        # 兼容 pytest-html/pytest-json 结构
        if "results" in data:
            tests = data["results"]
        elif "items" in data:
            tests = data["items"]
        else:
            tests = []
        data = {"tests": tests}

    # 为每个 case 填充通用字段
    for case in data.get("tests", []):
        case.setdefault("name", case.get("nodeid", "unknown_case"))
        case.setdefault("status", case.get("outcome", "unknown"))
        case.setdefault("message", case.get("error", {}).get("message", ""))
        case.setdefault("duration", case.get("duration", 0))

    return data
