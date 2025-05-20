import ast
import os
import random
import time
import urllib
from typing import Tuple, Dict, Union, Text
import requests
import urllib3
from requests_toolbelt import MultipartEncoder
from common.setting import ensure_path_sep
from utils.other_tools.models import RequestType
from utils.logging_tool.log_decorator import log_decorator
from utils.mysql_tool.mysql_control import AssertExecution
from utils.logging_tool.run_time_decorator import execution_duration
from utils.other_tools.allure_data.allure_tools import (
    allure_step,
    allure_step_no,
    allure_attach,
)
from utils.read_files_tool.regular_control import cache_regular
from utils.request_tool.set_current_request_cache import SetCurrentRequestCache
from utils.other_tools.models import TestCase, ResponseData
from utils import config
from utils.logging_tool.log_control import ERROR, INFO


# 封装请求
class RequestControl:
    def __init__(self, yaml_case):
        self.__yaml_case = TestCase(**yaml_case)

    # 判断上传文件时，data参数书是否存在
    def file_data_exit(self, file_data):
        try:
            _data = self.__yaml_case.data
            for key, value in ast.literal_eval(cache_regular(str(_data)))[
                "data"
            ].items():
                file_data[key] = value
        except KeyError:
            pass

    @classmethod
    def multipart_data(cls, file_data: Dict):
        """
        处理上传文件
        :param file_data:
        :return:
        """
        multipart_data = MultipartEncoder(
            fields=file_data,
            boundary="-----------------------------"
            + str(random.randint(int(1e28), int(1e29 - 1))),
        )
        return multipart_data

    @classmethod
    def check_headers_str_null(cls, headers: Dict) -> Dict:
        """
        处理headers参数,将字符串None转换为None类型
        :param headers:
        :return:
        """
        headers = ast.literal_eval(cache_regular(str(headers)))
        if headers is None:
            headers = {"headers": None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
        return headers

    @classmethod
    def multipart_in_headers(cls, request_data: Dict, headers: Dict):
        """
        判断headers中是否存在上传文件
        :param request_data:
        :param headers:
        :return:
        """
        headers = ast.literal_eval(cache_regular(str(headers)))
        request_data = ast.literal_eval(cache_regular(str(request_data)))
        if headers is not None:
            headers = {"headers": None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
            if "multipart/form-data" in str(headers.values()):
                # 判断请求参数不为空，且参数为字典
                if request_data is not None and isinstance(request_data, dict):
                    # 当 Content-Type 为 "multipart/form-data"时，需要将数据类型转换成 str
                    for key, value in request_data.items():
                        if isinstance(value, str):
                            request_data[key] = str(value)
                    request_data = MultipartEncoder(request_data)
                    headers["Content-Type"] = request_data.content_type
        return request_data, headers

    def file_params_exit(self):
        """
        判断是否存在上传文件
        :return:
        """
        try:
            params = self.__yaml_case.data["params"]
        except KeyError:
            params = None
        return params

    @classmethod
    def text_encode(cls, text: Text) -> Text:
        return text.encode("utf-8").decode("utf-8")

    @classmethod
    def response_elapsed_total_seconds(cls, response):
        """
        获取响应时间
        :param response:
        :return:
        """
        try:
            return round(response.elapsed.total_seconds() * 1000, 2)
        except AttributeError:
            return 0

    def upload_file(self) -> Tuple:
        """
        处理上传文件
        :return:
        """

        # 处理上传多个文件
        _files = []
        file_data = {}

        # 兼容上传其它类型参数
        self.file_data_exit(file_data)
        _data = self.__yaml_case.data
        for key, value in ast.literal_eval(cache_regular(str(_data)))["file"].items():
            file_path = ensure_path_sep("\\Files\\" + value)
            file_data[key] = (
                value,
                open(file_path, "rb"),
                f"image/{value.split('.')[-1]}",
            )
            _files.append(key)
            allure_attach(source=file_path, name=value, extension=value)
        multipart = self.multipart_data(file_data)
        INFO.logger.info(f"上传文件：{_files}")
        INFO.logger.info(f"上传文件数据：{file_data}")
        INFO.logger.info(f"上传文件数据类型：{multipart}")
        INFO.logger.info(f"上传文件数据类型：{multipart.content_type}")
        self.__yaml_case.headers["Content-Type"] = multipart.content_type
        params_data = ast.literal_eval(cache_regular(str(self.file_params_exit())))
        return multipart, params_data, self.__yaml_case

    def request_type_for_json(self, headers: Dict, method: Text, **kwargs):
        """
        处理json请求
        :param headers: 请求头
        :param method: 请求方法
        :param kwargs: 请求参数
        :return: 响应
        """
        _headers = self.check_headers_str_null(headers)
        _data = self.__yaml_case.data
        _url = self.__yaml_case.url
        response = requests.request(
            method=method,
            url=cache_regular(_url),
            headers=_headers,
            json=ast.literal_eval(cache_regular(str(_data))),
            verify=False,
            params=None,
            **kwargs,
        )
        return response

    def request_type_for_none(self, headers: Dict, method: Text, **kwargs):
        """
        处理无请求参数的请求
        :param headers: 请求头
        :param method: 请求方法
        :param kwargs: 请求参数
        :return: 响应
        """
        _headers = self.check_headers_str_null(headers)
        _url = self.__yaml_case.url
        response = requests.request(
            method=method,
            url=cache_regular(_url),
            headers=_headers,
            data=None,
            verify=False,
            params=None,
            **kwargs,
        )
        return response

    def request_type_for_params(self, headers: Dict, method: Text, **kwargs):
        """
        处理请求参数
        :param headers: 请求头
        :param method: 请求方法
        :param kwargs: 请求参数
        :return: 响应
        """
        _headers = self.check_headers_str_null(headers)
        _data = self.__yaml_case.data
        _url = self.__yaml_case.url
        if _data is not None:
            # 拼接url
            params_data = "?"
            for key, value in _data.items():
                if value is None or value == "":
                    params_data += key + "&"
                else:
                    params_data += key + "=" + str(value) + "&"
            _url += params_data[:-1]
        response = requests.request(
            method=method,
            url=cache_regular(_url),
            headers=_headers,
            data=None,
            verify=False,
            params=None,
            **kwargs,
        )
        return response

    def request_type_for_file(self, headers: Dict, method: Text, **kwargs):
        """
        处理requestType为file的请求
        :param headers: 上传文件请求头
        :param method: 请求方法
        :param kwargs: 请求参数
        :return: 响应
        """
        multipart = self.upload_file()
        yaml_data = multipart[2]
        _headers = multipart[2].headers
        _headers = self.check_headers_str_null(_headers)
        response = requests.request(
            method=method,
            url=cache_regular(yaml_data.url),
            data=multipart[0],
            params=multipart[1],
            headers=ast.literal_eval(cache_regular(str(_headers))),
            verify=False,
            **kwargs,
        )
        return response

    def request_type_for_data(self, headers: Dict, method: Text, **kwargs):
        """
        处理requestType为data的请求
        :param headers: 请求头
        :param method: 请求方法
        :param kwargs: 请求参数
        :return: 响应
        """
        data = self.__yaml_case.data
        _data, _headers = self.multipart_in_headers(
            ast.literal_eval(cache_regular(str(data))), headers
        )
        _url = self.__yaml_case.url
        response = requests.request(
            method=method,
            url=cache_regular(_url),
            data=_data,
            headers=_headers,
            verify=False,
            **kwargs,
        )
        return response

    @classmethod
    def get_export_api_filename(cls, response):
        """
        获取导出接口文件名
        :param response:
        :return:
        """
        try:
            _content_disposition = response.headers["Content-Disposition"]
            _filename = _content_disposition.split("=")[-1]
            _filename = urllib.parse.unquote(_filename)
        except KeyError:
            _filename = "未获取到文件名"
        return _filename

    def request_type_for_export(self, headers: Dict, method: Text, **kwargs):
        """
        处理导出接口请求
        :param headers: 请求头
        :param method: 请求方法
        :param kwargs: 请求参数
        :return: 响应
        """
        _headers = self.check_headers_str_null(headers)
        _url = self.__yaml_case.url
        _data = self.__yaml_case.data
        response = requests.request(
            method=method,
            url=cache_regular(_url),
            headers=_headers,
            json=ast.literal_eval(cache_regular(str(_data))),
            verify=False,
            params=None,
            data={} ** kwargs,
        )
        file_path = os.path.join(
            ensure_path_sep("\\Files\\"), self.get_export_api_filename(response)
        )
        if response.status_code == 200:
            if response.text:
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
            else:
                ERROR.logger.error("导出接口返回为空")
        return response

    @classmethod
    def _request_body_handler(cls, data: Dict, request_type: Text) -> Union[None, Dict]:
        """
        处理请求体
        :param data: 请求参数
        :param request_body: 请求体
        :return:
        """
        if request_type.upper() == "Params":
            return None
        else:
            return data

    @classmethod
    def _sql_data_handler(cls, sql_data, response):
        """
        处理sql数据
        :param sql_data: sql数据
        :param response: 响应
        :return:
        """
        if config.mysql_db.switch and sql_data is not None:
            sql_data = AssertExecution().assert_execution(sql_data, response)
        else:
            sql_data = {"sql": None}
        return sql_data

    def _check_params(self, res, yaml_data: "TestCase") -> "ResponseData":
        data = ast.literal_eval(cache_regular(str(yaml_data.data)))
        _data = {
            "url": res.url,
            "is_run": yaml_data.is_run,
            "detail": yaml_data.detail,
            "response_data": res.text,
            # 这个用于日志专用，判断如果是get请求，直接打印url
            "request_body": self._request_body_handler(data, yaml_data.requestType),
            "method": res.request.method,
            "sql_data": self._sql_data_handler(
                sql_data=ast.literal_eval(cache_regular(str(yaml_data.sql))),
                response=res,
            ),
            "yaml_data": yaml_data,
            "headers": res.request.headers,
            "cookie": res.cookies,
            "assert_data": yaml_data.assert_data,
            "res_time": self.response_elapsed_total_seconds(res),
            "status_code": res.status_code,
            "teardown": yaml_data.teardown,
            "teardown_sql": yaml_data.teardown_sql,
            "body": data,
        }
        # 抽离出通用模块，判断 http_request 方法中的一些数据校验
        return ResponseData(**_data)

    @classmethod
    def api_allure_step(
        cls,
        *,
        url: Text,
        headers: Text,
        method: Text,
        data: Text,
        assert_data: Text,
        res_time: Text,
        res: Text,
    ) -> None:
        """在allure中记录请求数据"""
        allure_step_no(f"请求URL: {url}")
        allure_step_no(f"请求方式: {method}")
        allure_step("请求头: ", headers)
        allure_step("请求数据: ", data)
        allure_step("预期数据: ", assert_data)
        _res_time = res_time
        allure_step_no(f"响应耗时(ms): {str(_res_time)}")
        allure_step("响应结果: ", res)

    @log_decorator(True)
    @execution_duration(3000)
    # @encryption("md5")
    def http_request(self, dependent_switch=True, **kwargs):
        """
        请求封装
        :param dependent_switch:
        :param kwargs:
        :return:
        """
        from utils.request_tool.dependent_case import DependentCase

        requests_type_mapping = {
            RequestType.JSON.value: self.request_type_for_json,
            RequestType.NONE.value: self.request_type_for_none,
            RequestType.PARAMS.value: self.request_type_for_params,
            RequestType.FILE.value: self.request_type_for_file,
            RequestType.DATA.value: self.request_type_for_data,
            RequestType.EXPORT.value: self.request_type_for_export,
        }

        is_run = ast.literal_eval(cache_regular(str(self.__yaml_case.is_run)))
        # 判断用例是否执行
        if is_run is True or is_run is None:
            # 处理多业务逻辑
            if dependent_switch is True:
                DependentCase(self.__yaml_case).get_dependent_data()
            INFO.logger.info(f"---------------处理多业务逻辑结束---------------")
            INFO.logger.info(f"---------------开始请求---------------")
            res = requests_type_mapping.get(self.__yaml_case.requestType)(
                headers=self.__yaml_case.headers,
                method=self.__yaml_case.method,
                **kwargs,
            )
            INFO.logger.info(f"---------------请求结束----------------")
            if self.__yaml_case.sleep is not None:
                time.sleep(self.__yaml_case.sleep)

            _res_data = self._check_params(res=res, yaml_data=self.__yaml_case)
            self.api_allure_step(
                url=_res_data.url,
                headers=str(_res_data.headers),
                method=_res_data.method,
                data=str(_res_data.body),
                assert_data=str(_res_data.assert_data),
                res_time=str(_res_data.res_time),
                res=_res_data.response_data,
            )
            # 将当前请求数据存入缓存中
            SetCurrentRequestCache(
                current_request_set_cache=self.__yaml_case.current_request_set_cache,
                request_data=self.__yaml_case.data,
                response_data=res,
            ).set_caches_main()

            return _res_data
        
