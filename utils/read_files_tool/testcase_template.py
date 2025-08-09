import datetime
import os
from utils.read_files_tool.yaml_control import GetYamlData
from common.setting import ensure_path_sep
from utils.other_tools.exceptions import ValueNotFoundError


def write_case(case_path, page):
    """写入测试用例"""
    with open(case_path, "w", encoding="utf-8") as file:
        file.write(page)


def write_testcase_file(
    *,
    allure_epic,
    allure_feature,
    class_title,
    func_title,
    case_path,
    case_ids,
    file_name,
    allure_story,
):

    conf_data = GetYamlData(ensure_path_sep("\\common\\config.yaml")).get_yaml_data()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    real_time_update_test_cases = conf_data.get("real_time_update_test_cases")
    page = f"""
# -*- coding: utf-8 -*-
# @Time    : {now}

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

case_id = {case_ids}
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))

@allure.epic("{allure_epic}")
@allure.feature("{allure_feature}")
class Test{class_title}:

    @allure.story("{allure_story}") 
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_{func_title}(self, in_data,case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )
if __name__ == '__main__':
    pytest.main(['{file_name}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
"""
    print(file_name,case_path)
    if real_time_update_test_cases:
        write_case(case_path=case_path, page=page)
    elif real_time_update_test_cases is False:
        if not os.path.exists(case_path):
            
            write_case(case_path=case_path, page=page)
    else:
        raise ValueNotFoundError("real_time_update_test_cases must be True or False")

    # path, filename = os.path.split(case_path)
