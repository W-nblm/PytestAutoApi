
# -*- coding: utf-8 -*-
# @Time    : 2025-08-23 17:04:52

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("Login")
class Test_Login:

    @allure.feature("登录模块")
    @allure.story("登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_login_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_login_01'])])
    def test_login(self, in_data, case_skip):
        allure.dynamic.title(f"login"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("banner")
    @allure.story("banner")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_upload_img_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_upload_img_01'])])
    def test_upload_img(self, in_data, case_skip):
        allure.dynamic.title(f"upload_img"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main(['d:\PytestAutoApi\test_case\Wobirdy\Login\test_login.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
