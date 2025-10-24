import os
import random
from time import sleep
import yaml
import requests
import regex
from common.setting import ensure_path_sep
from utils.cache_process.cache_control import CacheHandler
from utils.logging_tool.log_control import INFO, ERROR


class TempEmailManager:
    api_key = "1d2ac0d9b7msh553160860d35f17p15bddbjsn421dbc8f3b4f"

    # 服务商映射表（简写 -> host）
    HOST_MAP = {
        "inboxes": "inboxes-com.p.rapidapi.com",
        "temp-email": "temp-email-api-disposable-temporary-email-service.p.rapidapi.com",
    }

    def __init__(self, provider="inboxes", new_email=False):
        """
        :param provider: 邮箱服务商，支持:
                    - "inboxes"
                    - "temp-email"
        """
        if provider not in self.HOST_MAP:
            raise ValueError(
                f"不支持的邮箱服务商: {provider}, 可选值: {list(self.HOST_MAP.keys())}"
            )

        self.provider = provider
        self.api_host = self.HOST_MAP[provider]

        self.random_email_file_path = ensure_path_sep("config/temp_email.yaml")
        self.base_headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host,
            "Content-Type": "application/json",
        }

        self.temp_email = self._load_or_create_email()

        if new_email:
            self.temp_email = self.random_email()
            self._save_email(self.temp_email)
        else:
            self.activate_email(self.temp_email)

        self.message_id = None

    # ---------------- YAML ----------------
    def _load_or_create_email(self):
        if os.path.exists(self.random_email_file_path):
            with open(self.random_email_file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                temp_email = data.get("temp_email")
                INFO.logger.info(f"上次使用的临时邮箱地址为：{temp_email}")
                return temp_email
        else:
            email = self.random_email()
            self._save_email(email)
            return email

    def _save_email(self, email):
        os.makedirs(os.path.dirname(self.random_email_file_path), exist_ok=True)
        with open(self.random_email_file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump({"temp_email": email}, f)

    # ---------------- 请求 ----------------
    def _request(self, method, url, **kwargs):
        try:
            INFO.logger.info(f"邮件管理请求: {method} {url} {kwargs}")
            response = requests.request(
                method, url, headers=self.base_headers, timeout=10, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            ERROR.logger.error(f"邮件管理请求错误: {e}")
            return None

    # ---------------- 邮箱管理 ----------------
    def random_email(self):
        if self.provider == "inboxes":
            url = "https://inboxes-com.p.rapidapi.com/inboxes"
            data = self._request("POST", url, json={})
            if not data:
                ERROR.logger.error("生成临时邮箱失败！")
                return None
            INFO.logger.info(f"生成邮箱inboxes：{data}")
            return data.get("inbox")

        elif self.provider == "temp-email":
            url = f"https://{self.api_host}/api/rapidapi/temp-email/new-email"
            data = self._request("POST", url, json={})
            if not data:
                ERROR.logger.error("生成临时邮箱失败！")
                return None
            INFO.logger.info(f"生成邮箱temp-email：{data.get('data').get('email')}")
            return data.get("data").get("email")

    def activate_email(self, email):
        if self.provider == "inboxes":
            url = f"https://inboxes-com.p.rapidapi.com/inboxes/{email}"
            return self._request("POST", url, json={})
        return {"msg": "此 API 不支持激活邮箱"}

    def delete_email(self, email=None, token=None):
        email = email or self.temp_email
        if self.provider == "inboxes":
            url = f"https://inboxes-com.p.rapidapi.com/inboxes/{email}"
            return self._request("DELETE", url, json={})
        elif self.provider == "temp-email":
            url = f"https://{self.api_host}/api/rapidapi/temp-email/delete-mail"
            params = {"email": email, "token": token or ""}
            return self._request("DELETE", url, params=params, json={})

    def get_all_domains(self):
        if self.provider == "inboxes":
            url = "https://inboxes-com.p.rapidapi.com/domains"
            return self._request("GET", url)
        return {"msg": "此 API 不支持获取域名"}

    # ---------------- 邮件管理 ----------------
    def get_email_list(self, email=None):
        email = email or self.temp_email
        if self.provider == "inboxes":
            url = f"https://inboxes-com.p.rapidapi.com/inboxes/{email}"
            data = self._request("GET", url)
            if data:
                message = data[0]
                self.message_id = message.get("uid")
                return message
            return None

        elif self.provider == "temp-email":
            return {"msg": "此 API 不支持获取最件列表"}

    def get_email_messages(self, message_id=None):
        message_id = message_id or self.message_id
        if self.provider == "inboxes":
            url = f"https://inboxes-com.p.rapidapi.com/messages/{message_id}"
            data = self._request("GET", url)
        else:
            url = f"https://{self.api_host}/api/rapidapi/temp-email/show-mails"
            data = self._request("GET", url, params={"email": self.temp_email})

        if not data:
            return None
        match = regex.search(r"(?<!\d)(\d{6})(?!\d)", str(data))
        return match.group(1) if match else None

    def delete_email_message(self, message_id=None):
        message_id = message_id or self.message_id
        if self.provider == "inboxes":
            url = f"https://inboxes-com.p.rapidapi.com/messages/{message_id}"
            return self._request("DELETE", url, json={})
        return {"msg": "此 API 不支持删除单封邮件"}

    def get_email_attachment(self, message_id, attachment_id):
        if self.provider == "inboxes":
            url = f"https://inboxes-com.p.rapidapi.com/attachments/{message_id}/{attachment_id}"
            return self._request("GET", url)
        return {"msg": "此 API 不支持附件下载"}

    def send_email(self, payload: dict):
        if self.provider == "temp-email":
            url = f"https://{self.api_host}/api/rapidapi/temp-email/send-email"
            return self._request("POST", url, json=payload or {})
        return {"msg": "此 API 不支持发送邮件"}

    def random_email_code(self):
        """生成随机邮箱"""
        try:
            mail = f"{random.randint(100000, 999999)}@nimail.cn"
            response = requests.post(
                "https://www.nimail.cn/api/applymail", data={"mail": mail}
            )
            response.raise_for_status()  # 检查请求是否成功，如果不是200系列状态码则抛出异常

            INFO.logger.info(f"申请邮箱成功: {response.text.strip()}")
            CacheHandler.update_cache(cache_name="random_email", value=mail)

            # 获取验证码
            return mail

        except requests.exceptions.HTTPError as http_err:
            ERROR.logger.error(f"HTTP 错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            ERROR.logger.error(f"请求错误: {req_err}")
        except Exception as e:
            ERROR.logger.error(f"未知错误: {e}")

    def get_random_email_code(self, email):

        import time

        for i in range(10):
            try:
                # 计算一次时间戳，避免重复计算
                current_time = int(time.time())
                response = requests.post(
                    "https://www.nimail.cn/api/getmails",
                    data={
                        "mail": email,
                        "time": current_time,
                        "_": current_time * 1000,
                    },
                )
                INFO.logger.info(f"email: {email}, time: {current_time}")
                INFO.logger.info(
                    f"第{i+1}次获取到的邮箱验证码为{response.text.strip()}"
                )
                response.raise_for_status()  # 检查请求是否成功，如果不是200系列状态码则抛出异常

                res = response.json()
                # 判断是否收取到邮件
                if not res.get("mail"):
                    INFO.logger.info("暂未收取到邮件", res)
                    sleep(3)
                else:

                    mail = res.get("mail")
                    mail_id = mail[0].get("id")
                    url = f"https://www.nimail.cn/api/raw-html/{email}/{mail_id}"
                    response = requests.get(url)
                    match = regex.search(r"(?<!\d)(\d{6})(?!\d)", response.text)
                    CacheHandler.update_cache(
                        cache_name="random_email_code", value=match.group(1)
                    )
                    return match.group(1) if match else None

            except requests.exceptions.HTTPError as http_err:
                ERROR.logger.error(f"HTTP 错误: {http_err}")
            except requests.exceptions.RequestException as req_err:
                ERROR.logger.error(f"请求错误: {req_err}")
            except Exception as e:
                ERROR.logger.error(f"未知错误: {e}")


if __name__ == "__main__":
    # ✅ 用简写方式
    obj = TempEmailManager(provider="inboxes", new_email=True)
    msg = obj.get_email_message()
    if msg:
        INFO.logger.info(f"最新邮件: {msg}")
    code = obj.get_email_messages()
    if code:
        INFO.logger.info(f"验证码: {code}")
