import os
import sys
import traceback
import pytest
from utils.other_tools.models import NotificationType
from utils.other_tools.allure_data.allure_report_data import AllureFileClean
from utils.logging_tool.log_control import INFO

# from utils.notify.wechat_send import WeChatSend
# from utils.notify.ding_talk import DingTalkSendMsg
# from utils.notify.send_mail import SendEmail
# from utils.notify.lark import FeiShuTalkChatBot
# from utils.other_tools.allure_data.error_case_excel import ErrorCaseExcel
from utils import config
from utils.other_tools.models import load_module_functions
from utils.assertion import assert_type
from utils.read_files_tool.regular_control import regular


def run():
    try:
        pytest.main(
            [
                "-v",
                "-s",
                "-W",
                "ignore:Module already imported:pytest.PytestWarning",
                "--alluredir",
                "./report/tmp",
                "--clean-alluredir",
                # "--collect-only",
            ]
        )
        os.system(r"allure generate ./report/tmp -o ./report/html --clean")
        allure_data = AllureFileClean().get_case_count()
        INFO.logger.info(f"Allure report generated, total cases: {allure_data}")

    except Exception as e:
        # 如有异常，相关异常发送邮件
        INFO.logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    run()

# import re

# from faker import Faker


# class Context:
#     def __init__(self):
#         self.faker = Faker(locale="zh_CN")

#     def generate_vcode(self, img):
#         print("---------")

#         print(img)
#         print("---------")
#         return "1234"


# def regular(target: str):
#     """
#     新版本
#     使用正则替换请求数据
#     :return:
#     """

#     regular_pattern = r"\${{(.*?)}}"
#     while re.findall(regular_pattern, target):
#         key = re.search(regular_pattern, target).group(1)
#         value_types = ["int:", "bool:", "list:", "dict:", "tuple:", "float:"]
#         if any(i in key for i in value_types) is True:
#             func_name = key.split(":")[1].split("(")[0]
#             value_name = key.split(":")[1].split("(")[1][:-1]
#             if value_name == "":
#                 value_data = getattr(Context(), func_name)()
#             else:
#                 value_data = getattr(Context(), func_name)(*value_name.split(","))
#             regular_int_pattern = r"\'\${{(.*?)}}\'"
#             target = re.sub(regular_int_pattern, str(value_data), target, 1)
#         else:
#             func_name = key.split("(")[0]
#             value_name = key.split("(")[1][:-1]
#             if value_name == "":
#                 value_data = getattr(Context(), func_name)()
#             else:
#                 value_data = getattr(Context(), func_name)(*value_name.split(","))
#             target = re.sub(regular_pattern, str(value_data), target, 1)
#     return target


# img = "${{generate_vcode($cache{code_01_code})}} aaa"
# a = regular(img)
# print(a)
