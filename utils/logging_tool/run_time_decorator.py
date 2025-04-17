from utils.logging_tool.log_control import ERROR, INFO, WARNING


def execution_duration(number: int):
    """
    运行时间装饰器
    :param number: 运行时长
    :return:
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            run_time = res.res_time

            if run_time > number:
                ERROR.logger.error(
                    "\n==============================================\n"
                    "测试用例执行时间较长，请关注.\n"
                    "函数运行时间: %s ms\n"
                    "测试用例相关数据: %s\n"
                    "=================================================",
                    run_time,
                    res,
                )
            return res

        return wrapper

    return decorator
