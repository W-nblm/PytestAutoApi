import os
from common.setting import ensure_path_sep
from utils.read_files_tool.case_automatic_control import TestCaseAutomaticGeneration
from utils.read_files_tool.swagger_for_yaml import (
    SwaggerExporter,
    OpenAPITestcaseGenerator,
)


def generate_test_cases():
    # 导出swagger中的接口数据
    sw = SwaggerExporter()
    sw.export_swagger()

    #  通过导出的swagger数据生成测试用例
    for root, dirs, files in os.walk(ensure_path_sep("/Files/Swagger/")):
        for file in files:
            if file.endswith(".yaml"):
                output_dir = os.path.join(
                    ensure_path_sep("/Files/Testcase/"), file.replace(".yaml", "")
                )
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                generator = OpenAPITestcaseGenerator(
                    input_file=os.path.join(root, file),
                    output_dir=output_dir,
                )
                generated_files = generator.generate_all_cases()


if __name__ == "__main__":
    # 导出swagger并生成测试用例
    # generate_test_cases()

    # 根据用例文件生成测试用例文件
    TestCaseAutomaticGeneration().get_case_automatic(yaml_files_dir="app/interface_data",cases_dir="app/interface_case")
