
# -*- coding: utf-8 -*-
# @Time    : 2025-11-03 14:39:16

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("interface_data")
class Test_Interface_data:

    @allure.feature("未分类")
    @allure.story("邮件登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01', 'case_auth_innerLogin_01', 'case_auth_emailLogin_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01', 'case_auth_innerLogin_01', 'case_auth_emailLogin_01'])])
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

    @allure.feature("认证授权接口")
    @allure.story("登录方法-内部接口,无验证码")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01', 'case_auth_innerLogin_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01', 'case_auth_innerLogin_01'])])
    def test_case_auth_innerLogin(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_innerLogin"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("登录方法")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01'])])
    def test_case_auth_login(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_login"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("登出方法")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01', 'case_auth_innerLogin_01', 'case_auth_emailLogin_01', 'case_auth_logout_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01', 'case_auth_login_01', 'case_auth_innerLogin_01', 'case_auth_emailLogin_01', 'case_auth_logout_01'])])
    def test_case_auth_logout(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_logout"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("用户注册")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01', 'case_auth_register_01'])])
    def test_case_auth_register(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_register"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("短信登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_smsLogin_01'])])
    def test_case_auth_smsLogin(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_smsLogin"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("认证模块")
    @allure.story("小程序登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01'])])
    def test_case_auth_xcxLogin(self, in_data, case_skip):
        allure.dynamic.title(f"case_auth_xcxLogin"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main(['d:\PytestAutoApi\interface_case\test_interface_data.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
