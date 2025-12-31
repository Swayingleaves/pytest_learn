"""
Playwright测试示例

本文件演示如何使用pytest-playwright进行Web自动化测试。

Playwright要点：
1. 现代化的浏览器自动化工具
2. 支持Chromium、Firefox、WebKit
3. 自动等待元素，无需显式等待
4. 支持并行测试
5. 内置截图和视频录制

使用的工具：
- pytest-playwright: pytest插件，提供playwright fixtures
- Playwright API: 页面操作和元素定位

@author Test Engineer
@date 2025/01/01
"""

import pytest
from playwright.sync_api import Page, expect


class TestPlaywrightBasic:
    """
    Playwright基础测试类

    演示Playwright的基本功能。
    """

    def test_page_title(self, page: Page):
        """
        测试页面标题

        访问example.com并验证页面标题。
        """
        # 访问页面
        page.goto("https://example.com")

        # 验证页面标题
        expect(page).to_have_title("Example Domain")

    def test_click_button(self, page: Page):
        """
        测试点击按钮

        演示如何查找和点击元素。
        """
        # 访问页面
        page.goto("https://example.com")

        # 查找并点击链接（示例）
        # 注意：example.com页面很简单，这里仅作演示
        links = page.locator("a")
        expect(links).to_have_count(1)

    def test_input_text(self, page: Page):
        """
        测试输入文本

        演示如何填写表单。
        """
        # 访问带有表单的页面（使用demo页面）
        page.goto("https://demoqa.com/text-box")

        # 填写用户名
        page.fill("#userName", "Test User")

        # 填写邮箱
        page.fill("#userEmail", "test@example.com")

        # 填写当前地址
        page.fill("#currentAddress", "Test Address 123")

        # 验证输入的值
        expect(page.locator("#userName")).to_have_value("Test User")
        expect(page.locator("#userEmail")).to_have_value("test@example.com")


class TestPlaywrightAdvanced:
    """
    Playwright高级测试类

    演示Playwright的高级功能。
    """

    def test_screenshot_on_failure(self, page: Page):
        """
        测试失败时截图

        在测试失败时自动截图（需要在conftest.py中配置钩子）。
        """
        page.goto("https://example.com")
        page.screenshot(path="screenshot.png")

    def test_network_intercept(self, page: Page):
        """
        测试网络拦截

        演示如何拦截和修改网络请求。
        """
        # 记录所有请求
        requests = []

        def log_request(route, request):
            requests.append(request.url)
            route.continue_()

        page.route("**/*", log_request)

        page.goto("https://example.com")

        # 验证至少有一个请求
        assert len(requests) > 0

    def test_multiple_pages(self, context):
        """
        测试多页面操作

        演示如何在新标签页中打开页面。
        """
        # 创建新页面
        page = context.new_page()

        # 访问页面
        page.goto("https://example.com")

        # 验证标题
        expect(page).to_have_title("Example Domain")

        # 关闭页面
        page.close()


class TestPlaywrightAssertions:
    """
    Playwright断言测试类

    演示各种断言方式。
    """

    def test_element_visibility(self, page: Page):
        """
        测试元素可见性

        验证元素是否可见、隐藏或存在。
        """
        page.goto("https://example.com")

        # 验证h1元素可见
        h1 = page.locator("h1")
        expect(h1).to_be_visible()

        # 验证元素存在
        expect(h1).to_be_attached()

    def test_text_content(self, page: Page):
        """
        测试文本内容

        验证元素的文本内容。
        """
        page.goto("https://example.com")

        # 验证h1元素的文本
        h1 = page.locator("h1")
        expect(h1).to_have_text("Example Domain")

    def test_attribute_check(self, page: Page):
        """
        测试元素属性

        验证元素的属性值。
        """
        page.goto("https://example.com")

        # 验证链接的href属性
        link = page.locator("a")
        expect(link).to_have_attribute("href", "https://www.iana.org/domains/example")

    def test_css_properties(self, page: Page):
        """
        测试CSS属性

        验证元素的CSS样式。
        """
        page.goto("https://example.com")

        # 验证元素的CSS属性
        h1 = page.locator("h1")
        expect(h1).to_have_css("font-family", /Times New Roman/)


class TestPlaywrightForms:
    """
    Playwright表单测试类

    演示表单操作。
    """

    def test_select_dropdown(self, page: Page):
        """
        测试下拉选择框

        演示如何选择下拉选项。
        """
        page.goto("https://demoqa.com/select-menu")

        # 选择下拉选项
        page.select_option("#cars", "Volvo")

        # 验证选中的值
        expect(page.locator("#cars")).to_have_value("volvo")

    def test_checkbox(self, page: Page):
        """
        测试复选框

        演示如何勾选和取消勾选复选框。
        """
        page.goto("https://demoqa.com/checkbox")

        # 展开所有复选框
        page.click("button[title='Expand all']")

        # 勾选复选框
        page.check("input[type='checkbox']", first=True)

        # 验证复选框已勾选
        checkbox = page.locator("input[type='checkbox']").first
        expect(checkbox).to_be_checked()

    def test_radio_button(self, page: Page):
        """
        测试单选按钮

        演示如何选择单选按钮。
        """
        page.goto("https://demoqa.com/radio-button")

        # 选择单选按钮
        page.check("input[name='like'][value='Yes']")

        # 验证已选中的单选按钮
        expect(page.locator("input[name='like'][value='Yes']")).to_be_checked()


class TestPlaywrightWait:
    """
    Playwright等待测试类

    演示各种等待方式。
    """

    def test_wait_for_element(self, page: Page):
        """
        测试等待元素出现

        演示如何等待元素出现。
        """
        page.goto("https://example.com")

        # 等待h1元素出现（Playwright会自动等待）
        h1 = page.locator("h1")
        h1.wait_for()

        # 使用expect进行断言（自动等待）
        expect(h1).to_be_visible()

    def test_wait_for_navigation(self, page: Page):
        """
        测试等待导航完成

        演示如何等待页面导航完成。
        """
        # 等待导航完成
        page.goto("https://example.com", wait_until="networkidle")

        # 验证标题
        expect(page).to_have_title("Example Domain")

    def test_wait_for_response(self, page: Page):
        """
        测试等待网络响应

        演示如何等待特定的网络请求完成。
        """
        # 开始等待响应
        with page.expect_response("**/*") as response_info:
            page.goto("https://example.com")

        # 获取响应信息
        response = response_info.value
        assert response.status == 200
