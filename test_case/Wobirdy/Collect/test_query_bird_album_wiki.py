
# -*- coding: utf-8 -*-
# @Time    : 2025-06-27 16:51:02

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

case_id = ['wobirdy_query_bird_album_capture_wiki_01']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))

@allure.epic("WObird")
@allure.feature("我的收藏-云相册")
class TestQueryBirdAlbumWiki:

    @allure.story("单图片百科") 
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_query_bird_album_wiki(self, in_data,case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )
if __name__ == '__main__':
    pytest.main(['test_query_bird_album_wiki.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
