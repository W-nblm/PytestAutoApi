
# -*- coding: utf-8 -*-
# @Time    : 2025-08-09 10:47:40

import allure
import pytest
from utils.read_files_tool.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.request_tool.request_control import RequestControl
from utils.read_files_tool.regular_control import regular
from utils.request_tool.teardown_control import TearDownHandler
from utils.logging_tool.log_control import ERROR, INFO

@allure.epic("Feedback")
@allure.feature("Feedback")
class Test_Feedback:

    @allure.story("新增反馈")
    # @pytest.mark.order(1)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_addFeedback_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_addFeedback_01'])])
    def test_appdevice_info_feedback_userIssue_addFeedback(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("查询是否有未读消息 true:有未读消息 false:无未读消息")
    # @pytest.mark.order(6)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_checkMessageHint_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_checkMessageHint_01'])])
    def test_appdevice_info_feedback_userIssue_checkMessageHint(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("结单")
    # @pytest.mark.order(7)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_completeFeedback_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_completeFeedback_01'])])
    def test_appdevice_info_feedback_userIssue_completeFeedback_feedbackId(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("继续反馈")
    # @pytest.mark.order(4)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_continueFeedback_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_continueFeedback_01'])])
    def test_appdevice_info_feedback_userIssue_continueFeedback(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("查询工单详细情况")
    # @pytest.mark.order(5)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_queryDetailList_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_queryDetailList_01'])])
    def test_appdevice_info_feedback_userIssue_queryDetailList_feedbackId(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("查询用户反馈列表")
    # @pytest.mark.order(2)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_queryIssueList_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_queryIssueList_01'])])
    def test_appdevice_info_feedback_userIssue_queryIssueList(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )

    @allure.story("分页查询用户反馈列表")
    # @pytest.mark.order(3)
    @pytest.mark.parametrize('in_data', eval(regular(str(GetTestCase.case_data(['appdevice_info_feedback_userIssue_queryIssueListPage_01'])))), ids=[i['detail'] for i in GetTestCase.case_data(['appdevice_info_feedback_userIssue_queryIssueListPage_01'])])
    def test_appdevice_info_feedback_userIssue_queryIssueListPage(self, in_data, case_skip):
        INFO.logger.info("data: %s", in_data)
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(
            response_data=res.response_data,
            sql_data=res.sql_data,
            status_code=res.status_code,
        )
