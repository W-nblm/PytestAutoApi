
from io import BytesIO
from openpyxl import Workbook
import json,re
from google import genai

client = genai.Client(api_key="AIzaSyCmAo52ridCff1Ix6AvdHpzDenC5mW2nys")

def process_test_cases(text):
    # 提取 JSON 内容
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)

    if not match:
        return None

    json_content = match.group(1)

    try:
        test_cases = json.loads(json_content)

        return test_cases

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None


def generate_test_cases(document_text: str):
    """调用 AI 生成测试用例"""
    prompt = f"""
你是一位资深测试架构师。请根据以下需求文档内容生成测试用例：
只输出 JSON 格式不包含其它多余的内容，每个元素包括：
[{{"用例标题":"","前置条件":"","测试步骤":[],"预期结果":"","优先级":"","测试类型":""}}]
---
{document_text}
---
"""
    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
    return process_test_cases(response.text.strip())


def export_to_excel(cases):
    wb = Workbook()
    ws = wb.active
    ws.title = "测试用例"
    headers = ["用例标题", "前置条件", "测试步骤", "预期结果", "优先级", "测试类型"]
    ws.append(headers)
    for c in cases:
        ws.append(
            [
                c.get("用例标题", ""),
                c.get("前置条件", ""),
                "\n".join(c.get("测试步骤", [])),
                c.get("预期结果", ""),
                c.get("优先级", ""),
                c.get("测试类型", ""),
            ]
        )
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf