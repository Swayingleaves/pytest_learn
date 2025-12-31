"""
UI测试Fixtures

提供UI自动化测试所需的fixtures，包括：
- 浏览器实例
- WebDriver配置
- 页面等待设置

@author Test Engineer
@date 2025/01/01
"""

import pytest
from typing import Optional


class UIFixtures:
    """
    UI测试fixtures类

    提供Selenium WebDriver相关的fixtures。
    注意：实际使用时需要安装selenium和webdriver-manager。

    使用示例：
        class TestLoginPage:
            def test_login(self, browser, login_page):
                login_page.open()
                login_page.enter_username("admin")
                login_page.enter_password("123456")
                login_page.click_login()
                assert browser.title == "Dashboard"
    """

    @pytest.fixture
    def browser(self, settings) -> object:
        """
        获取浏览器实例

        使用webdriver-manager自动管理驱动程序。

        @param settings 全局配置对象
        @return WebDriver 浏览器驱动实例
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.options import Options

        # 配置Chrome选项
        options = Options()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # 使用webdriver-manager自动下载驱动程序
        service = Service(ChromeDriverManager().install())

        # 创建浏览器实例
        driver = webdriver.Chrome(service=service, options=options)

        # 设置隐式等待
        driver.implicitly_wait(settings.IMPLICIT_WAIT)

        yield driver

        # 测试结束后关闭浏览器
        driver.quit()

    @pytest.fixture
    def browser_config(self, settings) -> Dict[str, Any]:
        """
        返回浏览器配置

        @param settings 全局配置对象
        @return Dict 浏览器配置字典
        """
        return {
            "browser": settings.BROWSER,
            "implicit_wait": settings.IMPLICIT_WAIT,
            "explicit_wait": settings.EXPLICIT_WAIT,
            "timeout": settings.TIMEOUT
        }


# 创建实例供直接导入使用
ui_fixtures = UIFixtures()
