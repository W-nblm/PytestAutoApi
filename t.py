# from swagger_parser import SwaggerParser

# parser = SwaggerParser(swagger_path="http://192.168.100.105:10009/app-ali/v3/api-docs")
# print(parser.paths.keys())  # 输出所有接口路径
from prance import ResolvingParser

# 加载本地文件或远程 URL
parser = ResolvingParser("./Files/Swagger/app-ali.yaml")


# 得到完整的结构（已解析 $ref 引用）
spec = parser.specification

# 打印接口路径
for path, methods in spec["paths"].items():
    for method, details in methods.items():
        print(f"[{method.upper()}] {path} - {details.get('summary')}")
    print(methods.items())
