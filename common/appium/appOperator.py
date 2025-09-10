from appium.webdriver.webdriver import WebDriver
from datetime import datetime
import os
from time import sleep
import allure
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.action_chains import ActionChains

import random
import string
from utils.logging_tool.log_control import INFO, ERROR, WARNING


class AppOperator:

    def __init__(self, driver: WebDriver, appium_hub):
        # self.__data = load_yaml("data/defaultData.yaml")  # 打开指定的应用
        # self.__options = AppiumOptions()
        # self.__options.load_capabilities(self.__data["lzy_caps"])  # 读取配置文件
        # self.driver = webdriver.Remote(self.__data["url"], options=self.__options)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=0.2)
        self.ROOT_DIR = ""
        self.__get_root_dir()

    def __get_root_dir(self):

        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def locator(self, name, text):
        """
        显示等待定位
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 定位到的元素
        """
        INFO.logger.info("name %s, text %s", name, text)
        mapping = {
            "predicate": MobileBy.IOS_PREDICATE,
            "chain": MobileBy.IOS_CLASS_CHAIN,
            "uiautomator": MobileBy.ANDROID_UIAUTOMATOR,
            "accessibility_id": MobileBy.ACCESSIBILITY_ID,
            "xpath": MobileBy.XPATH,
            "id": MobileBy.ID,
            "name": MobileBy.NAME,
            "class_name": MobileBy.CLASS_NAME,
            "tag_name": MobileBy.TAG_NAME,
            "link_text": MobileBy.LINK_TEXT,
            "partial_link_text": MobileBy.PARTIAL_LINK_TEXT,
            "css_selector": MobileBy.CSS_SELECTOR,
        }
        name = mapping.get(name, name)

        element = self.wait.until(ec.visibility_of_element_located((name, text)))
        sleep(0.5)
        INFO.logger.info(f"查到的元素：{element}")
        return element

    def locator_elements(self, name, text):
        """
        重复元素定位
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 定位到的元素
        """
        INFO.logger.info("name %s, text %s", name, text)
        mapping = {
            "predicate": MobileBy.IOS_PREDICATE,
            "chain": MobileBy.IOS_CLASS_CHAIN,
        }
        name = mapping.get(name, name)

        elements = self.wait.until(ec.presence_of_all_elements_located((name, text)))
        sleep(0.5)
        INFO.logger.info(f"查到的元素：{elements}")
        return elements

    def elements_click(self, name, text, index):
        """
        点击元素
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :param index: 元素索引
        :return: 无
        """
        WebElements = self.locator_elements(name, text)
        if len(WebElements) == 0:
            INFO.logger.info("未定位到元素")
            return 0
        elif index >= len(WebElements):
            print("下标超出元素的个数,元素个数为:{}".format(len(WebElements)))
        else:
            INFO.logger.info(f"查到的元素：{WebElements[index]}")
            WebElements[index].click()
            INFO.logger.info(f"点击元素：{name},{text},{index}")

    def get_toast_text(self, name, text):
        """
        获取Toast内容,通过提升检查元素更新速度poll_frequency=0.1
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: Toast文本内容
        """
        toast = WebDriverWait(
            self.driver, timeout=5, poll_frequency=0.1  # 每0.1秒检查一次
        ).until(ec.presence_of_element_located((name, text)))
        return toast.text

    def get_toast_via_uiautomator(self, message):
        """
        通过UIAutomator2文本匹配
        """
        command = f'new UiSelector().textContains("{message}")'
        return self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, command).text

    def input(self, name, text, value):
        """
        输入框里面输入内容
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :param value: 要输入的内容
        :return: 无
        """
        self.locator(name, text).send_keys(value)

    def clear(self, name, text):
        """
        清空输入框里面的内容
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 无
        """
        self.locator(name, text).clear()

    def click(self, name, text):
        """
        点击当前元素
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 无
        """

        self.locator(name, text).click()
        INFO.logger.info(f"点击元素：{name},{text}")

    def get_title(self, name, text):
        """
        获取当前页面标题
        :return: 页面标题
        """
        return self.locator(name, text).text

    def is_checked(self, name, text):
        """
        检查复选框或开关是否被勾选
        :param name: 定位方式 (id, xpath 等)
        :param text: 元素名称或者路径
        :return: True(已勾选),False(未勾选)
        """
        element = self.locator(name, text)

        checked_status = element.get_attribute("checked")
        INFO.logger.info(f"元素是否被勾选checked属性：{checked_status}")
        return checked_status in ["true", "1"]

    def get_location(self, name, text, index=None):
        """
        点击当前元素
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 元素坐标字典：x,y
        """
        if index == None:
            return self.locator(name, text).location
        else:
            WebElements = self.locator_elements(name, text)
            if len(WebElements) == 0:
                INFO.logger.info("未找到元素")
                return 0
            else:
                return WebElements[index].location

    def element_is_present(self, name, text, index=None):
        """
        判断元素是否存在
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 元素是否存在
        """
        if index == None:
            return self.wait.until(ec.presence_of_element_located((name, text)))
        else:
            WebElements = self.wait.until(
                ec.presence_of_all_elements_located((name, text))
            )
            if len(WebElements) == 0:
                INFO.logger.info("未找到元素")
                return 0
            else:
                return WebElements[index]

    def element_size(self, name, text, index=None):
        """
        点击当前元素
        :param name: 定位方式ID、xpath...
        :param text: 元素名称或者路径
        :return: 元素大小：width,hidgth
        """
        if index == None:
            return self.locator(name, text).size
        else:
            WebElements = self.locator_elements(name, text)
            if len(WebElements) == 0:
                INFO.logger.info("未找到元素")
                return 0
            else:
                return WebElements[index].size

    def action_click(self, name, text, index=None):
        """
        手势点击
        """
        if index == None:
            on_element = self.locator(name=name, text=text)
        else:
            on_element = self.locator_elements(name=name, text=text)[index]
        action = ActionChains(self.driver)
        action.click(on_element).perform()

    def swipe(self, start_x, start_y, end_x, end_y, duration=250):
        """
        滑动
        :param start_x: 起始坐标x
        :param start_y: 起始坐标y
        :param end_x: 终止坐标x
        :param end_y: 终止坐标y
        :param duration: 持续时间
        :return: 无
        """
        action = ActionChains(self.driver, duration=duration)
        action.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        action.w3c_actions.pointer_action.pointer_down()
        action.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        action.w3c_actions.pointer_action.pointer_up()
        action.perform()

    def swipe_to_find_element(
        self, name, text, max_swipes: int = 5, swipe_duration: int = 1000
    ):
        """
        滑动屏幕以查找元素。

        :param locator: 元素定位器，例如 (MobileBy.XPATH, "//*[contains(@text,'目标元素文本')]")
        :param max_swipes: 最大滑动次数，默认值为 5
        :param swipe_duration: 每次滑动的持续时间（毫秒），默认值为 1000
        :return: 找到的元素对象；如果未找到，则返回 None
        """
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]

        start_x = width * 0.5
        start_y = height * 0.6
        end_x = width * 0.5
        end_y = height * 0.3

        for _ in range(max_swipes):
            try:
                element = self.locator(name, text)
                return element
            except (NoSuchElementException, TimeoutException):
                self.driver.swipe(
                    start_x, start_y, end_x, end_y, duration=swipe_duration
                )
        return None

    def save_screenshot(self, name: str) -> None:
        """
        截取当前屏幕
        :param name: str 截图名称,格式为"temp.png"
        :return: None
        """
        if not name.endswith(".png"):
            raise ValueError('文件名必须以".png"结尾')

        self.driver.save_screenshot(name)

    def toast_exist(self, toast_message, img_doc):
        """
        获取Toast内容并截图
        :param img_doc: 截图说明
        :param toast_message: Toast文本内容或者部分内容
        :return:
        """
        # Toast元素
        toast_loc = ("xpath", f"//*[contains(@text,'{toast_message}')]")
        try:
            res = WebDriverWait(self.driver, 3, 0.3).until(
                ec.presence_of_element_located(toast_loc)
            )
            self.add_screenshot_to_allure(img_doc)
            print(f"Toast提示：{res.text}")
        except TimeoutException as e:
            print(f"{e}_获取元素超时")
        except StaleElementReferenceException as e:
            print(f"{e}_获取toast失败")

    def add_screenshot_to_allure(self, img_name):
        """
        截图添加到allure中
        :param img_doc: 截图说明
        :return:
        """
        file_name = rf'{self.ROOT_DIR}\test_picture\{datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")}_{img_name}.png'
        INFO.logger.info(f"截图文件名：{file_name}")
        self.save_screenshot(file_name)
        sleep(0.5)
        with open(file_name, mode="rb") as f:
            file = f.read()
        allure.attach(file, img_name, allure.attachment_type.PNG)

    def generate_random_string(self, length):
        # 使用 string.printable 包含所有可打印字符(包括中文)
        characters = string.ascii_letters + string.digits + string.printable

        # 使用 random.choices() 从字符集中随机选择字符,并构建字符串
        random_string = "".join(random.choice(characters) for _ in range(length))

        return random_string

    def tips(self, text):
        INFO.logger.info(f"------{text}------")

    def getMobileKey(self):
        key = {
            "0": 7,
            "1": 8,
            "2": 9,
            "3": 10,
            "4": 11,
            "5": 12,
            "6": 13,
            "7": 14,
            "8": 15,
            "9": 16,
            "A": 29,
            "B": 30,
            "C": 31,
            "D": 32,
            "E": 33,
            "F": 34,
            "G": 35,
            "H": 36,
            "I": 37,
            "J": 38,
            "K": 39,
            "L": 40,
            "M": 41,
            "N": 42,
            "O": 43,
            "P": 44,
            "Q": 45,
            "R": 46,
            "S": 47,
            "T": 48,
            "U": 49,
            "V": 50,
            "W": 51,
            "X": 52,
            "Y": 53,
            "Z": 54,
            "a": 29,
            "b": 30,
            "c": 31,
            "d": 32,
            "e": 33,
            "f": 34,
            "g": 35,
            "h": 36,
            "i": 37,
            "j": 38,
            "k": 39,
            "l": 40,
            "m": 41,
            "n": 42,
            "o": 43,
            "p": 44,
            "q": 45,
            "r": 46,
            "s": 47,
            "t": 48,
            "u": 49,
            "v": 50,
            "w": 51,
            "x": 52,
            "y": 53,
            "z": 54,
            "META_ALT_LEFT_ON": 16,
            "META_ALT_MASK": 50,
            "META_ALT_ON": 2,
            "META_ALT_RIGHT_ON": 32,
            "META_CAPS_LOCK_ON": 1048576,
            "META_CTRL_LEFT_ON": 8192,
            "META_CTRL_MASK": 28672,
            "META_CTRL_ON": 4096,
            "META_CTRL_RIGHT_ON": 16384,
            "META_FUNCTION_ON": 8,
            "META_META_LEFT_ON": 131072,
            "META_META_MASK": 458752,
            "META_META_ON": 65536,
            "META_META_RIGHT_ON": 262144,
            "META_NUM_LOCK_ON": 2097152,
            "META_SCROLL_LOCK_ON": 4194304,
            "META_SHIFT_LEFT_ON": 64,
            "META_SHIFT_MASK": 193,
            "META_SHIFT_ON": 1,
            "META_SHIFT_RIGHT_ON": 128,
            "META_SYM_ON": 4,
            "KEYCODE_APOSTROPHE": 75,
            "KEYCODE_AT": 77,
            "KEYCODE_BACKSLASH": 73,
            "KEYCODE_COMMA": 55,
            "KEYCODE_EQUALS": 70,
            "KEYCODE_GRAVE": 68,
            "KEYCODE_LEFT_BRACKET": 71,
            "KEYCODE_MINUS": 69,
            "KEYCODE_PERIOD": 56,
            "KEYCODE_PLUS": 81,
            "KEYCODE_POUND": 18,
            "KEYCODE_RIGHT_BRACKET": 72,
            "KEYCODE_SEMICOLON": 74,
            "KEYCODE_SLASH": 76,
            "KEYCODE_STAR": 17,
            "KEYCODE_SPACE": 62,
            "KEYCODE_TAB": 61,
            "KEYCODE_ENTER": 66,
            "KEYCODE_ESCAPE": 111,
            "KEYCODE_CAPS_LOCK": 115,
            "KEYCODE_CLEAR": 28,
            "KEYCODE_PAGE_DOWN": 93,
            "KEYCODE_PAGE_UP": 92,
            "KEYCODE_SCROLL_LOCK": 116,
            "KEYCODE_MOVE_END": 123,
            "KEYCODE_MOVE_HOME": 122,
            "KEYCODE_INSERT": 124,
            "KEYCODE_SHIFT_LEFT": 59,
            "KEYCODE_SHIFT_RIGHT": 60,
            "KEYCODE_F1": 131,
            "KEYCODE_F2": 132,
            "KEYCODE_F3": 133,
            "KEYCODE_F4": 134,
            "KEYCODE_F5": 135,
            "KEYCODE_F6": 136,
            "KEYCODE_F7": 137,
            "KEYCODE_F8": 138,
            "KEYCODE_F9": 139,
            "KEYCODE_F10": 140,
            "KEYCODE_F11": 141,
            "KEYCODE_F12": 142,
            "KEYCODE_BACK": 4,
            "KEYCODE_CALL": 5,
            "KEYCODE_ENDCALL": 6,
            "KEYCODE_CAMERA": 27,
            "KEYCODE_FOCUS": 80,
            "KEYCODE_VOLUME_UP": 24,
            "KEYCODE_VOLUME_DOWN": 25,
            "KEYCODE_VOLUME_MUTE": 164,
            "KEYCODE_MENU": 82,
            "KEYCODE_HOME": 3,
            "KEYCODE_POWER": 26,
            "KEYCODE_SEARCH": 84,
            "KEYCODE_NOTIFICATION": 83,
            "KEYCODE_NUM": 78,
            "KEYCODE_SYM": 63,
            "KEYCODE_SETTINGS": 176,
            "KEYCODE_DEL": 67,
            "KEYCODE_FORWARD_DEL": 112,
            "KEYCODE_NUMPAD_0": 144,
            "KEYCODE_NUMPAD_1": 145,
            "KEYCODE_NUMPAD_2": 146,
            "KEYCODE_NUMPAD_3": 147,
            "KEYCODE_NUMPAD_4": 148,
            "KEYCODE_NUMPAD_5": 149,
            "KEYCODE_NUMPAD_6": 150,
            "KEYCODE_NUMPAD_7": 151,
            "KEYCODE_NUMPAD_8": 152,
            "KEYCODE_NUMPAD_9": 153,
            "KEYCODE_NUMPAD_ADD": 157,
            "KEYCODE_NUMPAD_COMMA": 159,
            "KEYCODE_NUMPAD_DIVIDE": 154,
            "KEYCODE_NUMPAD_DOT": 158,
            "KEYCODE_NUMPAD_EQUALS": 161,
            "KEYCODE_NUMPAD_LEFT_PAREN": 162,
            "KEYCODE_NUMPAD_MULTIPLY": 155,
            "KEYCODE_NUMPAD_RIGHT_PAREN": 163,
            "KEYCODE_NUMPAD_SUBTRACT": 156,
            "KEYCODE_NUMPAD_ENTER": 160,
            "KEYCODE_NUM_LOCK": 143,
            "KEYCODE_MEDIA_FAST_FORWARD": 90,
            "KEYCODE_MEDIA_NEXT": 87,
            "KEYCODE_MEDIA_PAUSE": 127,
            "KEYCODE_MEDIA_PLAY": 126,
            "KEYCODE_MEDIA_PLAY_PAUSE": 85,
            "KEYCODE_MEDIA_PREVIOUS": 88,
            "KEYCODE_MEDIA_RECORD": 130,
            "KEYCODE_MEDIA_REWIND": 89,
            "KEYCODE_MEDIA_STOP": 86,
        }
        return key

    def press_keycode(self, keycode):
        code = self.getMobileKey()
        # re_code = {v: k for k, v in code.items()}
        key = code.get(keycode)
        print(key)
        self.driver.press_keycode(key)
