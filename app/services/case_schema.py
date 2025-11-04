CASE_SCHEMA_EXAMPLE = {
    "name": "用户注册 - 成功",
    "base_url": "http://127.0.0.1:8000",
    "request": {
        "method": "POST",
        "url": "/api/v1/user/register",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "username": "string",
            "password": "string",
            "email": "string"
        }
    },
    "assert": {
        "status_code": 200,
        "body": {
            "code": 0,
            "message": "注册成功"
        }
    }
}
