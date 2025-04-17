import logging
from logging import handlers
from typing import Text
import time
import colorlog
from common.setting import ensure_path_sep


class LogHandler:
    """日志封装"""

    # 日志级别
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(
        self,
        filename: Text,
        level: Text = "info",
        when: Text = "D",
        fmt: Text = "%(levelname)-8s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s",
    ):
        self.logger = logging.getLogger(filename)
        formatter = self.log_color()
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 屏幕输出
        screen_output = logging.StreamHandler()
        screen_output.setFormatter(formatter)
        # 向文件写入#指定间隔时间自动生成文件的处理器
        file_output = handlers.TimedRotatingFileHandler(
            filename=filename, when=when, backupCount=3, encoding="utf-8"
        )
        # 设置写入文件格式
        file_output.setFormatter(format_str)
        # 添加对象到日志对象中
        self.logger.addHandler(screen_output)
        self.logger.addHandler(file_output)
        self.log_path = ensure_path_sep("\\logs\\log.log")

    @classmethod
    def log_color(cls):
        """日志格式化"""
        log_colors_config = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        }

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
            log_colors=log_colors_config,
        )
        return formatter


now_time_day = time.strftime("%Y-%m-%d", time.localtime())
INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day}.log"), level="info")
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day}.log"), level="error")
WARNING = LogHandler(ensure_path_sep(f"\\logs\\warning-{now_time_day}.log"))

if __name__ == "__main__":
    ERROR.logger.error("测试")
