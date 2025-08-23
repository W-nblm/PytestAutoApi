
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

@allure.epic("Favorite")
class Test_Favorite:

    @allure.feature("我的收藏-云相册")
    @allure.story("图片识别")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_bird_ai_album_by_image_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_bird_ai_album_by_image_01'])])
    def test_appdevice_info_birdAlbum_birdAiAlbumByImage(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdAlbum_birdAiAlbumByImage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("我的收藏-云相册")
    @allure.story("图片删除")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_delete_bird_album_image_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_delete_bird_album_image_01'])])
    def test_appdevice_info_birdAlbum_deleteBirdAlbumImage(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdAlbum_deleteBirdAlbumImage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("我的收藏-云相册")
    @allure.story("列表")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_query_bird_album_page_01', 'wobirdy_query_bird_album_page_02', 'wobirdy_query_bird_album_page_03', 'wobirdy_query_bird_album_page_04', 'wobirdy_query_bird_album_page_05'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_query_bird_album_page_01', 'wobirdy_query_bird_album_page_02', 'wobirdy_query_bird_album_page_03', 'wobirdy_query_bird_album_page_04', 'wobirdy_query_bird_album_page_05'])])
    def test_appdevice_info_birdAlbum_queryBirdAlbumPage(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdAlbum_queryBirdAlbumPage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("我的收藏-云相册")
    @allure.story("单图片百科")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_query_bird_album_capture_wiki_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_query_bird_album_capture_wiki_01'])])
    def test_appdevice_info_birdAlbum_queryBirdCaptureWiki_eventId(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdAlbum_queryBirdCaptureWiki_eventId"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("本地图片识别")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_bird_ai_by_image_and_save_capture_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_bird_ai_by_image_and_save_capture_01'])])
    def test_appdevice_info_birdMoment_birdAiByImageAndSaveCapture(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_birdAiByImageAndSaveCapture"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("图片识别")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_bird_ai_capture_by_image_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_bird_ai_capture_by_image_01'])])
    def test_appdevice_info_birdMoment_birdAiCaptureByImage(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_birdAiCaptureByImage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("收藏")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_capture_favorites_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_capture_favorites_01'])])
    def test_appdevice_info_birdMoment_captureFavorites(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_captureFavorites"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("鸟类首页 收藏")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_birdMoment_captureFavorites_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_birdMoment_captureFavorites_01'])])
    def test_appdevice_info_birdMoment_captureFavorites_eventId(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_captureFavorites_eventId"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("鸟类 云录像, 统计")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_birdMoment_countBydata_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_birdMoment_countBydata_01'])])
    def test_appdevice_info_birdMoment_countBydata(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_countBydata"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("图片删除")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_delete_bird_capture_image_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_delete_bird_capture_image_01'])])
    def test_appdevice_info_birdMoment_deleteBirdCaptureImage(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_deleteBirdCaptureImage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("智趣瞬间")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_query_bird_capture_page_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_query_bird_capture_page_01'])])
    def test_appdevice_info_birdMoment_queryBirdCapturePage(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_queryBirdCapturePage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("鸟类首页")
    @allure.story("单图片百科")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['wobirdy_query_bird_capture_wiki_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['wobirdy_query_bird_capture_wiki_01'])])
    def test_appdevice_info_birdMoment_queryBirdCaptureWiki_eventId(self, in_data, case_skip):
        allure.dynamic.title(f"appdevice_info_birdMoment_queryBirdCaptureWiki_eventId"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main(['d:\PytestAutoApi\test_case\Wobirdy\Favorite\test_favorite.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
