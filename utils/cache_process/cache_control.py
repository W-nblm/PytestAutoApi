import os
from typing import Any, Text, Union
from common.setting import ensure_path_sep
from utils.other_tools.exceptions import ValueNotFoundError


class Cache:
    """设置、读取缓存"""

    def __init__(self, filename: Union[Text, None]) -> None:
        # 如果filename不为空，则操作指定文件内容
        if filename:
            self.path = ensure_path_sep("\\cache" + filename)
        # 如果filename为None，则操作所有文件内容
        else:
            self.path = ensure_path_sep("\\cache")

    def set_cache(self, key: Text, value: Any) -> None:
        """设置缓存"""
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(str({key: value}))

    def set_caches(self, value: Any) -> None:
        """设置多个缓存
        :param value: 缓存内容
        :return: None
        """
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(str(value))

    def get_cache(self) -> Any:
        """获取缓存
        :return: 缓存内容
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            pass

    def clean_cache(self) -> None:
        """清除缓存"""
        if not os.path.exists(self.path):
            raise FileNotFoundError("缓存文件不存在")
        os.remove(self.path)

    @staticmethod
    def clean_all_cache(cls) -> None:
        """清除所有缓存文件
        :return: None
        """
        cache_path = ensure_path_sep("\\cache")

        list_dir = os.listdir(cache_path)
        for file_name in list_dir:
            os.remove(cache_path + file_name)


_cache_config = {}


class CacheHandler:
    @staticmethod
    def get_cache(cache_data):
        try:
            return _cache_config[cache_data]
        except KeyError:
            raise ValueNotFoundError("缓存不存在")

    @staticmethod
    def update_cache(*, cache_name, value):
        _cache_config[cache_name] = value
