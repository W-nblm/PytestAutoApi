import os
import requests
import yaml
import jsonpath

from common.setting import ensure_path_sep


class SwaggerExporter:
    resources_url = "http://192.168.100.105:10009/swagger-resources"
    docs_url = "http://192.168.100.105:10009/v3/api-docs"
    headers = {
        "knfie4j-gateway-request": "",
        "knife4j-gateway-code": "ROOT",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self):
        pass

    def get_api_headers(self, url, headers):
        # 导出 swagger json
        res = requests.get(url=url, headers=headers)
        print(res.json())
        swagger_header = jsonpath.jsonpath(res.json(), "$[*].header")
        swagger_name = jsonpath.jsonpath(res.json(), "$[*].name")
        swagger_json = dict(zip(swagger_name, swagger_header))
        return swagger_json

    def export_swagger_yaml(self, name, headers, output_file):
        try:
            response = requests.get(
                url=self.docs_url,
                headers=headers,
                cookies={
                    "_ga": "GA1.1.1445763860.1704869668",
                    "_ga_73YJPXJTLX": "GS1.1.1736152477.7.0.1736152478.0.0.0",
                },
            )
            response.raise_for_status()
            swagger_json = response.json()

            with open(output_file, "w", encoding="utf-8") as f:
                yaml.dump(
                    swagger_json,
                    f,
                    allow_unicode=True,
                    sort_keys=False,
                    default_flow_style=False,
                )

            print(f"✅ [{name}] 成功导出为 YAML 文件：{output_file}")
        except Exception as e:
            print(f"❌ [{name}] 导出失败：{e}")

    def export_swagger(self):
        api_headers = self.get_api_headers(self.resources_url, self.headers)
        file_path = ensure_path_sep("/Files/Swagger/")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for name, header in api_headers.items():
            self.headers["knfie4j-gateway-request"] = header
            self.export_swagger_yaml(name, self.headers, f"{file_path}{name}.yaml")
        return "✅ 导出成功"


import yaml
from pathlib import Path


class OpenAPITestcaseGenerator:
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        with open(self.input_file, "r", encoding="utf-8") as f:
            self.openapi_data = yaml.safe_load(f)

        self.case_common = {
            "case_common": {
                "allureEpic": "IoT",
                "allureFeature": "虚拟设备测试",
                "allureStory": "接口自动生成",
            }
        }

        self.method_map = {
            "get": "GET",
            "post": "POST",
            "put": "PUT",
            "delete": "DELETE",
        }

    def format_case_id(self, path: str, method: str) -> str:
        parts = [p for p in path.split("/") if p and not p.startswith("{")]
        return "_".join(parts + [method.lower()])

    def generate_case(self, path: str, method: str, content: dict) -> tuple:
        method = method.lower()
        case_id = self.format_case_id(path, method)
        method_data = content[method]

        case = {
            "host": "${{host()}}",
            "url": path,
            "method": self.method_map[method],
            "detail": f"{method_data.get('tags', ['未知模块'])[0]} - {method_data.get('summary', '')}",
            "headers": {
                "Authorization": "$cache{app_token}",
                "Content-Language": "zh_CN",
            },
            "requestType": "params",
            "is_run": "",
            "data": {},
            "dependence_case": "",
            "dependence_case_data": "",
            "assert": {
                "code": {
                    "jsonpath": "$.code",
                    "type": "==",
                    "value": 200,
                    "AssertType": "",
                    "message": "接口状态码不为200",
                },
                "msg": {
                    "jsonpath": "$.msg",
                    "type": "contains",
                    "value": "成功",
                    "AssertType": "",
                },
            },
            "sql": "",
            "setup_sql": "",
        }

        if "parameters" in method_data:
            for param in method_data["parameters"]:
                pname = param["name"]
                case["data"][pname] = f"$cache{{{pname}}}"

        if "requestBody" in method_data:
            content_type = list(method_data["requestBody"]["content"].keys())[0]
            case["requestType"] = "json" if "json" in content_type else "data"

        return case_id, case

    def generate_all_cases(self):
        generated_files = []
        for path, methods in self.openapi_data.get("paths", {}).items():
            for method in methods:
                case_id, case = self.generate_case(path, method, methods)
                single_case_yaml = dict(self.case_common)
                single_case_yaml[case_id] = case

                file_path = self.output_dir / f"{case_id}.yaml"
                with open(file_path, "w", encoding="utf-8") as f:
                    yaml.dump(
                        single_case_yaml,
                        f,
                        allow_unicode=True,
                        sort_keys=False,
                        default_flow_style=False,
                    )

                generated_files.append(str(file_path))

        return generated_files


if __name__ == "__main__":
    sw = SwaggerExporter()
    sw.export_swagger()
