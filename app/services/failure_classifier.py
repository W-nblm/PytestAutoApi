import re

def classify_failure(message:str)->str:
    """简单的失败分类器，根据错误信息返回失败类别"""
    message = message.lower()
    if "missing" in message or "required" in message:
        return "缺少必填字段"
    if "type" in message and "expected" in message:
        return "字段类型不符"
    if "connection" in message or "timeout" in message:
        return "网络/超时错误"
    if "assert" in message and "code" in message:
        return "状态码断言失败"
    if "keyerror" in message:
        return "字段缺失(KeyError)"
    if "json" in message and "decode" in message:
        return "响应非 JSON 格式"
    return "未知错误"