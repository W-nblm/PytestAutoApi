import ast
import json
from typing import Text, Dict, Any, Union
from jsonpath import jsonpath
from utils.other_tools.models import AssertMethod
from utils.logging_tool.log_control import ERROR, WARNING
from utils.read_files_tool.regular_control import cache_regular
from utils.other_tools.models import load_module_functions
from utils.assertion import assert_type
from utils.other_tools.exceptions import (
    JsonpathExtractionFailed,
    SqlNotFound,
    AssertTypeError,
)
from utils import config


class Assert:
    """封装assert"""

    def __init__(self, assert_data: Dict):
        self.assert_data = ast.literal_eval(cache_regular(str(assert_data)))
        self.functions_mapping = load_module_functions(assert_type)

    @staticmethod
    def _check_params(response_data: Text, sql_data: Union[Dict, None]) -> bool:
        """检查参数是否正确
        :param response_data: 响应数据
        :param sql_data: sql数据
        :return: bool
        """
        if (response_data and sql_data) is not False:
            if not isinstance(sql_data, dict):
                raise ValueError(
                    "断言失败,response_data、sql_data的数据类型必须要是字典类型,"
                    "请检查接口对应的数据是否正确\n"
                    f"sql_data: {sql_data}, 数据类型: {type(sql_data)}\n"
                )
        return True

    @staticmethod
    def res_sql_data_bytes(res_sql_data: Any) -> Text:
        """处理 mysql查询出来的数据类型如果是bytes类型,转换成str类型"""
        if isinstance(res_sql_data, bytes):
            res_sql_data = res_sql_data.decode("utf=8")
        return res_sql_data

    def sql_switch_handle(
        self,
        sql_data: Dict,
        assert_value: Any,
        key: Text,
        values: Any,
        resp_data: Dict,
        message: Text,
    ) -> None:
        """
        :param sql_data: 测试用例中的sql
        :param assert_value: 断言内容
        :param key:
        :param values:
        :param resp_data: 预期结果
        :param message: 预期结果
        :return:
        """
        # 判断数据库开关为关闭状态
        if config.mysql_db.switch is False:
            WARNING.logger.warning(
                f"数据库断言失败,原因: 数据库开关为关闭状态,请检查配置文件断言值:%s",
                values,
            )
        # 数据库为开启状态
        if config.mysql_db.switch is True:
            # 判断sql_data是否为空
            if sql_data != {"sql": None}:
                res_sql_data = jsonpath(sql_data, assert_value)
                if res_sql_data is False:
                    raise JsonpathExtractionFailed(
                        f"数据库断言内容jsonpath提取失败, 当前jsonpath内容: {assert_value}\n"
                        f"数据库返回内容: {sql_data}"
                    )
                # 判断mysql查询出来的数据类型如果是bytes类型，转换成str类型
                res_sql_data = self.res_sql_data_bytes(res_sql_data[0])
                name = AssertMethod(self.assert_data[key]["type"]).name
                self.functions_mapping[name](resp_data[0], res_sql_data, str(message))
            else:
                raise SqlNotFound(
                    f"数据库断言失败,原因: sql_data为空,请检查sql_data是否正确"
                )

    def assert_type_handle(
        self,
        assert_types: Union[Text, None],
        sql_data: Union[Dict, None],
        assert_value: Any,
        key: Text,
        values: Dict,
        resp_data: Any,
        message: Text,
    ) -> None:
        """处理断言类型"""
        if assert_types == "SQL":
            self.sql_switch_handle(
                sql_data=sql_data,
                assert_value=assert_value,
                key=key,
                values=values,
                resp_data=resp_data,
                message=message,
            )
        # AssertType为空
        elif assert_types is None:
            name = AssertMethod(self.assert_data[key]["type"]).name
            self.functions_mapping[name](resp_data[0], assert_value, message)
        else:
            raise AssertTypeError("断言失败，目前只支持数据库断言和响应断言")

    @classmethod
    def _message(cls, value):
        _message = ""
        if jsonpath(obj=value, expr="$.message") is not False:
            _message = value["message"]
        return _message

    def assert_equality(
        self, response_data: Text, sql_data: Dict, status_code: int
    ) -> None:
        """处理断言"""
        # 判断数据类型
        if self._check_params(response_data, sql_data) is not False:
            for key, values in self.assert_data.items():
                if key == "status_code":
                    assert (
                        status_code == values
                    ), f"断言失败, 期望状态码: {values}, 实际状态码: {status_code}"
                else:
                    assert_value = self.assert_data[key]["value"]
                    assert_jsonpath = self.assert_data[key]["jsonpath"]
                    assert_type = self.assert_data[key]["AssertType"]
                    resp_data = jsonpath(json.loads(response_data), assert_jsonpath)
                    message = self._message(value=values)
                    if resp_data is not False:
                        self.assert_type_handle(
                            assert_types=assert_type,
                            sql_data=sql_data,
                            assert_value=assert_value,
                            key=key,
                            values=values,
                            resp_data=resp_data,
                            message=message,
                        )
                    else:
                        ERROR.logger.error("JsonPath值获取失败 %s ", assert_jsonpath)
                        raise JsonpathExtractionFailed(
                            f"JsonPath值获取失败 {assert_jsonpath}"
                        )
