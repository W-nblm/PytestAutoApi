# from utils.email_tool.temp_email import TempEmailManager
# from utils.logging_tool.log_control import INFO

# if __name__ == "__main__":
#     obj = TempEmailManager(provider="temp-email")
#     msg = obj.random_email()
#     if msg:
#         INFO.logger.info(f"最新邮件：{msg}")
#     code = obj.get_email_messages()
#     print(code)
#     if code:
#         INFO.logger.info(f"验证码：{code}")
import regex
import requests
from bs4 import BeautifulSoup
import time
import random


class NimailClient:
    def __init__(self):
        self.base_url = "https://www.nimail.cn"
        # self.session = requests.Session()
        self.current_email = ""

    def generate_email(self, mail):
        """生成随机邮箱"""
        response = requests.post(f"{self.base_url}/api/applymail", data={"mail": mail})
        if response.status_code == 200:
            self.current_email = response.text.strip()
            print(f"生成新邮箱: {response.text}")
            return self.current_email
        return None

    def check_mails(self, mail):
        """检查邮箱中的邮件"""
        # if not self.current_email:
        #     print("请先生成邮箱地址")
        #     return []
        import time

        # 尝试5次获取邮件
        for i in range(10):
            timestr = int(time.time())
            response = requests.post(
                f"{self.base_url}/api/getmails",
                data={
                    "mail": mail,
                    "time": timestr,
                    "_": timestr * 1000,
                },
            )

            if not response.json().get("mail"):
                print("暂未收到邮件")
                time.sleep(1)
            else:
                print(f"收到邮件{response.json()}")
                return mail


# 使用示例
if __name__ == "__main__":
    client = NimailClient()
    # 生成新邮箱
    mail = f"{random.randint(10000, 999999)}@nimail.cn"
    # email = client.generate_email(mail)
    # print(f"最新邮箱: {email}")
    # # 模拟等待邮件
    # print("等待邮件中...（模拟场景）")
    # time.sleep(3)

    mails = client.check_mails("221175@nimail.cn")

    # return
    # res = {
    #     "to": "981578@nimail.cn",
    #     "mail": [
    #         {
    #             "subject": "\u8f6c\u53d1\uff1a\u8f6c\u53d1\uff1atest",
    #             "id": "1761030956292",
    #             "email": "981578@nimail.cn",
    #             "from": "\u6c6a\u6708\u51ef &lt;cpb-csz-01@szlongzy.com&gt;",
    #             "reply-to": "",
    #             "cc": "",
    #             "md5": "55e2f9ce06a499a2a77aad9f5b36fa9b",
    #             "mail-len": 32480,
    #             "attachments": [
    #                 "https:\/\/www.nimail.cn\/api\/attachment\/981578@nimail.cn\/5a4d9f6c9deea0d9d2053bcdc2b18a6b_-569356276png"
    #             ],
    #             "time": "2025-10-21 15:15:56",
    #         }
    #     ],
    #     "success": "true",
    #     "time": 1761030971,
    # }
    # match = regex.search(r"(?<!\d)(\d{6})(?!\d)", str(res))
    # print(match.group(1) if match else None)
    re = {
        "url": "http://47.107.113.31:18090/prod-api/app/info/appUser/registerCheckCodeTest",
        "method": "POST",
        "detail": "app用户控 制器 - TEST 注册 单独校验验证码 不需要加密",
        "assert_data": {
            "code": {
                "jsonpath": "$.code",
                "type": "==",
                "value": 200,
                "AssertType": None,
                "message": "接口状态码不为200",
            },
            "msg": {
                "jsonpath": "$.msg",
                "type": "contains",
                "value": "成功",
                "AssertType": None,
            },
        },
        "headers": {
            "Authorization": "$cache{app_token}",
            "Content-Language": "zh_CN",
            "App-Source": "WObird",
        },
        "requestType": "JSON",
        "is_run": None,
        "data": {
            "customId": "$cache{customId}",
            "email": "$cache{random_email}",
            "mailCode": "$cache{random_email_code}",
            "password": "w12345678",
            "timezoneId": "",
            "countryCode": "US",
            "wopetUserInfo": {
                "phoneCode": "",
                "countryName": "",
                "nationalNumber": "",
                "headPic": "",
                "sex": "",
                "nickName": "",
            },
        },
        "dependence_case": False,
        "dependence_case_data": None,
        "sql": None,
        "setup_sql": None,
        "status_code": None,
        "teardown_sql": None,
        "teardown": None,
        "current_request_set_cache": None,
        "sleep": None,
    }
