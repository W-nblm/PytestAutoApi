import pytest

@pytest.mark.parametrize("username, password, expected", [
    ("admin", "123456", True),
    ("guest", "wrongpass", False),
])
def test_login(username, password, expected):
    """模拟登录接口测试"""
    result = (username == "admin" and password == "123456")
    assert result == expected, f"登录失败: {username}"

def test_add():
    """模拟加法接口测试"""
    assert 1 + 1 == 2

def test_error_case():
    """模拟异常接口测试"""
    with pytest.raises(ZeroDivisionError):
        1 / 0
