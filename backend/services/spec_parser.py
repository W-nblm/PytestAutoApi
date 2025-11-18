import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename

from prance import ResolvingParser


def parse_openapi_spec(file_path: str):
    spec_dict, spec_url = read_from_filename(file_path)

    validate_spec(spec_dict)
    # 验证通过后，使用 Prance 解析并解引用
    parser = ResolvingParser(str(file_path))
    dereferenced_spec = parser.specification
    paths = dereferenced_spec.get("paths", {})

    api_list = []
    for path, methods in paths.items():
        for method, info in methods.items():
            print(info.get("requestBody", {}))
            api_list.append(
                {
                    "path": path,
                    "method": method.upper(),
                    "summary": info.get("summary", ""),
                    "parameters": info.get("requestBody", {}),
                    "responses": info.get("responses", {}),
                }
            )
    return api_list
