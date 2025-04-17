from typing import Union, Text, Any


def equals(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否相等"""
    assert check_value == expect_value, message


def less_than(
    check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果小于预期结果"""
    assert check_value < expect_value, message


def less_than_or_equals(
    check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果小于等于预期结果"""
    assert check_value <= expect_value, message


def greater_than(
    check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果大于预期结果"""
    assert check_value > expect_value, message


def greater_than_or_equals(
    check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果大于等于预期结果"""
    assert check_value >= expect_value, message


def not_equals(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否不相等"""
    assert check_value != expect_value, message


def string_equals(check_value: Text, expect_value: Any, message: Text = ""):
    """判断字符串是否相等"""
    assert check_value == str(expect_value), message


def length_equals(check_value: Text, expect_value: int, message: Text = ""):
    """判断字符串长度是否相等"""
    assert isinstance(expect_value, int), "expect_value must be int"
    assert len(check_value) == expect_value, message


def length_greater_than(
    check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断字符串长度是否大于预期值"""
    assert isinstance(expect_value, (int, float)), "expect_value must be int or float"
    assert len(str(check_value)) > expect_value, message


def length_greater_than_or_equals(
    check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断字符串长度是否大于等于预期值"""
    assert isinstance(expect_value, (int, float)), "expect_value must be int or float"
    assert len(str(check_value)) >= expect_value, message


def length_less_than(
    check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断字符串长度是否小于预期值"""
    assert isinstance(expect_value, (int, float)), "expect_value must be int or float"
    assert len(str(check_value)) < expect_value, message


def contains(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否包含"""
    assert isinstance(
        check_value, (list, tuple, dict, str, bytes)
    ), "check_value must be list,tuple,dict,str or bytes"
    assert expect_value in check_value, message


def contained_by(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否被包含"""
    assert isinstance(
        expect_value, (list, tuple, dict, str, bytes)
    ), "expect_value must be list,tuple,dict,str or bytes"
    assert check_value in expect_value, message


def startswitch(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否以expect_value开头"""
    assert str(check_value).startswith(str(expect_value)), message


def endswith(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否以expect_value结尾"""
    assert str(check_value).endswith(str(expect_value)), message
