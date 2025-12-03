
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

@allure.epic("mqtt_ali")
class Test_Mqtt_ali:

    @allure.feature("未分类")
    @allure.story("解绑设备同时")
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['case_mqtt_VirtualDeviceTest_unbind_01', 'case_mqtt_VirtualDeviceTest_unbind_02', 'case_mqtt_VirtualDeviceTest_unbind_03', 'case_mqtt_VirtualDeviceTest_unbind_04'])))), ids=[i['detail'] for i in GetTestCase.case_data(['case_mqtt_VirtualDeviceTest_unbind_01', 'case_mqtt_VirtualDeviceTest_unbind_02', 'case_mqtt_VirtualDeviceTest_unbind_03', 'case_mqtt_VirtualDeviceTest_unbind_04'])])
    def test_case_mqtt_VirtualDeviceTest_unbind(self, in_data, case_skip):
        allure.dynamic.title(f"case_mqtt_VirtualDeviceTest_unbind"+"_"+in_data["detail"])
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )


if __name__ == '__main__':
    pytest.main([r'D:\PytestAutoApi\test_case\interface_case\mqtt_ali\test_mqtt_ali.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
