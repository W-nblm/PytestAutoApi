def success(data=None, message="success"):
    return {"code": 0, "message": message, "data": data}


def fail(message="failed", code=1):
    return {"code": code, "message": message}
