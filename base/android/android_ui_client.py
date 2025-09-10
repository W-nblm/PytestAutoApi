import ast
from common.setting import ensure_path_sep
from utils.cache_process.cache_control import CacheHandler
from utils.read_files_tool.yaml_control import GetYamlData
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from appium import webdriver
import os
from common.appium import appOperator


class Android_UI_Client(object):
    __instance = None
    __inited = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, is_reset_app=False, is_kill_app=False):
        if self.__inited is None:
            self.__inited = True
            self.__is_first = True

            # 获取设备信息
            self.device_info = self.get_device_info()
            self.current_desired_caps = self.device_info.get(
                "current_desired_capabilities"
            )
            self.fullReset = self.device_info.get("fullReset", False)
            self.noReset = self.device_info.get("noReset", False)
            self.appium_hub = (
                self.device_info["server_url"]
                + ":"
                + self.device_info["server_port"]
                + self.device_info["server_path"]
            )

            # 初始化设备信息
            self._init()

            # 启动设备
            self.driver = webdriver.Remote(
                self.appium_hub,
                self.current_desired_caps,
            )

            # 判断是否需要重置app
            if is_reset_app:
                self.driver.reset()

            self.appOperator = appOperator(self.driver, self.appium_hub)

    def get_device_info(self) -> dict:
        # 获取设备配置信息
        return CacheHandler.get_cache(cache_data="device" + str(os.getpid()))

    def _init(self):
        # 初始化设备的基础数据
        INFO.logger.info("初始化设备的基础数据")

        INFO.logger.info("初始化设备的基础数据完成")
