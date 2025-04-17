"""日志装饰器"""

import ast
from functools import wraps
from utils.read_files_tool.regular_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR


def log_decorator(switch=True):
    """日志装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if switch:
                try:
                    res = func(*args, **kwargs)
                    _log_msg = (
                        f"\n======================================================\n"
                        f"用例标题: {res.detail}\n"
                        f"请求路径: {res.url}\n"
                        f"请求方式: {res.method}\n"
                        f"请求头:   {res.headers}\n"
                        f"请求内容: {res.request_body}\n"
                        f"接口响应内容: {res.response_data}\n"
                        f"接口响应时长: {res.res_time} ms\n"
                        f"Http状态码: {res.status_code}\n"
                        "====================================================="
                    )
                    _is_run = ast.literal_eval(cache_regular(str(res.is_run)))
                    if _is_run in (True, None) and res.status_code == 200:
                        INFO.logger.info(_log_msg)
                    else:
                        ERROR.logger.error(_log_msg)
                    return res
                except Exception as e:
                    ERROR.logger.exception(e)
                    raise e
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
