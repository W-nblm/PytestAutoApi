from time import sleep
from typing import Literal
from selenium.common.exceptions import TimeoutException
from basepage.base import BasePages
from page_objects.app_ui.android.elements.login_wobird import LoginWobirdElements as le
from page_objects.app_ui.android.elements.login_wobird import HomeWobirdElements as he
from page_objects.app_ui.android.elements.login_wobird import UserInfoElements as ue
from page_objects.app_ui.android.elements.login_wobird import AreaSelectElements as ae
from page_objects.app_ui.android.elements.login_wobird import ForgotPasswordElements as fe


class LoginPage(BasePages):
    """
    登录界面
    """

    def select_agreement(self):
        # 选择协议
        if self.is_checked(*le.AGREEMENT):
            pass
        else:
            self.click(*le.AGREEMENT)

    def enter_username(self, username):
        # 清空账号输入框、输入账号
        self.clear(*le.ACCOUNT)
        self.input(*le.ACCOUNT, value=username)

    def enter_password(self, password):
        # 清空密码输入框、输入密码
        self.clear(*le.PASSWORD)
        # 输入密码
        self.input(*le.PASSWORD, value=password)

    def click_login(self):
        # 登陆
        self.click(*le.LOGIN_BUTTON)

    def click_forget_password(self):
        # 点击忘记密码
        self.click(*le.FORGET_PASSWORD)

    def get_toast_message(self):
        # 获取toast消息
        # return self.get_toast_text(*le.TOAST)
        return self.get_toast_via_uiautomator("错误")

    def click_register(self):
        # 点击注册
        self.click(*le.REGISTER)

    def logout(self):
        # 退出登录
        self.click(*he.MY_BUTTON)
        # 点击用户信息
        self.click(*ue.USER_INFO_BUTTON)
        # 点击退出登录
        self.click(*ue.LOGOUT_BUTTON)
        # 点击确认
        self.click(*ue.CONFIRM_BUTTON)

    def login_success(self):
        # 登录成功
        if self.element_is_present(*he.MY_BUTTON):
            return True
        else:
            return False

    def click_location(self):
        # 点击切换区域
        self.click(*le.ACCOUNT_AREA)

    def get_area_title(self):
        # 获取区域标题
        return self.get_title(*ae.SELECT_AREA_TITLE)

    def select_area(self, area, method: Literal["swipe", "search"] = "swipe"):
        # 选择区域
        name, text = ae.AREA
        text = text.replace("区域", area)
        if method == "swipe":
            self.swipe_to_find_element(name, text, swipe_duration=1200).click()
        elif method == "search":
            self.input(*ae.SEARCH_INPUT, value=area)
            self.click(name, text)

    def change_forget_password_area(self, area, method: Literal["swipe", "search"] = "swipe"):
        # 切换忘记密码区域
        self.click(*fe.AREA_SELECT_BUTTON)
        # 选择区域
        name, text = ae.AREA
        text = text.replace("区域", area)
        if method == "swipe":
            self.swipe_to_find_element(name, text, swipe_duration=1200).click()
        elif method == "search":
            self.input(*ae.SEARCH_INPUT, value=area)
            self.click(name, text)
    
    def input_forget_password_account(self, account):
        # 输入忘记密码账号
        self.input(*fe.ACCOUNT_INPUT, value=account)

    def click_forget_password_send_code(self):
        # 点击发送验证码
        self.click(*fe.SEND_CODE_BUTTON)

    def input_forget_password_code(self, code):
        # 输入验证码
        for i in code:
            self.press_keycode(i)