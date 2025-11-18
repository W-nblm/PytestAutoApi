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


def get_all_files(file_path, yaml_data_switch=False) -> list:
    """
    获取文件路径
    :param file_path: 目录路径
    :param yaml_data_switch: 是否过滤文件为 yaml格式， True则过滤
    :return:
    """
    filename = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(file_path):
        print(root)
        for _file_path in files:
            path = os.path.join(root, _file_path)
            print("path:", path)
            if yaml_data_switch:
                if "yaml" in path or ".yml" in path:
                    filename.append(path)
            else:
                filename.append(path)
    return filename


if __name__ == "__main__":
    print(ensure_path_sep("\\common\\config.yaml"))
