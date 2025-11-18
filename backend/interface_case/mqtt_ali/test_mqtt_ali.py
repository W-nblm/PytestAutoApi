
# -*- coding: utf-8 -*-
# @Time    : 2025-11-18 16:05:35

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("mqtt_ali")
class Test_Mqtt_ali:

    @allure.feature("未分类")
    @allure.story("向设备下发实时命令")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_mqtt_VirtualDeviceTest_sendRealTimeCommand_01', 'case_mqtt_VirtualDeviceTest_sendRealTimeCommand_02', 'case_mqtt_VirtualDeviceTest_sendRealTimeCommand_03'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_mqtt_VirtualDeviceTest_sendRealTimeCommand_01', 'case_mqtt_VirtualDeviceTest_sendRealTimeCommand_02', 'case_mqtt_VirtualDeviceTest_sendRealTimeCommand_03'])])
    def test_case_mqtt_VirtualDeviceTest_sendRealTimeCommand(self, in_data, case_skip):
        allure.dynamic.title(f"case_mqtt_VirtualDeviceTest_sendRealTimeCommand"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.feature("未分类")
    @allure.story("向影子设备发送请求")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_mqtt_VirtualDeviceTest_sendShadowCommand_01_positive', 'case_mqtt_VirtualDeviceTest_sendShadowCommand_02_missing_devId', 'case_mqtt_VirtualDeviceTest_sendShadowCommand_03_invalid_productId_type', 'case_mqtt_VirtualDeviceTest_sendShadowCommand_04_missing_data_object'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_mqtt_VirtualDeviceTest_sendShadowCommand_01_positive', 'case_mqtt_VirtualDeviceTest_sendShadowCommand_02_missing_devId', 'case_mqtt_VirtualDeviceTest_sendShadowCommand_03_invalid_productId_type', 'case_mqtt_VirtualDeviceTest_sendShadowCommand_04_missing_data_object'])])
    def test_case_mqtt_VirtualDeviceTest_sendShadowCommand(self, in_data, case_skip):
        allure.dynamic.title(f"case_mqtt_VirtualDeviceTest_sendShadowCommand"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main([r'D:\PytestAutoApi\backend\interface_case\mqtt_ali\test_mqtt_ali.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
