import base64
import pytest
import time
import allure
import requests
import ast
from io import BytesIO
from PIL import Image
from common.setting import ensure_path_sep
from utils.request_tool.request_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.read_files_tool.clean_files import del_file
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler
from utils.captcha.vcode import fix_img, cut_img, train_model, rek_img


INFO.logger.info("初始化conftest.py")


@pytest.fixture(scope="session", autouse=False)
def clear_report() -> None:
    """
    清理测试报告
    """

    del_file(ensure_path_sep("\\report"))


@pytest.fixture(scope="session", autouse=True)
def work_login_init():
    """
    登录初始化
    """
    INFO.logger.info("登录初始化")
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
    """测试用例收集完成后,将item的name和node_id显示到控制台"""
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    # 期望用例顺序


    appoint_items = [
        "test_upload_img",
    ]

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)
    INFO.logger.info(f"指定运行顺序: {run_items}")
    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]
    INFO.logger.info(f"运行顺序: {items}")


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
