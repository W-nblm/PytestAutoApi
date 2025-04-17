import os
from typing import Text


def root_path():
    """获取项目根目录路径"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ensure_path_sep(path: Text) -> Text:
    """兼容windows和linux的路径分隔符"""
    if "/" in path:
        path = os.sep.join(path.split("/"))
    elif "\\" in path:
        path = os.sep.join(path.split("\\"))
    return root_path() + path
