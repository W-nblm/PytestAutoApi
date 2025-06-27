import base64
from DrissionPage import ChromiumOptions, ChromiumPage

from common.setting import ensure_path_sep

co = ChromiumOptions().set_paths(
    browser_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
)
page = ChromiumPage(co)
pages = page.tab_ids
print(pages)
# page.activate_tab(pages[1])
page.get("http://47.107.113.31:18090/product/category")
# page.get("https://music.163.com/")
tab = page.get_tab(title="龙之源")
page.activate_tab(tab)
tab_url = page.url
if "login" in tab_url:
    print("登录页面")
    # 登录页面
    name = page.ele("@name=username")
    name.clear().input("test02")
    password = page.ele("@name=password")
    password.clear().input("admin@lzy123")

    # 输入验证码
    captcha = page.ele("@placeholder=验证码")

    # 获取验证码的图片
    captcha_img = page.ele(".login-code-img")
    # 保存验证码图片的base64编码

    # 识别验证码
    import ddddocr

    ocr = ddddocr.DdddOcr()
    ocr.set_ranges("0123456789*-+")

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
            break
        else:
            print(f"识别结果:{code}")
            captcha_img.click()
            page.wait(1)
    captcha.input(result)

    login_btn = page.ele(".el-button el-button--primary el-button--medium")
    login_btn.click()
