# import requests
# import time


# def get_public_ip(retries=50, delay=5):
#     for attempt in range(1, retries + 1):
#         try:
#             ip = requests.get("https://ipinfo.io/ip", timeout=5).text.strip()
#             print(f"[{attempt}] Got public IP: {ip}")
#             return ip
#         except requests.RequestException as e:
#             print(f"[{attempt}] Failed to get public IP: {e}")
#             if attempt < retries:
#                 time.sleep(delay)
#     print("Exceeded maximum retry attempts to fetch public IP.")
#     return None


# def get_record_id(dns_name, zone_id, token):
#     resp = requests.get(
#         "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records",
#         headers={
#             "Authorization": "Bearer " + token,
#             "Content-Type": "application/json",
#         },
#     )
#     print(resp.json())
#     if not resp.json()["success"]:
#         return None

#     domains = resp.json()["result"]
#     for domain in domains:
#         if dns_name == domain["name"]:
#             return domain["id"]
#     return None


# def update_record(dns_name, zone_id, token, dns_id, ip, proxied=False):
#     resp = requests.put(
#         "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(
#             zone_id, dns_id
#         ),
#         json={"type": "A", "name": dns_name, "content": ip, "proxied": proxied},
#         headers={
#             "Authorization": "Bearer " + token,
#             "Content-Type": "application/json",
#         },
#     )
#     if not resp.json()["success"]:
#         return False
#     return True


# if __name__ == "__main__":
#     token = "QURYiz77jmDV8NoMcBqBQCVCFFDNk18LMPsM__Xd"
#     zone_id = "2d2bcfe7a92e97da138f5d83b350b8f6"
#     dns_name = "66532523.xyz"
#     dns_id = get_record_id(dns_name, zone_id, token)

#     ip = get_public_ip()
#     print(ip)
#     # if not ip:
#     #     exit(1)
#     # sdfsd
#     # update_record(dns_name, zone_id, token, dns_id, ip)
# import base64

# auth_key = "1+kerOsP0wPDscT3CFVs1+GirhJxuK5SfqxxB08HdtxWcZ6zYRfTXeO5pTqhOPFL"
# try:
#     decoded = base64.b64decode(auth_key)
#     print(decoded)
# except Exception as e:
#     print(f"解码失败：{e}")

# from Crypto.Cipher import DES
# import base64

# authKey = "1+kerOsP0wPDscT3CFVs1+GirhJxuK5SfqxxB08HdtxWcZ6zYRfTXeO5pTqhOPFL"
# ciphertext = base64.b64decode(authKey)

# key = b"Property"  # 必须是 8 字节 DES 密钥
# cipher = DES.new(key, DES.MODE_ECB)
# plaintext = cipher.decrypt(ciphertext)
# print(plaintext)
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

        self.input_file = Path(ensure_path_sep(input_file))
        self.output_dir = Path(ensure_path_sep(output_dir))
        self.output_dir.mkdir(exist_ok=True)
        with open(self.input_file, "r", encoding="utf-8") as f:
            self.openapi_data = yaml.safe_load(f)

        self.method_map = {
            "get": "GET",
            "post": "POST",
            "put": "PUT",
            "delete": "DELETE",
        }

    def get_allure_epic(self):
        """获取 allure epic 名称"""
        _allure_epic = self.openapi_data["info"]["title"]
        return _allure_epic

    def get_allure_feature(self):
        """获取 allure feature 名称"""
        _allure_feature = self.openapi_data["tags"]
        return _allure_feature

    # def get_allure_story(self):
    #     """获取 allure story 名称"""
    #     _allure_story = self.openapi_data["summary"]
    #     return _allure_story

    def format_case_id(self, path: str) -> str:
        parts = [p for p in path.split("/") if p and not p.startswith("{")]
        parts.append("01")
        return "_".join(parts)

    def format_request_data(self, case, type, data: dict) -> dict:
        """格式化请求参数"""
        schemas = self.openapi_data.get("components", {}).get("schemas", {})
        for name, schema in schemas.items():
            pass

    def generate_case(
        self, path: str, method: str, content: dict, schema_data: dict
    ) -> tuple:
        method = method.lower()
        case_id = self.format_case_id(path)
        method_data = content[method]

        case = {
            "common": {
                "allureEpic": self.get_allure_epic(),
                "allureFeature": self.get_allure_feature(),
                "allureStory": method_data.get("summary", ""),
            },
            case_id: {
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
            },
        }
        # 判断请求参数类型
        if "parameters" in method_data:
            for param in method_data["parameters"]:
                pname = param["name"]
                case[case_id]["data"][pname] = f"$cache{{{pname}}}"

        if "requestBody" in method_data:
            content_type = list(method_data["requestBody"]["content"].keys())[0]
            case[case_id]["requestType"] = "json" if "json" in content_type else "data"
            refs = method_data["requestBody"]["content"][content_type]["schema"][
                "$ref"
            ].split("/")
            ref_name = refs[-1]
            if ref_name in schema_data:
                schema = schema_data[ref_name]
                for prop_name, prop_schema in schema.get("properties", {}).items():
                    if "type" in prop_schema:
                        if prop_schema["type"] == "string":
                            case[case_id]["data"][prop_name] = f"${{{prop_name}}}"
                        elif prop_schema["type"] == "integer":
                            case[case_id]["data"][prop_name] = f"${{{prop_name}}}"
                        elif prop_schema["type"] == "number":
                            case[case_id]["data"][prop_name] = f"${{{prop_name}}}"
                        elif prop_schema["type"] == "boolean":
                            case[case_id]["data"][prop_name] = f"${{{prop_name}}}"
                    if prop_name == "data":
                        case[case_id]["data"][prop_name] = {}
                        temp_ref_name = prop_schema["$ref"].split("/")[-1]
                        if temp_ref_name in schema_data:
                            temp_schema = schema_data[temp_ref_name]
                            for temp_prop_name, temp_prop_schema in temp_schema.get(
                                "properties", {}
                            ).items():
                                if "type" in temp_prop_schema:
                                    if temp_prop_schema["type"] == "string":
                                        case[case_id]["data"]["data"][
                                            temp_prop_name
                                        ] = f"${{{temp_prop_name}}}"
                                    elif temp_prop_schema["type"] == "integer":
                                        case[case_id]["data"]["data"][
                                            temp_prop_name
                                        ] = f"${{{temp_prop_name}}}"
                                    elif temp_prop_schema["type"] == "number":
                                        case[case_id]["data"]["data"][
                                            temp_prop_name
                                        ] = f"${{{temp_prop_name}}}"
                                    elif temp_prop_schema["type"] == "boolean":
                                        case[case_id]["data"]["data"][
                                            temp_prop_name
                                        ] = f"${{{temp_prop_name}}}"

        # 获取请求的参数
        return case

    def generate_all_cases(self):
        generated_files = []
        # 生成测试用例文件
        schema_data = self.openapi_data.get("components", {}).get("schemas", {})

        for path, methods in self.openapi_data.get("paths", {}).items():
            file_name = "_".join(path.split("/")[1::])
            for method in methods:
                case = self.generate_case(path, method, methods, schema_data)
                file_path = self.output_dir / f"{file_name}.yaml"
                with open(file_path, "w", encoding="utf-8") as f:
                    yaml.dump(
                        case,
                        f,
                        allow_unicode=True,
                        sort_keys=False,
                        default_flow_style=False,
                    )
                generated_files.append(str(file_path))
        return generated_files


if __name__ == "__main__":
    # sw = SwaggerExporter()
    # sw.export_swagger()
    generator = OpenAPITestcaseGenerator(
        input_file="/Files/Swagger/mqtt-ali.yaml", output_dir="/Files/Testcase/"
    )
    generated_files = generator.generate_all_cases()
    print(f"✅ 共生成 {len(generated_files)} 个测试用例文件：{generated_files}")
