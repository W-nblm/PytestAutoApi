from time import sleep
import allure
import pytest
from common.setting import ensure_path_sep
from page_objects.app_ui.android.pages.login_page import LoginPage
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.ocr import OCRProcessor
from utils.read_files_tool.yaml_control import GetYamlData


class TestLogin:
    case_data = GetYamlData(
        ensure_path_sep("/test_data/app_ui/login_page.yaml")
    ).get_yaml_data()

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, app):
        self.ocr = OCRProcessor()
        self.lg = LoginPage(app.driver, app.appium_hub)

    @pytest.mark.skip(reason="跳过测试")
    @allure.feature("登录模块")
    @allure.title("登录测试用例")
    @pytest.mark.parametrize("case", case_data["login_cases"])
    def test_login(self, case):
        """
        登录测试用例,
        """
        INFO.logger.info(case)

        # 勾选隐私协议
        self.lg.select_agreement()

        # 输入账号密码
        self.lg.enter_username(case["username"])
        self.lg.enter_password(case["password"])

        # 登陆
        self.lg.click_login()

        # 断言
        if case["expected"] == "登录成功":
            assert self.lg.login_success() == True, "登录失败"

        else:
            sleep(0.5)
            self.lg.save_screenshot(ensure_path_sep("test_pictures/login_success.png"))
            result_text = self.ocr.recognize_text(
                image_path=ensure_path_sep("test_pictures/login_success.png"),
                roi=(500, 1300, 950, 1700),
            )
            assert case["expected"] in result_text, "测试失败"
        self.lg.driver.reset()

    @pytest.mark.skip(reason="跳过测试")
    @allure.feature("登录模块")
    @allure.title("未勾选隐私协议")
    @pytest.mark.parametrize(
        "case",
        case_data["login_without_agreement"],
    )
    def test_login_without_agreement(self, case):
        """
        未勾选隐私协议
        """
        INFO.logger.info(case)

        # 输入账号密码
        self.lg.enter_username(case["username"])
        self.lg.enter_password(case["password"])

        # 登陆
        self.lg.click_login()

        # 断言
        sleep(0.5)
        self.lg.save_screenshot("test_pictures/login_success.png")
        result_text = self.ocr.recognize_text(
            image_path="test_pictures/login_success.png", roi=(0, 200, 0, 0)
        )
        assert case["expected"] in result_text, "测试失败"

        # 重置app
        self.lg.driver.reset()

    @allure.feature("登录模块")
    @allure.title("选择不同区域登录")
    @pytest.mark.parametrize(
        "case",
        case_data["login_area_cases"],
    )
    def test_login_with_area(self, case):
        """
        选择不同区域登录
        """
        INFO.logger.info(case)

        # 选择不同区域
        self.lg.click_location()
        self.lg.select_area(case["area"])

        # 输入账号密码
        self.lg.enter_username(case["username"])
        self.lg.enter_password(case["password"])

        # 勾选隐私协议
        self.lg.select_agreement()

        # 登陆
        self.lg.click_login()

        # 断言
        assert self.lg.login_success() == True, "登录失败"

        # 重置app
        self.lg.driver.reset()

    @allure.feature("登录模块")
    @allure.title("忘记密码")
    @pytest.mark.parametrize(
        "case",
        case_data["login_area_cases"],
    )
    def test_forget_password(self, case):
        """
        忘记密码
        """
        INFO.logger.info(case)

        # 点击忘记密码
        self.lg.click_forget_password()
