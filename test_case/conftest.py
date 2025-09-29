import base64
import os
import pytest
import time
import allure
import requests
import ast
from io import BytesIO
from PIL import Image
import yaml
from common.setting import ensure_path_sep
from utils.request_tool.request_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.read_files_tool.clean_files import del_file
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler
from utils.captcha.vcode import fix_img, cut_img, train_model, rek_img
from utils import config
from utils.other_tools.rsa_encrypt import rsa_encrypt


INFO.logger.info("初始化conftest.py")


@pytest.fixture(scope="session", autouse=False)
def clear_report() -> None:
    """
    清理测试报告
    """

    del_file(ensure_path_sep("\\report"))


# app接口登录初始化，获取登录token
@pytest.fixture(scope="session", autouse=True)
def app_login_init():
    """
    登录初始化
    """
    INFO.logger.info("app接口登录初始化")
    # 获取host list
    host_url = "http://47.107.113.31:19800/api/hostList"
    headers = {
        "App-Source": "WObird",
        "Content-Language": "CN",
        "Authorization": "",
        "Platform": "apple",
    }
    response = requests.post(url=host_url, headers=headers)
    AL_HOST = response.json()["data"]["hostListVoList"][0]["host"]
    DEV_HOST = response.json()["data"]["hostListVoList"][1]["host"]
    CacheHandler.update_cache(cache_name="AL_HOST", value=AL_HOST)
    CacheHandler.update_cache(cache_name="DEV_HOST", value=DEV_HOST)
    CacheHandler.update_cache(cache_name="customId", value=config.customId)
    INFO.logger.info(f"AL_HOST: {AL_HOST}")
    INFO.logger.info(f"DEV_HOST: {DEV_HOST}")

    iot_url = f"{AL_HOST}/app/info/appUser/loginTest"
    para = {
        "email": "834532523@qq.com",
        "password": "w12345678",
        "customId": config.customId,
        "countryCode": "US",
        "loginConfirm": 1,
    }
    response_json = requests.post(url=iot_url, headers=headers, json=para)
    token = response_json.json()["data"]["token"]
    userId = response_json.json()["data"]["userInfo"]["userUid"]
    INFO.logger.info(f"登录响应: {response_json.json()}")
    CacheHandler.update_cache(cache_name="app_token", value=token)
    CacheHandler.update_cache(cache_name="userId", value=userId)


# iot接口登录初始化，获取登录token
@pytest.fixture(scope="session", autouse=True)
def work_login_init():
    """
    登录初始化
    """
    INFO.logger.info("iot登录初始化")
    code_url = "http://47.107.113.31:18090/prod-api/code"

    def get_code():
        model_dict = train_model(
            ensure_path_sep(r"\utils\captcha\vcode\cut_dir"), ["png"]
        )
        code = rek_img(
            model_dict, ensure_path_sep(r"\utils\captcha\vcode\test"), ["png"]
        )
        if "x" in code and len(code) > 2:
            return int(code[0]) * int(code[2])
        return eval(code[:3])

    response = requests.get(url=code_url)
    base64_data = response.json()["data"]["img"]
    uuid = response.json()["data"]["uuid"]
    image_data = base64.b64decode(base64_data)
    image_file = BytesIO(image_data)
    image = Image.open(image_file)
    image.save(ensure_path_sep(rf"\utils\captcha\vcode\test\code.png"))
    code = get_code()
    CacheHandler.update_cache(cache_name="code", value=code)
    CacheHandler.update_cache(cache_name="uuid", value=uuid)
    INFO.logger.info(f"验证码: {code}")
    INFO.logger.info(f"uuid: {uuid}")
    # 登录平台
    iot_url = "http://47.107.113.31:18090/prod-api/auth/login"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Language": "zh_CN",
        "App-Source": "WOcam",
        "Authorization": None,
    }
    json_data = {
        "username": "test02",
        "password": "admin@lzy123",
        "code": code,
        "uuid": uuid,
    }

    try:
        res = requests.post(headers=headers, json=json_data, url=iot_url)
        token = res.json()["data"]["access_token"]
        token = "Bearer " + token
        CacheHandler.update_cache(cache_name="token", value=token)
        INFO.logger.info(
            "缓存中的token:{}".format(CacheHandler.get_cache(cache_data="token"))
        )
    except Exception as e:
        ERROR.logger.error(f"获取token失败: {e}")
        raise e


def pytest_collection_modifyitems(items):
    """根据 case_order.yaml 对模块和用例进行排序"""

    # 1. 读取配置
    order_config_path = ensure_path_sep("common/case_order.yaml")
    with open(order_config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    strict_mode = config.get("strict", False)
    modules_config = config.get("modules", [])

    # 2. 收集测试用例 -> 按模块分组
    module_map = {}
    for item in items:
        module_path = os.path.normpath(item.fspath.relto(os.getcwd()))
        module_dir = os.path.dirname(module_path).replace("test_case" + os.sep, "")
        module_name = module_dir.replace(os.sep, "/")
        module_map.setdefault(module_name, []).append(item)

    sorted_items = []
    collected_modules = set(module_map.keys())
    print(collected_modules)
    # 3. 按配置顺序排序模块
    for module in modules_config:
        name = module["name"]
        enabled = module.get("enabled", True)
        appoint_items = module.get("cases", [])

        if name not in module_map:
            msg = f"[排序警告] 配置中的模块 {name} 未找到"
            if strict_mode:
                pytest.exit(msg)
            else:
                INFO.logger.warning(msg)
                continue

        if not enabled:
            INFO.logger.info(f"[跳过模块] {name}")
            continue

        # 4. 模块内排序
        order_map = {case: idx for idx, case in enumerate(appoint_items)}
        module_cases = module_map[name]
        module_cases.sort(key=lambda x: order_map.get(x.name.split("[")[0], 9999))

        # 检查配置缺失
        collected_names = [x.name.split("[")[0] for x in module_cases]
        missing_cases = [c for c in appoint_items if c not in collected_names]
        if missing_cases:
            msg = f"[排序警告] 模块 {name} 配置的用例未收集到: {missing_cases}"
            if strict_mode:
                pytest.exit(msg)
            else:
                INFO.logger.warning(msg)

        sorted_items.extend(module_cases)
        collected_modules.discard(name)

    # 5. 剩余未配置的模块（保持原有顺序）
    # for mod_name in list(collected_modules):
    #     sorted_items.extend(module_map[mod_name])

    # 6. 更新 pytest 的执行顺序
    items[:] = sorted_items

    # 7. 输出最终顺序
    INFO.logger.info("\n[执行顺序]")
    for idx, item in enumerate(items, 1):
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        INFO.logger.info(f"{idx}. {item.nodeid}")


@pytest.fixture(scope="function", autouse=True)
def case_skip(in_data):
    """处理跳过用例"""
    in_data = TestCase(**in_data)
    if ast.literal_eval(cache_regular(str(in_data.is_run))) is False:
        allure.dynamic.title(in_data.detail)
        allure_step_no(f"请求URL: {in_data.is_run}")
        allure_step_no(f"请求方式: {in_data.method}")
        allure_step("请求头: ", in_data.headers)
        allure_step("请求数据: ", in_data.data)
        allure_step("依赖数据: ", in_data.dependence_case_data)
        allure_step("预期数据: ", in_data.assert_data)
        pytest.skip()


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """

    _PASSED = len(
        [i for i in terminalreporter.stats.get("passed", []) if i.when != "teardown"]
    )
    _ERROR = len(
        [i for i in terminalreporter.stats.get("error", []) if i.when != "teardown"]
    )
    _FAILED = len(
        [i for i in terminalreporter.stats.get("failed", []) if i.when != "teardown"]
    )
    _SKIPPED = len(
        [i for i in terminalreporter.stats.get("skipped", []) if i.when != "teardown"]
    )
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime

    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")
