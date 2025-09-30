from utils.email_tool.temp_email import TempEmailManager
from utils.logging_tool.log_control import INFO

if __name__ == "__main__":
    obj = TempEmailManager(provider="temp-email")
    msg = obj.random_email()
    if msg:
        INFO.logger.info(f"最新邮件：{msg}")
    code = obj.get_email_messages()
    print(code)
    if code:
        INFO.logger.info(f"验证码：{code}")
