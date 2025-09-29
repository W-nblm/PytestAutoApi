import os
import yaml
import requests
import regex
from common.setting import ensure_path_sep
from utils.logging_tool.log_control import INFO, ERROR


class TempEmail:
    api_key = "1d2ac0d9b7msh553160860d35f17p15bddbjsn421dbc8f3b4f"

    def __init__(self, api_host="inboxes-com.p.rapidapi.com", new_email=False):
        self.random_email_file_path = ensure_path_sep("config/temp_email.yaml")
        self.api_host = api_host
        self.base_headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host,
            "Content-Type": "application/json",
        }

        self.temp_email = self._load_or_create_email()

        # 如果需要新邮箱，则生成新邮箱，否则激活已保存的邮箱
        if new_email:
            self.temp_email = self.random_email()
        else:
            self.activate_email(self.temp_email)
        self.message_id = None

    # ---------------- YAML 相关 ----------------
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

    # ---------------- 请求封装 ----------------
    def _request(self, method, url, **kwargs):
        try:
            response = requests.request(
                method, url, headers=self.base_headers, timeout=10, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            INFO.logger.info(f"Request error: {e}")
            return None

    # ---------------- 邮箱管理 ----------------
    def random_email(self):
        url = "https://inboxes-com.p.rapidapi.com/inboxes"
        data = self._request("POST", url, json={})
        if data is None:
            ERROR.logger.error("生成临时邮箱失败！")
            return None
        INFO.logger.info(f"请求结果：{data}")
        return data.get("inbox")

    def activate_email(self, email):
        url = f"https://inboxes-com.p.rapidapi.com/inboxes/{email}"
        return self._request("POST", url, json={})

    def delete_email(self, email=None):
        email = email or self.temp_email
        url = f"https://inboxes-com.p.rapidapi.com/inboxes/{email}"
        return self._request("DELETE", url, json={})

    def get_all_domains(self):
        url = "https://inboxes-com.p.rapidapi.com/domains"
        return self._request("GET", url)

    # ---------------- 邮件管理 ----------------
    def get_email_message(self, email=None):
        # 获取最新一封邮件
        email = email or self.temp_email
        url = f"https://inboxes-com.p.rapidapi.com/inboxes/{email}"
        data = self._request("GET", url)
        if data:
            message = data[0]
            self.message_id = message.get("uid")
            return message
        return None

    def get_email_messages(self, message_id=None):
        message_id = message_id or self.message_id
        url = f"https://inboxes-com.p.rapidapi.com/messages/{message_id}"
        data = self._request("GET", url)
        if not data:
            return None
        match = regex.search(r"(?<!\d)(\d{6})(?!\d)", str(data))
        return match.group(1) if match else None

    def delete_email_message(self, message_id=None):
        message_id = message_id or self.message_id
        url = f"https://inboxes-com.p.rapidapi.com/messages/{message_id}"
        return self._request("DELETE", url, json={})

    def get_email_attachment(self, message_id, attachment_id):
        url = f"https://inboxes-com.p.rapidapi.com/attachments/{message_id}/{attachment_id}"
        return self._request("GET", url)


if __name__ == "__main__":
    obj = TempEmail()
    msg = obj.get_email_message()
    if msg:
        INFO.logger.info("最新邮件：", msg)
    code = obj.get_email_messages()
    if code:
        INFO.logger.info("验证码：", code)
