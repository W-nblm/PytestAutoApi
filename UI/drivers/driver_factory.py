from DrissionPage import Chromium, ChromiumOptions


def create_page(headless=True):
    co = ChromiumOptions().set_browser_path(
        "C:\Program Files\Google\Chrome\Application\chrome.exe"
    )

    return Chromium(addr_or_opts=co).latest_tab


if __name__ == "__main__":
    page = create_page(headless=False)
    page.get("https://www.baidu.com")
