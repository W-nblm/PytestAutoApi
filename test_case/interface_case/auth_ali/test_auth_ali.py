
# -*- coding: utf-8 -*-
# @Time    : 2025-12-03 10:03:04

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

    @allure.feature("未分类")
    @allure.story("登录方法-内部接口,无验证码")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_innerLogin_01_success', 'case_auth_innerLogin_02_user_not_exist', 'case_auth_innerLogin_03_wrong_password', 'case_auth_innerLogin_04_empty_username', 'case_auth_innerLogin_05_empty_password', 'case_auth_innerLogin_06_missing_username_field', 'case_auth_innerLogin_07_missing_password_field'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_innerLogin_01_success', 'case_auth_innerLogin_02_user_not_exist', 'case_auth_innerLogin_03_wrong_password', 'case_auth_innerLogin_04_empty_username', 'case_auth_innerLogin_05_empty_password', 'case_auth_innerLogin_06_missing_username_field', 'case_auth_innerLogin_07_missing_password_field'])])
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
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_login_01_success', 'case_auth_login_02_invalid_credentials', 'case_auth_login_03_missing_username', 'case_auth_login_04_missing_password', 'case_auth_login_05_empty_username', 'case_auth_login_06_empty_password', 'case_auth_login_07_empty_body'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_login_01_success', 'case_auth_login_02_invalid_credentials', 'case_auth_login_03_missing_username', 'case_auth_login_04_missing_password', 'case_auth_login_05_empty_username', 'case_auth_login_06_empty_password', 'case_auth_login_07_empty_body'])])
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

    @allure.feature("认证授权")
    @allure.story("登出方法")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_logout_01', 'case_auth_logout_02', 'case_auth_logout_03'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_logout_01', 'case_auth_logout_02', 'case_auth_logout_03'])])
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
    @allure.story("短信登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_smsLogin_01_success', 'case_auth_smsLogin_02_missing_phonenumber', 'case_auth_smsLogin_03_missing_smsCode', 'case_auth_smsLogin_04_invalid_phonenumber_format', 'case_auth_smsLogin_05_incorrect_smsCode', 'case_auth_smsLogin_06_empty_phonenumber', 'case_auth_smsLogin_07_empty_smsCode'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_smsLogin_01_success', 'case_auth_smsLogin_02_missing_phonenumber', 'case_auth_smsLogin_03_missing_smsCode', 'case_auth_smsLogin_04_invalid_phonenumber_format', 'case_auth_smsLogin_05_incorrect_smsCode', 'case_auth_smsLogin_06_empty_phonenumber', 'case_auth_smsLogin_07_empty_smsCode'])])
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

    @allure.feature("认证授权模块")
    @allure.story("小程序登录")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_xcxLogin_02', 'case_auth_xcxLogin_03', 'case_auth_xcxLogin_04'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_auth_xcxLogin_01', 'case_auth_xcxLogin_02', 'case_auth_xcxLogin_03', 'case_auth_xcxLogin_04'])])
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
    pytest.main([r'D:\PytestAutoApi\test_case\interface_case\auth_ali\test_auth_ali.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
