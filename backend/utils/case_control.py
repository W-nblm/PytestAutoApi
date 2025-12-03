from collections import defaultdict
import datetime
import os
from typing import Text, Dict
import yaml
from common.setting import ensure_path_sep
import logging
from backend.utils.file_control import get_all_files
from backend.utils.custom_exceptions import ValueNotFoundError


class TestCaseAutomaticGeneration:

    @staticmethod
    def error_message(param_name, file_path):
        """
        用例中填写不正确的相关提示
        :return:
        """
        msg = (
            f"用例中未找到 {param_name} 参数值，请检查新增的用例中是否填写对应的参数内容"
            "如已填写，可能是 yaml 参数缩进不正确\n"
            f"用例路径: {file_path}"
        )
        return msg

    def func_title(self, file_path: Text) -> Text:
        # 获取文件名
        file_name = os.path.basename(file_path)

        # 去掉后缀名
        file_name = os.path.splitext(file_name)[0]

        if "-" in file_name:
            file_name = file_name.replace("-", "_")

        return file_name

    @staticmethod
    def allure_epic(case_data: Dict, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容 @allure.epic("项目名称")
        :param file_path: 用例路径
        :param case_data: 用例数据
        :return:
        """
        try:
            return case_data["case_common"]["allureEpic"]
        except KeyError as exc:
            raise ValueNotFoundError(
                TestCaseAutomaticGeneration.error_message(
                    param_name="allureEpic", file_path=file_path
                )
            ) from exc

    @staticmethod
    def allure_feature(case_data: Dict, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容 @allure.feature("模块名称")
        :param file_path:
        :param case_data:
        :return:
        """
        try:
            return case_data["case_common"]["allureFeature"]
        except KeyError as exc:
            raise ValueNotFoundError(
                TestCaseAutomaticGeneration.error_message(
                    param_name="allureFeature", file_path=file_path
                )
            ) from exc

    @staticmethod
    def allure_story(case_data: Dict, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容  @allure.story("测试功能")
        :param file_path:
        :param case_data:
        :return:
        """
        try:
            return case_data["case_common"]["allureStory"].replace("\n", "")
        except KeyError as exc:
            raise ValueNotFoundError(
                TestCaseAutomaticGeneration.error_message(
                    param_name="allureStory", file_path=file_path
                )
            ) from exc

    def mk_dir(self, dir_path: Text) -> None:
        """判断生成自动化代码的文件夹路径是否存在，如果不存在，则自动创建"""
        print(f"用例文件夹路径: {os.path.exists(dir_path)}")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logging.info(f"创建用例文件夹: {dir_path}")

    # 获取yaml文件数据
    def get_yaml_data(self, file_path: Text) -> dict:
        """获取yaml文件数据
        :return: dict
        """
        # 判断文件是否存在
        if os.path.exists(file_path):
            # 读取yaml文件
            data = open(file_path, "r", encoding="utf-8").read()
            # 解析yaml文件
            try:
                yaml_data = yaml.load(data, Loader=yaml.FullLoader)
            except yaml.YAMLError as e:
                raise e
        else:
            raise FileNotFoundError(f"文件{file_path}不存在！")
        return yaml_data

    @staticmethod
    def case_ids(test_case):
        """
        获取用例 ID
        :param test_case: 测试用例内容
        :return:
        """
        ids = []
        for k, v in test_case.items():
            if k != "case_common":
                ids.append(k)
        return ids

    def write_case(self, case_path, page):
        """写入测试用例"""
        with open(case_path, "w", encoding="utf-8") as file:
            file.write(page)
        print(f"生成用例文件: {case_path}")

    def replace_data_dir(self, path: str, old="data", new="test_case") -> str:
        parts = os.path.normpath(path).split(os.sep)
        parts = [new if part.lower() == old.lower() else part for part in parts]
        return os.sep.join(parts)

    def get_case_automatic(self, yaml_files_dir="data", cases_dir="test_case") -> None:
        """
        自动生成 测试代码
        :param yaml_files_dir: yaml用例文件目录
        :param cases_dir: 生成测试用例文件目录
        :return:
        """
        print(os.path.abspath(__file__))
        print("yaml用例文件目录:", yaml_files_dir)
        # 读取所有的yaml文件
        file_paths = get_all_files(
            file_path=ensure_path_sep(yaml_files_dir), yaml_data_switch=True
        )
        # 按目录进行分类
        dir_groups = defaultdict(list)
        for file in file_paths:
            if "proxy_data.yaml" not in file:
                # 判断用例需要用的文件夹路径是否存在，不存在则创建
                dir_groups[os.path.dirname(file)].append(file)

        for dir_path, yaml_files in dir_groups.items():
            # 创建测试用例输出目录
            dir_path = dir_path.replace("-", "_")
            dir_path = dir_path.replace(yaml_files_dir, cases_dir)
            self.mk_dir(dir_path=dir_path)

            dir_name = os.path.basename(dir_path)

            print("目录名称:", dir_path)
            print("用例文件:", yaml_files)

            # 生成测试用例类名
            class_title = "Test_" + dir_path.split(os.sep)[-1].capitalize()
            # 合成测试用例文件路径

            case_path = os.path.join(dir_path, "test_" + dir_name.lower() + ".py")
            case_path = case_path.replace(yaml_files_dir, cases_dir)

            print("*" * 60)
            # 存放所有方法
            methods_code = ""
            case_list = []

            for yf in yaml_files:
                # 读取yaml文件内容
                yaml_case_process = self.get_yaml_data(yf)
                # 生成测试用例方法名
                case_ids = self.case_ids(yaml_case_process)
                func_title = self.func_title(yf)  # 用例标题
                allure_feature = self.allure_feature(yaml_case_process, yf)  # 用例模块
                allure_story = self.allure_story(yaml_case_process, yf)  # 用例描述
                re_data = f"regular(str(GetTestCase.case_data({case_ids})))"
                method = f"""
    @allure.feature("{allure_feature}")
    @allure.story("{allure_story}")
    @pytest.mark.parametrize('in_data', eval({re_data}), ids=[i['detail'] for i in GetTestCase.case_data({case_ids})])
    def test_{func_title}(self, in_data, case_skip):
        allure.dynamic.title(f"{func_title}"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )
"""
                methods_code += method
                case_list.append(f"test_{func_title}")

            # 组装整个pytest文件
            page = f"""
# -*- coding: utf-8 -*-
# @Time    : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("{dir_name}")
class {class_title}:
{methods_code}

if __name__ == '__main__':
    pytest.main([r'{case_path}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
"""

            self.write_case(case_path=case_path, page=page)
