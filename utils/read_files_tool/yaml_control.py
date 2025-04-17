import os
import ast
import yaml
from utils.read_files_tool.regular_control import regular


class GetYamlData:
    """获取yaml文件数据"""

    def __init__(self, file_path):
        self.file_path = str(file_path)

    # 获取yaml文件数据
    def get_yaml_data(self) -> dict:
        """获取yaml文件数据
        :return: dict
        """
        # 判断文件是否存在
        if os.path.exists(self.file_path):
            # 读取yaml文件
            data = open(self.file_path, "r", encoding="utf-8").read()
            # 解析yaml文件
            try:
                yaml_data = yaml.load(data, Loader=yaml.FullLoader)
            except yaml.YAMLError as e:
                raise e
        else:
            raise FileNotFoundError(f"文件{self.file_path}不存在！")
        return yaml_data

    # 写入yaml文件数据
    def write_yaml_data(self, key: str, value) -> int:
        """写入yaml文件数据
        :param key: str
        :param value: str
        :return: int
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = []
            for line in f.readlines():
                if line != "\n":
                    lines.append(line)
        with open(self.file_path, "w", encoding="utf-8") as f:
            flag = 0
            for line in lines:
                left_str = line.split(":")[0]
                if key == left_str and "#" not in line:
                    newline = f"{left_str}: {value}"
                    line = newline
                    f.write(f"{line}\n")
                    flag = 1
                else:
                    f.write(f"{line}")
        return flag


class GetCaseData(GetYamlData):
    """获取用例数据"""

    def get_different_formats_yaml_data(self) -> list:
        """
        获取兼容不同格式的yaml数据
        :return:
        """
        res_list = []
        for i in self.get_yaml_data():
            res_list.append(i)
        return res_list

    def get_yaml_case_data(self):
        """
        获取测试用例数据, 转换成指定数据格式
        :return:
        """

        _yaml_data = self.get_yaml_data()
        # 正则处理yaml文件中的数据
        re_data = regular(str(_yaml_data))
        return ast.literal_eval(re_data)

    