
# -*- coding: utf-8 -*-
# @Time    : 2025-11-19 11:29:14

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("auth_ali")
class Test_Auth_ali:

    @allure.feature("认证授权模块")
    @allure.story("邮件登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_emailLogin_01_success'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_emailLogin_01_success'])])
    def test_case_auth_emailLogin(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_emailLogin"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main([r'D:\PytestAutoApi\test_case\interface_case\auth_ali\test_auth_ali.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
