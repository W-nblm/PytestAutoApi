import pytest
from base.android.android_ui_client import Android_UI_Client


@pytest.fixture(scope="session", autouse=True)
def app():
    # 初始化app
    driver = Android_UI_Client()

    yield driver

    driver.driver.quit()
