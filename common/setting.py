# import os
# from typing import Text


# def root_path():
#     """获取项目根目录路径"""
#     return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# def ensure_path_sep(path: Text) -> Text:
#     """兼容windows和linux的路径分隔符"""
#     if "/" in path:
#         path = os.sep.join(path.split("/"))
#     elif "\\" in path:
#         path = os.sep.join(path.split("\\"))
#     return root_path() + path
import os
from typing import Text


def root_path() -> Text:
    """获取项目根目录路径"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ensure_path_sep(path: Text) -> Text:
    """
    兼容 Windows 和 Linux 的路径分隔符，并返回绝对路径
    """
    # 将所有分隔符统一替换为当前系统的分隔符
    path = path.replace("\\", os.sep).replace("/", os.sep)

    # 去掉开头多余的分隔符，避免 join 出错
    path = path.lstrip(os.sep)

    # 拼接路径
    full_path = os.path.join(root_path(), path)

    # 规范化路径分隔符
    return os.path.normpath(full_path)


if __name__ == "__main__":
    print(ensure_path_sep("\\common\\config.yaml"))
