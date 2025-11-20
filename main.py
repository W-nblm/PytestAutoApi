import os

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
