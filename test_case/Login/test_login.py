import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

case_id = ["login_01"]
TestData = GetTestCase.case_data(case_id)
INFO.logger.info(f"TestData: {TestData}")
re_data = regular(str(TestData))
INFO.logger.info(f"re_data: {re_data}")


@allure.epic("登录接口")
class TestLogin:
    @allure.feature("登录接口")
    @allure.story("登录接口-登录成功")
    @pytest.mark.parametrize(
        "in_data", eval(re_data), ids=[i["detail"] for i in TestData]
    )
    def test_login(
        self,
        in_data,
        case_skip,
    ):
        INFO.logger.info(f"data: {in_data}")
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )
