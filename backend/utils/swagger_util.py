import os
import requests
import yaml
import jsonpath
from prance import ResolvingParser
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
            self.export_swagger_yaml(name, self.headers, f"{file_path}\{name}.yaml")
        return "✅ 导出成功"


# 解析 Swagger 文件示例
class SwaggerParser:

    def __init__(self):
        self.is_swagger_file()
        self.file_list = []

    # 判断是否是 Swagger 文件
    def is_swagger_file(self):
        file_path = ensure_path_sep("/Files/Swagger")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"路径不存在: {file_path}")
        for file_name in os.listdir(file_path):
            if file_name.endswith((".yaml", ".yml")):
                self.file_list.append(os.path.join(file_path, file_name))

    def parse_swagger(self):
        # 加载本地文件或远程 URL
        for file in self.file_list:
            parser = ResolvingParser(file)

            # 得到完整的结构（已解析 $ref 引用）
            spec = parser.specification

            # 打印接口路径
            for path, methods in spec["paths"].items():
                for method, details in methods.items():
                    print(f"[{method.upper()}] {path} - {details.get('summary')}")
                print(methods.items())
