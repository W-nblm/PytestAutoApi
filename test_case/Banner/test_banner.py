
# -*- coding: utf-8 -*-
# @Time    : 2025-08-11 14:38:44

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("Banner")
@allure.feature("Banner")
class Test_Banner:

    @allure.story("添加banner")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_add_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_add_01'])])
    def test_banner_add(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("banner list")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_cancel_publish_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_cancel_publish_01'])])
    def test_banner_cancel_publish(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("banner delete接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_delete_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_delete_01'])])
    def test_banner_delete(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("获取banner详细信息")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_detail_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_detail_01'])])
    def test_banner_detail(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("banner edit接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_edit_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_edit_01'])])
    def test_banner_edit(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("banner list")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_list_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_list_01'])])
    def test_banner_list(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("banner publish")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['banner_publish_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['banner_publish_01'])])
    def test_banner_publish(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main(['d:\PytestAutoApi\test_case\Banner\test_banner.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
