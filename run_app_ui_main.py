import os
import pytest
from common.setting import ensure_path_sep
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.times_tools.time_control import TimeControl
import requests
from utils.cache_process.cache_control import CacheHandler
from utils.read_files_tool.yaml_control import GetYamlData


def pytest_main(pytest_execute_params):
    exit_code = pytest.main(pytest_execute_params)


def start_app_device(device_info):

    INFO.logger.info(
        f"{TimeControl.get_current_time()} 开始检测appium server是否启动成功"
    )

    # 检测appium server是否启动成功
    try:
        response = requests.get(
            device_info["server_url"]
            + ":"
            + device_info["server_port"]
            + device_info["server_path"]
            + "/status"
        )
        if response.status_code == 200 and response.json()["status"] == 0:
            INFO.logger.info(f"{TimeControl.get_current_time()} appium server连接成功")
        else:
            INFO.logger.error(f"{TimeControl.get_current_time()} appium server连接失败")
    except:
        INFO.logger.error(f"{TimeControl.get_current_time()} appium server连接失败")
        raise Exception(f"{TimeControl.get_current_time()} appium server连接失败")

    # 缓存设备信息
    device_desired_caps = device_info["desired_caps"]
    CacheHandler.update_cache(
        cache_name="device" + str(os.getpid()), value=device_desired_caps
    )
    INFO.logger.info(
        f"{TimeControl.get_current_time()} 缓存设备信息成功\n{device_desired_caps}"
    )
    INFO.logger.info(f"{TimeControl.get_current_time()} 开始启动app")

    pytest_execute_params = [
        "-v",
        "--alluredir",
        "output/app_ui/%s/report_data/" % (device_desired_caps["deviceName"]),
    ]
    pytest_main(pytest_execute_params)


if __name__ == "__main__":

    device_info = GetYamlData(
        ensure_path_sep("config/app_ui_android_devices_info.yaml")
    ).get_yaml_data()
    print(device_info)
    start_app_device(device_info=device_info["devices_info"][0])
