import pytest
from UI.page_object.login_page import LoginPage


class TestLogin:
    @pytest.mark.parametrize("username,password", [("test02", "admin@lzy123")])
    def test_login(self, username, password):
        login_page = LoginPage()
        login_page.open_login_page()
        login_page.input_username(username)
        login_page.input_password(password)
        login_page.input_verification_code()
        login_page.click_login_button()
