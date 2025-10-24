
# -*- coding: utf-8 -*-
# @Time    : 2025-09-29 10:00:41

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("Register")
class Test_Register:

    @allure.feature("账号相关信息代理接口")
    @allure.story("账号注册发送邮箱验证码 不需要加密 test")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['app_info_agent_registerMailCodeTest_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['app_info_agent_registerMailCodeTest_01'])])
    def test_app_info_agent_registerMailCodeTest(self, in_data, case_skip):
        allure.dynamic.title(f"app_info_agent_registerMailCodeTest"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("app用户控制器")
    @allure.story("TEST 注册 单独校验验证码 不需要加密")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['app_info_appUser_registerCheckCodeTest_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['app_info_appUser_registerCheckCodeTest_01'])])
    def test_app_info_appUser_registerCheckCodeTest(self, in_data, case_skip):
        allure.dynamic.title(f"app_info_appUser_registerCheckCodeTest"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        from utils.email_tool.temp_email import TempEmailManager
        from utils.cache_process.cache_control import CacheHandler

        te = TempEmailManager()
        email = CacheHandler.get_cache("random_email")
        code = te.get_random_email_code(email)

        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main(['d:\PytestAutoApi\test_case\Wobirdy\Register\test_register.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
