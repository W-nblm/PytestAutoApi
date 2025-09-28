from utils.email_tool.temp_email import TempEmail
from utils.logging_tool.log_control import INFO
if __name__ == "__main__":
    obj = TempEmail()
    msg = obj.get_email_message()
    if msg:
        INFO.logger.info("最新邮件：", msg)
    code = obj.get_email_messages()
    if code:
        INFO.logger.info("验证码：", code)
