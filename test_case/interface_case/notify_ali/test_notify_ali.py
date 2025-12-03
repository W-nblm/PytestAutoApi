
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

@allure.epic("notify_ali")
class Test_Notify_ali:

    @allure.feature("未分类")
    @allure.story("二级页面-系统消息删除接口单个多个删除  包含wocam与wopet系统消息单个多个删除 wocam wobirdy 传 123 wopet 传 45")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_deleteAlarmMessageNotify_01_success_wobird_single', 'case_notify_info_notify_deleteAlarmMessageNotify_02_success_wopet_multiple', 'case_notify_info_notify_deleteAlarmMessageNotify_03_error_missing_userId', 'case_notify_info_notify_deleteAlarmMessageNotify_04_error_invalid_type'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_deleteAlarmMessageNotify_01_success_wobird_single', 'case_notify_info_notify_deleteAlarmMessageNotify_02_success_wopet_multiple', 'case_notify_info_notify_deleteAlarmMessageNotify_03_error_missing_userId', 'case_notify_info_notify_deleteAlarmMessageNotify_04_error_invalid_type'])])
    def test_case_notify_info_notify_deleteAlarmMessageNotify(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_deleteAlarmMessageNotify"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("二级页面-告警消息单个设备删除全部接口  WOcam WObirdy适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_deleteDetectAllMessageNotify_01', 'case_notify_info_notify_deleteDetectAllMessageNotify_02', 'case_notify_info_notify_deleteDetectAllMessageNotify_03', 'case_notify_info_notify_deleteDetectAllMessageNotify_04'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_deleteDetectAllMessageNotify_01', 'case_notify_info_notify_deleteDetectAllMessageNotify_02', 'case_notify_info_notify_deleteDetectAllMessageNotify_03', 'case_notify_info_notify_deleteDetectAllMessageNotify_04'])])
    def test_case_notify_info_notify_deleteDetectAllMessageNotify(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_deleteDetectAllMessageNotify"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("二级页面-告警消息单个多个删除  WOcam WObirdy适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_deleteDetectMessageNotify_01_success_single', 'case_notify_info_notify_deleteDetectMessageNotify_02_success_multiple', 'case_notify_info_notify_deleteDetectMessageNotify_03_missing_devId', 'case_notify_info_notify_deleteDetectMessageNotify_04_missing_userId', 'case_notify_info_notify_deleteDetectMessageNotify_05_missing_messageId_in_list', 'case_notify_info_notify_deleteDetectMessageNotify_06_empty_messageDeleteVoList', 'case_notify_info_notify_deleteDetectMessageNotify_07_invalid_nowDate_type'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_deleteDetectMessageNotify_01_success_single', 'case_notify_info_notify_deleteDetectMessageNotify_02_success_multiple', 'case_notify_info_notify_deleteDetectMessageNotify_03_missing_devId', 'case_notify_info_notify_deleteDetectMessageNotify_04_missing_userId', 'case_notify_info_notify_deleteDetectMessageNotify_05_missing_messageId_in_list', 'case_notify_info_notify_deleteDetectMessageNotify_06_empty_messageDeleteVoList', 'case_notify_info_notify_deleteDetectMessageNotify_07_invalid_nowDate_type'])])
    def test_case_notify_info_notify_deleteDetectMessageNotify(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_deleteDetectMessageNotify"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("消息开关上报接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_enableMessageNotify_01', 'case_notify_info_notify_enableMessageNotify_02', 'case_notify_info_notify_enableMessageNotify_03', 'case_notify_info_notify_enableMessageNotify_04'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_enableMessageNotify_01', 'case_notify_info_notify_enableMessageNotify_02', 'case_notify_info_notify_enableMessageNotify_03', 'case_notify_info_notify_enableMessageNotify_04'])])
    def test_case_notify_info_notify_enableMessageNotify(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_enableMessageNotify"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("勿扰配置上报 Wopet适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_enableMessageNotifyDisturb_01_success_all_everyday', 'case_notify_info_notify_enableMessageNotifyDisturb_02_success_specific_devices_periods_nextday', 'case_notify_info_notify_enableMessageNotifyDisturb_03_missing_userid', 'case_notify_info_notify_enableMessageNotifyDisturb_04_invalid_id_type', 'case_notify_info_notify_enableMessageNotifyDisturb_05_invalid_disturbEnable_value', 'case_notify_info_notify_enableMessageNotifyDisturb_06_isAllDevice_0_empty_deviceList', 'case_notify_info_notify_enableMessageNotifyDisturb_07_isEveryDay_0_empty_periodList'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_enableMessageNotifyDisturb_01_success_all_everyday', 'case_notify_info_notify_enableMessageNotifyDisturb_02_success_specific_devices_periods_nextday', 'case_notify_info_notify_enableMessageNotifyDisturb_03_missing_userid', 'case_notify_info_notify_enableMessageNotifyDisturb_04_invalid_id_type', 'case_notify_info_notify_enableMessageNotifyDisturb_05_invalid_disturbEnable_value', 'case_notify_info_notify_enableMessageNotifyDisturb_06_isAllDevice_0_empty_deviceList', 'case_notify_info_notify_enableMessageNotifyDisturb_07_isEveryDay_0_empty_periodList'])])
    def test_case_notify_info_notify_enableMessageNotifyDisturb(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_enableMessageNotifyDisturb"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("FW90消息开关上报 Wopet适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_enableNotifyEnableByType_01_positive_all_on_off', 'case_notify_info_notify_enableNotifyEnableByType_02_negative_missing_devId', 'case_notify_info_notify_enableNotifyEnableByType_03_negative_invalid_offlineEnable_value'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_enableNotifyEnableByType_01_positive_all_on_off', 'case_notify_info_notify_enableNotifyEnableByType_02_negative_missing_devId', 'case_notify_info_notify_enableNotifyEnableByType_03_negative_invalid_offlineEnable_value'])])
    def test_case_notify_info_notify_enableNotifyEnableByType(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_enableNotifyEnableByType"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("消息推送测试接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_notifyMessage_01_success', 'case_notify_info_notify_notifyMessage_02_missing_userId', 'case_notify_info_notify_notifyMessage_03_invalid_appType', 'case_notify_info_notify_notifyMessage_04_empty_msgTitle'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_notifyMessage_01_success', 'case_notify_info_notify_notifyMessage_02_missing_userId', 'case_notify_info_notify_notifyMessage_03_invalid_appType', 'case_notify_info_notify_notifyMessage_04_empty_msgTitle'])])
    def test_case_notify_info_notify_notifyMessage(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_notifyMessage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("三级页面-查询设备系统消息详情接口 WOcam wobird适用 适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryAlarmMessageNotifyDetail_01_success', 'case_notify_info_notify_queryAlarmMessageNotifyDetail_02_missing_devId', 'case_notify_info_notify_queryAlarmMessageNotifyDetail_03_invalid_messageId_type', 'case_notify_info_notify_queryAlarmMessageNotifyDetail_04_empty_devId'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryAlarmMessageNotifyDetail_01_success', 'case_notify_info_notify_queryAlarmMessageNotifyDetail_02_missing_devId', 'case_notify_info_notify_queryAlarmMessageNotifyDetail_03_invalid_messageId_type', 'case_notify_info_notify_queryAlarmMessageNotifyDetail_04_empty_devId'])])
    def test_case_notify_info_notify_queryAlarmMessageNotifyDetail(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryAlarmMessageNotifyDetail"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("二级页面-查询系统消息列表接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryAlarmMessageNotifyList_01_success_full_params', 'case_notify_info_notify_queryAlarmMessageNotifyList_02_success_min_params', 'case_notify_info_notify_queryAlarmMessageNotifyList_03_missing_type', 'case_notify_info_notify_queryAlarmMessageNotifyList_04_missing_userId', 'case_notify_info_notify_queryAlarmMessageNotifyList_05_invalid_type_value', 'case_notify_info_notify_queryAlarmMessageNotifyList_06_empty_userId', 'case_notify_info_notify_queryAlarmMessageNotifyList_07_invalid_pageSize', 'case_notify_info_notify_queryAlarmMessageNotifyList_08_invalid_pageNum'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryAlarmMessageNotifyList_01_success_full_params', 'case_notify_info_notify_queryAlarmMessageNotifyList_02_success_min_params', 'case_notify_info_notify_queryAlarmMessageNotifyList_03_missing_type', 'case_notify_info_notify_queryAlarmMessageNotifyList_04_missing_userId', 'case_notify_info_notify_queryAlarmMessageNotifyList_05_invalid_type_value', 'case_notify_info_notify_queryAlarmMessageNotifyList_06_empty_userId', 'case_notify_info_notify_queryAlarmMessageNotifyList_07_invalid_pageSize', 'case_notify_info_notify_queryAlarmMessageNotifyList_08_invalid_pageNum'])])
    def test_case_notify_info_notify_queryAlarmMessageNotifyList(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryAlarmMessageNotifyList"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("二级页面-查询告警消息列表接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryDetectMessageNotifyList_01_success_default_query', 'case_notify_info_notify_queryDetectMessageNotifyList_02_success_time_range_query', 'case_notify_info_notify_queryDetectMessageNotifyList_03_error_missing_devId', 'case_notify_info_notify_queryDetectMessageNotifyList_04_error_missing_userId', 'case_notify_info_notify_queryDetectMessageNotifyList_05_error_empty_devId', 'case_notify_info_notify_queryDetectMessageNotifyList_06_error_invalid_pageSize', 'case_notify_info_notify_queryDetectMessageNotifyList_07_error_invalid_pageNum', 'case_notify_info_notify_queryDetectMessageNotifyList_08_error_invalid_time_range', 'case_notify_info_notify_queryDetectMessageNotifyList_09_error_invalid_shareFlag'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryDetectMessageNotifyList_01_success_default_query', 'case_notify_info_notify_queryDetectMessageNotifyList_02_success_time_range_query', 'case_notify_info_notify_queryDetectMessageNotifyList_03_error_missing_devId', 'case_notify_info_notify_queryDetectMessageNotifyList_04_error_missing_userId', 'case_notify_info_notify_queryDetectMessageNotifyList_05_error_empty_devId', 'case_notify_info_notify_queryDetectMessageNotifyList_06_error_invalid_pageSize', 'case_notify_info_notify_queryDetectMessageNotifyList_07_error_invalid_pageNum', 'case_notify_info_notify_queryDetectMessageNotifyList_08_error_invalid_time_range', 'case_notify_info_notify_queryDetectMessageNotifyList_09_error_invalid_shareFlag'])])
    def test_case_notify_info_notify_queryDetectMessageNotifyList(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryDetectMessageNotifyList"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("FW90喂食记录列表查询 Wopet适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryFeedRecordsList_01_success', 'case_notify_info_notify_queryFeedRecordsList_02_missing_userId', 'case_notify_info_notify_queryFeedRecordsList_03_missing_devId', 'case_notify_info_notify_queryFeedRecordsList_04_invalid_param_types'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryFeedRecordsList_01_success', 'case_notify_info_notify_queryFeedRecordsList_02_missing_userId', 'case_notify_info_notify_queryFeedRecordsList_03_missing_devId', 'case_notify_info_notify_queryFeedRecordsList_04_invalid_param_types'])])
    def test_case_notify_info_notify_queryFeedRecordsList(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryFeedRecordsList"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("一级页面-查询告警设备列表  系统设备列表接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryMessageDeviceList_01_success', 'case_notify_info_notify_queryMessageDeviceList_02_success_messageType_2', 'case_notify_info_notify_queryMessageDeviceList_03_empty_result', 'case_notify_info_notify_queryMessageDeviceList_04_missing_messageType', 'case_notify_info_notify_queryMessageDeviceList_05_missing_userId', 'case_notify_info_notify_queryMessageDeviceList_06_invalid_messageType_value', 'case_notify_info_notify_queryMessageDeviceList_07_invalid_userId_empty', 'case_notify_info_notify_queryMessageDeviceList_08_invalid_pageSize_negative', 'case_notify_info_notify_queryMessageDeviceList_09_invalid_pageNum_zero'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryMessageDeviceList_01_success', 'case_notify_info_notify_queryMessageDeviceList_02_success_messageType_2', 'case_notify_info_notify_queryMessageDeviceList_03_empty_result', 'case_notify_info_notify_queryMessageDeviceList_04_missing_messageType', 'case_notify_info_notify_queryMessageDeviceList_05_missing_userId', 'case_notify_info_notify_queryMessageDeviceList_06_invalid_messageType_value', 'case_notify_info_notify_queryMessageDeviceList_07_invalid_userId_empty', 'case_notify_info_notify_queryMessageDeviceList_08_invalid_pageSize_negative', 'case_notify_info_notify_queryMessageDeviceList_09_invalid_pageNum_zero'])])
    def test_case_notify_info_notify_queryMessageDeviceList(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryMessageDeviceList"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("消息管理")
    @allure.story("消息开关查询接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryMessageNotifyEnable_01_success', 'case_notify_info_notify_queryMessageNotifyEnable_02_missing_userId', 'case_notify_info_notify_queryMessageNotifyEnable_03_missing_appType', 'case_notify_info_notify_queryMessageNotifyEnable_04_invalid_appType', 'case_notify_info_notify_queryMessageNotifyEnable_05_empty_userId'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryMessageNotifyEnable_01_success', 'case_notify_info_notify_queryMessageNotifyEnable_02_missing_userId', 'case_notify_info_notify_queryMessageNotifyEnable_03_missing_appType', 'case_notify_info_notify_queryMessageNotifyEnable_04_invalid_appType', 'case_notify_info_notify_queryMessageNotifyEnable_05_empty_userId'])])
    def test_case_notify_info_notify_queryMessageNotifyEnable(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryMessageNotifyEnable"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("一级页面-查询通知消息列表接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryMessageNotifyList_01', 'case_notify_info_notify_queryMessageNotifyList_02', 'case_notify_info_notify_queryMessageNotifyList_03'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryMessageNotifyList_01', 'case_notify_info_notify_queryMessageNotifyList_02', 'case_notify_info_notify_queryMessageNotifyList_03'])])
    def test_case_notify_info_notify_queryMessageNotifyList(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryMessageNotifyList"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("FW90消息开关查询 Wopet适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryNotifyEnableByType_01_success', 'case_notify_info_notify_queryNotifyEnableByType_02_missing_devId', 'case_notify_info_notify_queryNotifyEnableByType_03_empty_devId', 'case_notify_info_notify_queryNotifyEnableByType_04_invalid_devId'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryNotifyEnableByType_01_success', 'case_notify_info_notify_queryNotifyEnableByType_02_missing_devId', 'case_notify_info_notify_queryNotifyEnableByType_03_empty_devId', 'case_notify_info_notify_queryNotifyEnableByType_04_invalid_devId'])])
    def test_case_notify_info_notify_queryNotifyEnableByType(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryNotifyEnableByType"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("通知开关通用查询  喂鸟器开关查询接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_queryNotifyEnableByTypeCom_01', 'case_notify_info_notify_queryNotifyEnableByTypeCom_02', 'case_notify_info_notify_queryNotifyEnableByTypeCom_03', 'case_notify_info_notify_queryNotifyEnableByTypeCom_04', 'case_notify_info_notify_queryNotifyEnableByTypeCom_05'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_queryNotifyEnableByTypeCom_01', 'case_notify_info_notify_queryNotifyEnableByTypeCom_02', 'case_notify_info_notify_queryNotifyEnableByTypeCom_03', 'case_notify_info_notify_queryNotifyEnableByTypeCom_04', 'case_notify_info_notify_queryNotifyEnableByTypeCom_05'])])
    def test_case_notify_info_notify_queryNotifyEnableByTypeCom(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_queryNotifyEnableByTypeCom"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("一级页面-消息已读接口全部  WOcam wobirdy适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_readAllMessage_01_success', 'case_notify_info_notify_readAllMessage_02_missing_isRead', 'case_notify_info_notify_readAllMessage_03_missing_userId', 'case_notify_info_notify_readAllMessage_04_invalid_isRead_value', 'case_notify_info_notify_readAllMessage_05_invalid_userId_value', 'case_notify_info_notify_readAllMessage_06_empty_body', 'case_notify_info_notify_readAllMessage_07_invalid_isRead_type'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_readAllMessage_01_success', 'case_notify_info_notify_readAllMessage_02_missing_isRead', 'case_notify_info_notify_readAllMessage_03_missing_userId', 'case_notify_info_notify_readAllMessage_04_invalid_isRead_value', 'case_notify_info_notify_readAllMessage_05_invalid_userId_value', 'case_notify_info_notify_readAllMessage_06_empty_body', 'case_notify_info_notify_readAllMessage_07_invalid_isRead_type'])])
    def test_case_notify_info_notify_readAllMessage(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_readAllMessage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("一级页面-消息已读接口单个 WOcam Wobirdy适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_readMessage_01_success_system_message', 'case_notify_info_notify_readMessage_02_success_alarm_message', 'case_notify_info_notify_readMessage_03_missing_userId', 'case_notify_info_notify_readMessage_04_invalid_messageType', 'case_notify_info_notify_readMessage_05_alarm_missing_devId', 'case_notify_info_notify_readMessage_06_system_invalid_alarmType', 'case_notify_info_notify_readMessage_07_invalid_isRead'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_readMessage_01_success_system_message', 'case_notify_info_notify_readMessage_02_success_alarm_message', 'case_notify_info_notify_readMessage_03_missing_userId', 'case_notify_info_notify_readMessage_04_invalid_messageType', 'case_notify_info_notify_readMessage_05_alarm_missing_devId', 'case_notify_info_notify_readMessage_06_system_invalid_alarmType', 'case_notify_info_notify_readMessage_07_invalid_isRead'])])
    def test_case_notify_info_notify_readMessage(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_readMessage"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("消息通知管理")
    @allure.story("一级页面-根据类型多选或者全选未读消息 Wopet适用")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_readMessageAllByType_01', 'case_notify_info_notify_readMessageAllByType_02', 'case_notify_info_notify_readMessageAllByType_03', 'case_notify_info_notify_readMessageAllByType_04', 'case_notify_info_notify_readMessageAllByType_05', 'case_notify_info_notify_readMessageAllByType_06', 'case_notify_info_notify_readMessageAllByType_07', 'case_notify_info_notify_readMessageAllByType_08', 'case_notify_info_notify_readMessageAllByType_09', 'case_notify_info_notify_readMessageAllByType_10', 'case_notify_info_notify_readMessageAllByType_11', 'case_notify_info_notify_readMessageAllByType_12', 'case_notify_info_notify_readMessageAllByType_13'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_readMessageAllByType_01', 'case_notify_info_notify_readMessageAllByType_02', 'case_notify_info_notify_readMessageAllByType_03', 'case_notify_info_notify_readMessageAllByType_04', 'case_notify_info_notify_readMessageAllByType_05', 'case_notify_info_notify_readMessageAllByType_06', 'case_notify_info_notify_readMessageAllByType_07', 'case_notify_info_notify_readMessageAllByType_08', 'case_notify_info_notify_readMessageAllByType_09', 'case_notify_info_notify_readMessageAllByType_10', 'case_notify_info_notify_readMessageAllByType_11', 'case_notify_info_notify_readMessageAllByType_12', 'case_notify_info_notify_readMessageAllByType_13'])])
    def test_case_notify_info_notify_readMessageAllByType(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_readMessageAllByType"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("根据类型查看消息状态")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_readMessageByType_01', 'case_notify_info_notify_readMessageByType_02', 'case_notify_info_notify_readMessageByType_03'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_readMessageByType_01', 'case_notify_info_notify_readMessageByType_02', 'case_notify_info_notify_readMessageByType_03'])])
    def test_case_notify_info_notify_readMessageByType(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_readMessageByType"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("通知开关上报通用查询  喂鸟器开关上报接口")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_notify_reportNotifyEnableByTypeCom_01', 'case_notify_info_notify_reportNotifyEnableByTypeCom_02', 'case_notify_info_notify_reportNotifyEnableByTypeCom_03', 'case_notify_info_notify_reportNotifyEnableByTypeCom_04'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_notify_reportNotifyEnableByTypeCom_01', 'case_notify_info_notify_reportNotifyEnableByTypeCom_02', 'case_notify_info_notify_reportNotifyEnableByTypeCom_03', 'case_notify_info_notify_reportNotifyEnableByTypeCom_04'])])
    def test_case_notify_info_notify_reportNotifyEnableByTypeCom(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_notify_reportNotifyEnableByTypeCom"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("清除设备token")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_notify_info_removeDeviceToken_01_success', 'case_notify_info_removeDeviceToken_02_missing_appType', 'case_notify_info_removeDeviceToken_03_missing_userId', 'case_notify_info_removeDeviceToken_04_invalid_appType_pattern', 'case_notify_info_removeDeviceToken_05_empty_userId', 'case_notify_info_removeDeviceToken_06_empty_appType', 'case_notify_info_removeDeviceToken_07_invalid_phoneType', 'case_notify_info_removeDeviceToken_08_invalid_id_type', 'case_notify_info_removeDeviceToken_09_unauthorized'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_notify_info_removeDeviceToken_01_success', 'case_notify_info_removeDeviceToken_02_missing_appType', 'case_notify_info_removeDeviceToken_03_missing_userId', 'case_notify_info_removeDeviceToken_04_invalid_appType_pattern', 'case_notify_info_removeDeviceToken_05_empty_userId', 'case_notify_info_removeDeviceToken_06_empty_appType', 'case_notify_info_removeDeviceToken_07_invalid_phoneType', 'case_notify_info_removeDeviceToken_08_invalid_id_type', 'case_notify_info_removeDeviceToken_09_unauthorized'])])
    def test_case_notify_info_removeDeviceToken(self, in_data, case_skip):
        allure.dynamic.title(f"case_notify_info_removeDeviceToken"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main([r'D:\PytestAutoApi\test_case\interface_case\notify_ali\test_notify_ali.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
