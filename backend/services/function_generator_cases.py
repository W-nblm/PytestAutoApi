from io import BytesIO
from openpyxl import Workbook
import json, re
from google import genai

client = genai.Client(api_key="AIzaSyCmAo52ridCff1Ix6AvdHpzDenC5mW2nys")


def process_test_cases(text):

    try:
        test_cases = json.loads(text)

        return test_cases

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None


def generate_test_cases(document_text: str):
    """调用 AI 生成测试用例"""
    prompt = f"""
你是一位资深测试架构师。请根据以下需求文档内容生成测试用例：
1. 基于需求文档内容,尽可能详尽的分析出一下信息:
- "需求测试点": 根据需求内容总结出需求关键点
- "测试场景": 为每个需求测试点设计具体的测试场景,按次序分点列出,格式如下:
    1. 测试场景1: ......
    2. 测试场景2: ......
    3. 测试场景3: ......
    多个场景之间换行展示)
2. 将每个"需求测试点"及其对应的"测试场景"按照以下格式组织成一个JSON对象:
    - {{"用例标题":"","前置条件":[],"测试步骤":[],"预期结果":"","优先级":"","测试类型":""}}
3. 将生成的JSON对象append一个数组中
4. 支持分段输出：如果内容较多,可以分段输出,但每段输出的内容前后不要加任何分割符,确保最终拼接后是一个完整的、标准的JSON数组,内部不包含其他内容。
5. 最终仅返回该数组内容,输出结果不使用```json及```包裹,输出结果需为标准JSON格式。
---
{document_text}
---
"""

    response = client.models.generate_content(model="gemini-2.5-pro", contents=prompt)
    test_cases = process_test_cases(response.text.strip())
    if "这是第一部分" in response.text.strip():
        prompt = "继续生成剩余的测试用例内容，确保输出结果不使用```json及```包裹,输出结果需为标准JSON格式。"
        response = client.models.generate_content(
            model="gemini-2.5-pro", contents=prompt
        )
        test_cases.extend(process_test_cases(response.text.strip()))
    print("AI response:", response.text.strip())
    return test_cases


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
                "\n".join(c.get("前置条件", [])),
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
