
# -*- coding: utf-8 -*-
# @Time    : 2025-08-11 14:17:03

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("03_Collect")
@allure.feature("03_Collect")
class Test_03_collect:

    @allure.story("图片识别")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_bird_ai_album_by_image_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_bird_ai_album_by_image_01'])])
    def test_bird_ai_album_by_image(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("图片删除")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_delete_bird_album_image_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_delete_bird_album_image_01'])])
    def test_delete_bird_album_image(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("列表")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_query_bird_album_page_01', 'wobirdy_query_bird_album_page_02', 'wobirdy_query_bird_album_page_03', 'wobirdy_query_bird_album_page_04', 'wobirdy_query_bird_album_page_05'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_query_bird_album_page_01', 'wobirdy_query_bird_album_page_02', 'wobirdy_query_bird_album_page_03', 'wobirdy_query_bird_album_page_04', 'wobirdy_query_bird_album_page_05'])])
    def test_query_bird_album_page(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("单图片百科")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_query_bird_album_capture_wiki_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_query_bird_album_capture_wiki_01'])])
    def test_query_bird_album_wiki(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main(['d:\PytestAutoApi\test_case\Wobirdy\03_Collect\test_03_collect.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
