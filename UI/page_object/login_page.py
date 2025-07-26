from UI.drivers.driver_factory import create_page


class LoginPage:
    url = "http://47.107.113.31:18090/"
    username = "@name=username"
    password = "@name=password"
    login_button = ".el-button el-button--primary el-button--medium"
    verification_code = "@placeholder=验证码"
    code_img = ".login-code-img"
    code_error = ".el-form-item__error"

    def __init__(self):
        self.page = create_page()

    # 打开登录页面
    def open_login_page(self):
        self.page.get(self.url)

    # 输入用户名
    def input_username(self, username):
        self.page.ele(self.username).clear().input(username)

    # 输入密码
    def input_password(self, password):
        self.page.ele(self.password).clear().input(password)

    # 点击登录按钮
    def click_login_button(self):
        self.page.ele(self.login_button).click()

    # 输入验证码
    def input_verification_code(self):
        code = self.get_verification_code()
        self.page.ele(self.verification_code).clear().input(code)

    # 验证码错误提示
    def get_code_error(self):
        return self.page.ele(self.code_error).text

    # 获取验证码的计算结果
    def get_verification_code(self):
        """
        获取验证码图片的base64编码,并通过ddddocr识别验证码
        验证码格式a*b=,其中a、b为数字,*为计算符号(+,-,*,/)
        """
        # 获取验证码图片的base64编码
        captcha_img = self.page.ele(".login-code-img")  # 识别验证码
        import ddddocr
        import base64

        ocr = ddddocr.DdddOcr()
        ocr.set_ranges("0123456789*-+")
        captcha_img.click()
        # 检查验证码格式,第一位和第三位必须为数字,第二位必须为+-*
        # 循环验证码识别结果,循环10次，每次间隔1秒，失败后不再继续尝试
        for i in range(10):
            img_str = captcha_img.link
            code = ocr.classification(base64.b64decode(img_str.split(",")[1]))

            if (
                len(code) >= 3
                and code[0] in "0123456789"
                and code[2] in "0123456789"
                and (code[1] in "+-*x")
            ):
                if code[1] == "x":
                    code = code.replace("x", "*")
                # 计算验证码的结果
                result = eval(code[:3])
                print(f"计算结果:{result}")
                return result
            else:
                print(f"识别结果:{code}")
                captcha_img.click()
                self.page.wait(1)
