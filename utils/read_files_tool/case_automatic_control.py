from collections import defaultdict
import datetime
import os
import shutil
from typing import Text, Dict

import yaml
from common.setting import ensure_path_sep
from utils.logging_tool.log_control import INFO
from utils.read_files_tool.testcase_template import write_testcase_file
from utils.read_files_tool.yaml_control import GetYamlData
from utils.read_files_tool.get_all_files_path import get_all_files
from utils.other_tools.exceptions import ValueNotFoundError


class TestCaseAutomaticGeneration:

    @staticmethod
    def case_data_path() -> Text:
        """ "返回yaml 用例文件路径"""
        return ensure_path_sep("\\data")

    @staticmethod
    def case_path() -> Text:
        """存放用例代码路径"""
        return ensure_path_sep("\\test_case")

    def file_name(self, file: Text) -> Text:
        """通过yaml文件的命名,将名称转换成py文件名称"""
        i = len(self.case_data_path())
        yaml_path = file[i:]
        file_name = None
        if ".yaml" in yaml_path:
            file_name = yaml_path.replace(".yaml", ".py")
        elif ".yml" in yaml_path:
            file_name = yaml_path.replace(".yml", ".py")
        return file_name

    def get_case_path(self, file_path: Text) -> tuple:
        """根据yaml用例生成testcase文件路径"""
        path = self.file_name(file_path).split(os.sep)
        case_name = path[-1].replace(path[-1], "test_" + path[-1])
        path[-1] = case_name
        test_path = os.sep.join(path)
        return ensure_path_sep("\\test_case" + test_path), case_name

    def get_test_class_title(self, file_path: Text) -> Text:
        """生成测试类名"""
        _file_name = os.path.split(self.file_name(file_path))[1][:-3]
        _name = _file_name.split("_")
        _name_len = len(_name)
        # 将文件名称格式，转换成类名称: sup_apply_list --> SupApplyList
        for i in range(_name_len):
            _name[i] = _name[i].capitalize()
        return "".join(_name)

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
        _file_name = os.path.split(self.file_name(file_path))[1][:-3]
        return _file_name

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
            INFO.logger.info(f"创建用例文件夹: {dir_path}")

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

    def yaml_path(self, file_path: Text) -> Text:
        """
        生成动态 yaml 路径, 主要处理业务分层场景
        :param file_path: 如业务有多个层级, 则获取到每一层/test_demo/DateDemo.py
        :return: Login/common.yaml
        """
        i = len(self.case_date_path())
        # 兼容 linux 和 window 操作路径
        yaml_path = file_path[i:].replace("\\", "/")
        return yaml_path

    # def get_case_automatic(self) -> None:
    #     """自动生成 测试代码"""
    #     file_path = get_all_files(
    #         file_path=ensure_path_sep("\\data"), yaml_data_switch=True
    #     )
    #     for file in file_path:
    #         # 判断代理拦截的yaml文件，不生成test_case代码
    #         if "proxy_data.yaml" not in file:
    #             # 判断用例需要用的文件夹路径是否存在，不存在则创建
    #             self.mk_dir(file)
    #             yaml_case_process = GetYamlData(file).get_yaml_data()
    #             self.case_ids(yaml_case_process)
    #             write_testcase_file(
    #                 allure_epic=self.allure_epic(
    #                     case_data=yaml_case_process, file_path=file
    #                 ),
    #                 allure_feature=self.allure_feature(
    #                     yaml_case_process, file_path=file
    #                 ),
    #                 class_title=self.get_test_class_title(file),
    #                 func_title=self.func_title(file),
    #                 case_path=self.get_case_path(file)[0],
    #                 case_ids=self.case_ids(yaml_case_process),
    #                 file_name=self.get_case_path(file)[1],
    #                 allure_story=self.allure_story(
    #                     case_data=yaml_case_process, file_path=file
    #                 ),
    #             )

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
        case_order_data = {"strict": True, "modules": []}

        for dir_path, yaml_files in dir_groups.items():
            # 创建测试用例输出目录
            self.mk_dir(
                self.replace_data_dir(dir_path, old=yaml_files_dir, new=cases_dir)
            )
            dir_name = os.path.basename(dir_path)
            print("目录名称:", dir_path)
            print("用例文件:", yaml_files)
            # 生成模块名称
            module_name = os.path.relpath(
                self.replace_data_dir(dir_path, old=yaml_files_dir, new=cases_dir),
                ensure_path_sep("\\test_case"),
            ).replace(os.sep, "/")
            print("模块名称:", module_name)
            # 生成测试用例类名
            class_title = "Test_" + dir_path.split(os.sep)[-1].capitalize()
            # 合成测试用例文件路径
            case_path = os.path.join(dir_path, "test_" + dir_name.lower() + ".py")
            # 转换为 test_case 目录下的路径
            case_path = self.replace_data_dir(
                case_path, old=yaml_files_dir, new=cases_dir
            )
            print("用例文件路径:", case_path)
            print("*" * 60)
            # 存放所有方法
            methods_code = ""
            case_list = []

            for yf in yaml_files:
                # 读取yaml文件内容
                yaml_case_process = GetYamlData(yf).get_yaml_data()
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
            # print(methods_code)
            # 写入case_order.yaml模块配置
            case_order_data["modules"].append(
                {"name": module_name, "enabled": True, "cases": case_list}
            )
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
    pytest.main(['{case_path}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
"""
            # 判断是否实时更新
            conf_data = GetYamlData(
                ensure_path_sep("\\common\\config.yaml")
            ).get_yaml_data()
            real_time_update_test_cases = conf_data.get("real_time_update_test_cases")
            if real_time_update_test_cases:
                self.write_case(case_path=case_path, page=page)
            elif real_time_update_test_cases is False:
                if not os.path.exists(case_path):
                    self.write_case(case_path=case_path, page=page)
            else:
                raise ValueNotFoundError(
                    "real_time_update_test_cases must be True or False"
                )
        # 最后一次性生成 case_order.yaml
        order_file_path = ensure_path_sep("\\common\\case_order.yaml")

        if os.path.exists(order_file_path):
            order_file_path = ensure_path_sep("\\common\\case_order_back.yaml")
            with open(order_file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(case_order_data, f, allow_unicode=True, sort_keys=False)
            INFO.logger.info(f"case_order.yaml 已生成到: {order_file_path}")
        else:
            with open(order_file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(case_order_data, f, allow_unicode=True, sort_keys=False)
            INFO.logger.info(f"case_order.yaml 已生成到: {order_file_path}")
