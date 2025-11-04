import yaml
from openapi_spec_validator import validate_spec

def parse_openapi_spec(file_content: bytes):
    """解析上传的 OpenAPI 文件"""
    spec = yaml.safe_load(file_content)
    validate_spec(spec)
    paths = spec.get("paths", {})
    api_list = []
    for path, methods in paths.items():
        for method, info in methods.items():
            api_list.append({
                "path": path,
                "method": method.upper(),
                "summary": info.get("summary", ""),
                "parameters": info.get("parameters", []),
                "responses": info.get("responses", {}),
            })
    return api_list
