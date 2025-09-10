class LoginWobirdElements:
    # 登录页面元素
    ACCOUNT_AREA = ("id", "com.lzy.wobird:id/tv_region")
    ACCOUNT = ("xpath", '//*[@class="android.widget.EditText"][1]')
    PASSWORD = ("xpath", '//*[@class="android.widget.EditText"][2]')
    LOGIN_BUTTON = ("id", "com.lzy.wobird:id/btn_sign_in")
    FORGET_PASSWORD = ("id", "com.lzy.wobird:id/tv_forgot")
    REGISTER = ("id", "com.lzy.wobird:id/tv_sign_up")
    AGREEMENT = ("id", "com.lzy.wobird:id/cb_agree")
    NOT_AGREE = ("id", "com.lzy.wobird:id/tv")
    TOAST = ("xpath", '//*[@class="android.widget.Toast"]')


class HomeWobirdElements:
    # 首页页面元素
    HOME_BUTTON = ("xpath", '//android.widget.TextView[@text="首页"]')
    COLLECT_BUTTON = ("xpath", '//android.widget.TextView[@text="收藏"]')
    DEVICE_BUTTON = ("xpath", '//android.widget.TextView[@text="设备"]')
    MY_BUTTON = ("xpath", '//android.widget.TextView[@text="我的"]')


class UserInfoElements:
    # 用户信息页面元素
    USER_INFO_BUTTON = ("id", "com.lzy.wobird:id/layout_user_info")
    USER_NAME = ("id", "com.lzy.wobird:id/tv_name")
    LOGOUT_BUTTON = ("id", "com.lzy.wobird:id/root")
    CONFIRM_BUTTON = ("id", "com.lzy.wobird:id/btn_confirm")
    CANCEL_BUTTON = ("id", "com.lzy.wobird:id/btn_cancel")


class AreaSelectElements:
    # 地区选择页面元素
    CITY_LIST = ("id", "com.lzy.wobird:id/tv_region")
    # 搜索框
    SEARCH_INPUT = ("id", "com.lzy.wobird:id/customEditText2")
    # 搜索按钮

    # 区域,多元素
    AREA = (
        "xpath",
        '//android.widget.TextView[@resource-id="com.lzy.wobird:id/tv_region" and @text="区域"]',
    )

    # 选择区域title
    SELECT_AREA_TITLE = (
        "id",
        "com.lzy.wobird:id/title",
    )


class ForgotPasswordElements:

    # 忘记密码页面元素
    # 忘记密码页面title
    FORGET_PASSWORD_TITLE = ("xpath", '//android.widget.TextView[@text="忘记密码"]')
    # 区域选择按钮
    AREA_SELECT_BUTTON = ("id", "com.lzy.wobird:id/ly_region")
    # 账号输入框
    ACCOUNT_INPUT = ("id", "com.lzy.wobird:id/et_account")
    # 发送验证码按钮
    SEND_CODE_BUTTON = ("id", "com.lzy.wobird:id/btn_get_code")
    # 验证码输入框
    CODE_INPUT = ("id", "com.lzy.wobird:id/pin_view")
    # 验证码页面断言
    CODE_ASSERT = ("id", "com.lzy.wobird:id/tv_desc")
    # 重置密码按钮
    RESET_PASSWORD_BUTTON = ("id", "com.lzy.wobird:id/btn_reset_password")
    # 未收到验证码提示
    NO_CODE_TIP = ("id", "com.lzy.wobird:id/tv_not_received")
    #重新发送验证码按钮
    RESEND_CODE_BUTTON = ("xpath", 'c//android.widget.TextView[@text="重新发送"]')
