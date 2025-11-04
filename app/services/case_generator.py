import re
from time import sleep
import yaml
from faker import Faker
from pathlib import Path
from google import genai
from app.services.case_schema import CASE_SCHEMA_EXAMPLE

client = genai.Client(api_key="AIzaSyCmAo52ridCff1Ix6AvdHpzDenC5mW2nys")

faker = Faker("zh_CN")


def fill_test_data(api_info):
    """根据接口名生成测试数据"""
    return {
        "username": faker.user_name(),
        "password": faker.password(),
        "email": faker.email(),
    }


def generate_basic_cases(
    api_defs: list,
    output_dir: str = "interface_data",
    project_name: str = "platform-Cloud-Plus微服务权限管理系统",
):
    """
    使用 AI 根据 OpenAPI 接口定义生成符合 pytest 自动化执行的 YAML 测试用例
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_paths = []
    for api in api_defs:
        all_cases = {}
        path = api.get("path")
        method = api.get("method", "GET").upper()
        summary = api.get("summary", "未命名接口")
        tags = api.get("tags", ["未分类"])
        tag = tags[0] if isinstance(tags, list) else tags

        # ---- prompt 构造 ----
        prompt = f"""
        你是一个接口自动化测试专家。
        请基于以下接口信息，生成一个可执行的 YAML 测试用例,用例需要覆盖基本的正向场景和异常场景。
        YAML 必须符合如下格式：
        ---
        case_common:
          allureEpic: 标题：{project_name}_接口文档
          allureFeature: {tag}
          allureStory: {summary}

        case_{path.strip('/').replace('/', '_')}_01:
          host: ${{{{host()}}}}
          url: {path}
          method: {method}
          detail: {tag} - {summary}
          headers:
            Authorization: $cache{{app_token}}
            Content-Language: zh_CN
            App-Source: WObird
          requestType: json
          data:
            # 请根据接口参数类型填写示例字段
          dependence_case: []
          # 断言部分:name: 断言名称;jsonpath: 响应内容的 JSONPath 表达式;type: 断言类型(==、lt、le、gt、ge、not_eq、str_eq、contains 等）;value: 预期值;message: 断言失败时的提示信息
          assert:
            - name: 校验接口状态码
              jsonpath: $.code
              type: eq
              value: 200
              message: 状态码不为200
            - name: 校验响应消息
              jsonpath: $.msg
              type: contains
              value: 成功
        ---
        以下是接口描述：
        {api}
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            raw = response.text.strip()
            print(f"✅ LLM Raw Output:\n{raw}\n{'='*60}")
            # 去掉 Markdown 代码块标识
            raw = re.sub(
                r"^```[a-zA-Z]*|```$", "", raw.strip(), flags=re.MULTILINE
            ).strip()

            # 有时模型会生成多个 case，用 safe_load_all 兼容
            yaml_docs = list(yaml.safe_load_all(raw))
            for doc in yaml_docs:
                if isinstance(doc, dict):
                    all_cases.update(doc)

        except Exception as e:
            print(f"⚠️ 生成失败: {e}")
            continue

        # ---- 输出 YAML 文件 ----
        output_path = (
            Path(output_dir) / f"case_{path.strip('/').replace('/', '_')}.yaml"
        )
        output_paths.append(str(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(all_cases, f, allow_unicode=True, sort_keys=False)
    print(f"✅ 已生成可执行测试用例文件: {output_paths}")
    return output_paths
