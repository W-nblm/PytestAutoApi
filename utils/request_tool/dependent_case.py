import ast
import json
from typing import Any, Text, Dict, Union, List
from jsonpath import jsonpath
from utils.request_tool.request_control import RequestControl
from utils.mysql_tool.mysql_control import SetUpMySQL
from utils.read_files_tool.regular_control import regular, cache_regular
from utils.other_tools.jsonpath_data_replace import jsonpath_replace
from utils.logging_tool.log_control import ERROR, WARNING, INFO
from utils.other_tools.models import DependentType
from utils.other_tools.models import TestCase, DependentCaseData, DependentData
from utils.other_tools.exceptions import ValueNotFoundError
from utils.cache_process.cache_control import CacheHandler
from utils import config


# 处理依赖相关业务
class DependentCase:
    def __init__(self, dependent_yaml_case: TestCase):
        self.__yaml_case = dependent_yaml_case

    @classmethod
    def get_cache(cls, case_id: Text) -> Dict:
        """获取缓存中用例数据
        :param case_id: 依赖用例id
        :return: 缓存中用例数据
        """
        _case_data = CacheHandler.get_cache(case_id)
        return _case_data

    @classmethod
    def jsonpath_data(cls, obj: Dict, expr: Text) -> list:
        """获取jsonpath表达式对应的值
        :param obj: 待处理数据
        :param expr: jsonpath表达式
        :return: 表达式对应的值列表
        """
        _jsonpath_data = jsonpath(obj, expr)
        # 判断是否提取到数据
        if _jsonpath_data is False:
            raise ValueNotFoundError(f"表达式{expr}提取不到数据")
        return _jsonpath_data

    @classmethod
    def set_cache_value(cls, dependent_data: "DependentData") -> Union[Text, None]:
        """设置缓存值
        :param dependent_data: 依赖数据
        :return: 缓存值
        """
        try:
            return dependent_data.set_cache
        except KeyError:
            return None

    @classmethod
    def replace_key(cls, dependent_data: "DependentData"):
        """获取需要替换的内容"""
        try:
            _replace_key = dependent_data.replace_key
            return _replace_key
        except KeyError:
            return None

    def url_replace(
        self, replace_key: Text, jsonpath_datas: Dict, jsonpath_data: list
    ) -> None:
        """
        url中的动态参数替换
        # 如: 一般有些接口的参数在url中,并且没有参数名称, /api/v1/work/spu/approval/spuApplyDetails/{id}
        # 那么可以使用如下方式编写用例, 可以使用 $url_params{}替换,
        # 如/api/v1/work/spu/approval/spuApplyDetails/$url_params{id}
        :param jsonpath_data: jsonpath 解析出来的数据值
        :param replace_key: 用例中需要替换数据的 replace_key
        :param jsonpath_dates: jsonpath 存放的数据值
        :return:
        """
        if "$url_params" in replace_key:
            _url = self.__yaml_case.url.replace(replace_key, str(jsonpath_data[0]))
            jsonpath_datas["$.url"] = _url
        else:
            jsonpath_datas[replace_key] = jsonpath_data[0]

    def _dependent_type_for_sql(
        self,
        setup_sql: List,
        dependence_case_data: "DependentCaseData",
        jsonpath_datas: Dict,
    ) -> None:
        """
        判断依赖类型为 sql,程序中的依赖参数从 数据库中提取数据
        @param setup_sql: 前置sql语句
        @param dependence_case_data: 依赖的数据
        @param jsonpath_dates: 依赖相关的用例数据
        @return:
        """
        # 判断依赖数据类型
        if setup_sql is not None:
            if config.mysql_db.switch:
                setup_sql = ast.literal_eval(cache_regular(str(setup_sql)))
                # 数据库中提取数据
                sql_data = SetUpMySQL().setup_sql_data(setup_sql)
                # 依赖数据
                dependent_data = dependence_case_data.dependent_data
                for i in dependent_data:
                    _jsonpath = i.jsonpath
                    # 从查询结果中提取数据
                    jsonpath_data = self.jsonpath_data(obj=sql_data, expr=_jsonpath)
                    _set_value = self.set_cache_value(i)
                    _replace_key = self.replace_key(i)

                    # 判断是否需要缓存
                    if _set_value is not None:
                        CacheHandler.update_cache(
                            cache_name=_set_value, value=jsonpath_data[0]
                        )

                    # 判断是否需要替换
                    if _replace_key is not None:
                        self.url_replace(
                            replace_key=_replace_key,
                            jsonpath_datas=jsonpath_datas,
                            jsonpath_data=jsonpath_data,
                        )
            else:
                WARNING.logger.warning("检查到数据库开关为关闭状态，请确认配置")

    def dependent_handler(
        self,
        _jsonpath: Text,
        set_value: Text,
        replace_key: Text,
        jsonpath_datas: Dict,
        data: Dict,
        dependent_type: int,
    ) -> None:
        """
        依赖处理
        :param _jsonpath: 依赖数据jsonpath表达式
        :param set_value: 缓存值
        :param replace_key: 需要替换的key
        :param jsonpath_datas: 依赖相关的用例数据
        :param data: 依赖数据
        :param dependent_type: 依赖类型
        :return:
        """
        # 通过jsonpath获取到需要的数据
        jsonpath_data = self.jsonpath_data(obj=data, expr=_jsonpath)
        if set_value is not None:
            if len(jsonpath_data) > 1:
                CacheHandler.update_cache(cache_name=set_value, value=jsonpath_data)
            else:
                CacheHandler.update_cache(cache_name=set_value, value=jsonpath_data[0])
        if replace_key is not None:
            if dependent_type == 0:
                jsonpath_datas[replace_key] = jsonpath_data[0]
            self.url_replace(
                replace_key=replace_key,
                jsonpath_datas=jsonpath_datas,
                jsonpath_data=jsonpath_data,
            )

    def is_dependent(self) -> Union[Dict, bool]:
        """
        判断是否存在依赖
        """
        # 获取用例中dependent_type值
        _dependent_type = self.__yaml_case.dependence_case
        # 获取依赖数据
        _dependence_case_datas = self.__yaml_case.dependence_case_data
        _setup_sql = self.__yaml_case.setup_sql
        INFO.logger.info(f"_dependent_type: {_dependent_type}")
        INFO.logger.info(f"_dependence_case_datas: {_dependence_case_datas}")
        # 判断是否存在依赖
        if _dependent_type is True:
            jsonpath_datas = {}
            # 循环依赖数据
            try:
                for dependence_case_data in _dependence_case_datas:
                    _case_id = dependence_case_data.case_id
                    INFO.logger.info(f"********开始获取依赖数据: {_case_id}********")
                    if _case_id == "self":
                        self._dependent_type_for_sql(
                            setup_sql=_setup_sql,
                            dependence_case_data=dependence_case_data,
                            jsonpath_datas=jsonpath_datas,
                        )
                    else:
                        re_data = regular(str(self.get_cache(_case_id)))
                        re_data = ast.literal_eval(cache_regular(str(re_data)))
                        INFO.logger.info(
                            f"********获取依赖数据成功: {_case_id}********"
                        )
                        INFO.logger.info(f"依赖数据: {re_data}")
                        res = RequestControl(re_data).http_request()
                        INFO.logger.info(f"依赖响应数据: {res}")
                        if dependence_case_data.dependent_data is not None:
                            dependent_data = dependence_case_data.dependent_data
                            for i in dependent_data:
                                _case_id = dependence_case_data.case_id
                                _jsonpath = i.jsonpath
                                _request_data = self.__yaml_case.data
                                _replace_key = self.replace_key(i)
                                _set_value = self.set_cache_value(i)
                                if i.dependent_type == DependentType.RESPONSE.value:
                                    self.dependent_handler(
                                        _jsonpath=_jsonpath,
                                        set_value=_set_value,
                                        replace_key=_replace_key,
                                        jsonpath_datas=jsonpath_datas,
                                        data=json.loads(res.response_data),
                                        dependent_type=0,
                                    )
                                elif i.dependent_type == DependentType.REQUEST.value:
                                    self.dependent_handler(
                                        _jsonpath=_jsonpath,
                                        set_value=_set_value,
                                        replace_key=_replace_key,
                                        jsonpath_datas=jsonpath_datas,
                                        data=res.body,
                                        dependent_type=1,
                                    )
                                else:
                                    raise ValueError(
                                        "依赖的dependent_type不正确,只支持request、response、sql依赖\n"
                                        f"当前填写内容: {i.dependent_type}"
                                    )
                return jsonpath_datas
            except KeyError as exc:
                # pass
                raise ValueNotFoundError(
                    f"dependence_case_data依赖用例中,未找到 {exc} 参数，请检查是否填写"
                    f"如已填写,请检查是否存在yaml缩进问题"
                ) from exc
            except TypeError as exc:
                raise ValueNotFoundError(
                    "dependence_case_data下的所有内容均不能为空！"
                    "请检查相关数据是否填写，如已填写，请检查缩进问题"
                ) from exc
        else:
            return False

    # def get_dependent_data(self) -> None:
    #     """
    #     jsonpath 和 依赖的数据,进行替换
    #     :return:
    #     """
    #     _dependent_data = DependentCase(self.__yaml_case).is_dependent()
    #     INFO.logger.info(f"测试用例: {self.__yaml_case}")
    #     INFO.logger.info(f"依赖数据: {_dependent_data}")
    #     INFO.logger.info(f"测试用例数据: {type(self.__yaml_case.data)}")
    #     _new_data = ""
    #     # 判断有依赖
    #     if _dependent_data is not None and _dependent_data is not False:
    #         # if _dependent_data is not False:
    #         for key, value in _dependent_data.items():
    #             # 通过jsonpath判断出需要替换数据的位置
    #             _change_data = key.split(".")
    #             INFO.logger.info(f"替换数据: {_change_data}")
    #             # jsonpath 数据解析
    #             # 不要删 这个yaml_case
    #             yaml_case = self.__yaml_case
    #             _new_data = jsonpath_replace(
    #                 change_data=_change_data, key_name="yaml_case"
    #             )
    #             # 最终提取到的数据,转换成 __yaml_case.data
    #             _new_data += " = " + repr(value)
    #             INFO.logger.info(f"Exec: {_new_data}")
    #             # 明确传入 yaml_case
    #             exec(_new_data, {}, {"yaml_case": self.__yaml_case})

    def navigate_to(self, target: Any, path: List[str]) -> Any:
        """
        递归导航到 target 对象或 dict 的嵌套字段：
        - 如果 target 有属性 name,用 getattr 访问；
        - 否则如果 target 是 dict,用 target[name] 访问；
        - 否则抛出 KeyError。
        """
        for name in path:
            if hasattr(target, name):
                target = getattr(target, name)
            elif isinstance(target, dict):
                target = target[name]
            else:
                raise KeyError(f"无法在 {target!r} 上访问键/属性 {name!r}")
        return target

    def get_dependent_data(self) -> None:
        _dependent_data = DependentCase(self.__yaml_case).is_dependent()
        if not _dependent_data:
            return

        for raw_key, new_value in _dependent_data.items():
            # 1) URL 替换
            if raw_key.startswith("$.url"):
                # 直接替换模型的 url 属性
                self.__yaml_case.url = new_value
                INFO.logger.info(f"已替换 URL → {new_value}")

            # 2) data 嵌套字段替换
            elif raw_key.startswith("$.data."):
                # 去掉 "$.data." 前缀
                nested = raw_key[len("$.data.") :]
                path_parts = nested.split(".")
                # 导航到 data 的父级对象（可能是模型属性或 dict）
                parent = self.navigate_to(self.__yaml_case, ["data"] + path_parts[:-1])
                last_attr = path_parts[-1]

                # 动态赋值
                if hasattr(parent, last_attr):
                    setattr(parent, last_attr, new_value)
                elif isinstance(parent, dict):
                    parent[last_attr] = new_value
                else:
                    raise TypeError(f"{parent!r} 不支持赋值字段 {last_attr!r}")
                INFO.logger.info(f"已替换 {raw_key} → {new_value}")
            else:
                INFO.logger.warning(f"未知的依赖 Key: {raw_key}")
            INFO.logger.info(f"替换后的用例数据: {self.__yaml_case}")
