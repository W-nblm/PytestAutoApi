from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename
import yaml

# 加载完整的 OpenAPI 规范
spec_dict, spec_url = read_from_filename("auth-ali.yaml")

# 验证规范
try:
    validate_spec(spec_dict)
    print("OpenAPI 规范验证通过！")
except Exception as e:
    print(f"验证失败: {e}")

# 安装
# pip install prance

from prance import ResolvingParser
import yaml

parser = ResolvingParser("auth-ali.yaml")
dereferenced_spec = parser.specification
paths =dereferenced_spec.get("paths",{})
print(paths.keys())
print(paths.values())

# 保存为文件，保持中文可读性
with open("bundled-openapi.yaml", "w", encoding="utf-8") as f:
    yaml.dump(
        dereferenced_spec,
        f,
        default_flow_style=False,
        allow_unicode=True,  # 关键参数：允许直接输出Unicode字符
        encoding="utf-8",  # 确保编码正确
        sort_keys=False,  # 保持原有键的顺序
    )
