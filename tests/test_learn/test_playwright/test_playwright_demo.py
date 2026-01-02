"""
Playwright测试示例

本文件演示如何使用pytest-playwright进行Web自动化测试。

所有测试使用本地HTML页面，确保测试稳定可靠。

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
import re
from pathlib import Path
from playwright.sync_api import Page, expect


# 获取测试页面的绝对路径
TEST_PAGE_PATH = f"file://{Path(__file__).parent.resolve()}/test_page.html"


class TestPlaywrightBasic:
    """
    Playwright基础测试类

    演示Playwright的基本功能。
    """

    def test_page_title(self, page: Page):
        """
        测试页面标题

        访问测试页面并验证页面标题。
        """
        # 访问测试页面 这里使用的本地HTML文件，实际测试中应替换为目标URL比如https://www.baidu.com
        page.goto(TEST_PAGE_PATH)

        # 验证页面标题
        expect(page).to_have_title("Playwright测试页面")

    def test_click_button(self, page: Page):
        """
        测试点击按钮

        演示如何查找和点击按钮。
        """
        page.goto(TEST_PAGE_PATH)

        # 点击提交按钮
        submit_button = page.locator("#submit-button")
        submit_button.click()

        # 验证结果显示
        result_div = page.locator("#result")
        expect(result_div).to_be_visible()

    def test_input_text(self, page: Page):
        """
        测试输入文本

        演示如何在输入框中输入文本并验证。
        """
        page.goto(TEST_PAGE_PATH)

        # 定位文本输入框
        text_input = page.locator("#text-input")

        # 输入文本
        text_input.fill("北京")

        # 验证输入框的值
        expect(text_input).to_have_value("北京")

        # 测试数字输入框
        number_input = page.locator("#number-input")
        number_input.fill("123")
        expect(number_input).to_have_value("123")


class TestPlaywrightAdvanced:
    """
    Playwright高级测试类

    演示Playwright的高级功能。
    """

    def test_screenshot_on_failure(self, page: Page):
        """
        测试截图

        演示如何截取页面和元素的截图。
        """
        page.goto(TEST_PAGE_PATH)

        # 截取整个页面
        page.screenshot(path="screenshots/full_page.png", full_page=True)

        # 截取特定元素
        section = page.locator("#input-section")
        section.screenshot(path="screenshots/input_section.png")

    def test_network_intercept(self, page: Page):
        """
        测试网络拦截

        演示如何拦截和记录网络请求。
        """
        # 记录所有请求
        requests = []

        def log_request(route, request):
            requests.append(request.url)
            route.continue_()

        page.route("**/*", log_request)

        page.goto(TEST_PAGE_PATH)

        # 验证至少有请求发生
        assert len(requests) > 0

    def test_multiple_pages(self, context):
        """
        测试多页面操作

        演示如何在新标签页中打开页面。
        """
        # 创建新页面
        page = context.new_page()

        # 访问测试页面
        page.goto(TEST_PAGE_PATH)

        # 验证标题
        expect(page).to_have_title("Playwright测试页面")

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
        page.goto(TEST_PAGE_PATH)

        # 验证可见元素
        visible_element = page.locator("#visible-element")
        expect(visible_element).to_be_visible()

        # 验证隐藏元素
        hidden_element = page.locator("#hidden-element")
        expect(hidden_element).not_to_be_visible()

        # 点击按钮切换可见性
        page.click("#toggle-button")
        expect(hidden_element).to_be_visible()

    def test_text_content(self, page: Page):
        """
        测试文本内容

        验证元素的文本内容。
        """
        page.goto(TEST_PAGE_PATH)

        # 验证h1元素的文本
        h1 = page.locator("h1")
        expect(h1).to_have_text("Playwright测试页面")

        # 验证可见元素的文本
        visible_element = page.locator("#visible-element")
        expect(visible_element).to_have_text("这是一个可见的元素")

    def test_attribute_check(self, page: Page):
        """
        测试元素属性

        验证元素的属性值。
        """
        page.goto(TEST_PAGE_PATH)

        # 验证链接的href属性
        link = page.locator("#example-link")
        expect(link).to_have_attribute("href", "https://iana.org/domains/example")

        # 验证输入框的placeholder属性
        text_input = page.locator("#text-input")
        expect(text_input).to_have_attribute("placeholder", "请输入文本")

    def test_css_properties(self, page: Page):
        """
        测试CSS属性

        验证元素的CSS样式。
        """
        page.goto(TEST_PAGE_PATH)

        # 验证元素的CSS属性
        css_element = page.locator("#css-test-element")
        expect(css_element).to_have_css("color", "rgb(0, 123, 255)")
        expect(css_element).to_have_css("font-weight", "700")

        # 使用正则表达式匹配
        h1 = page.locator("h1")
        expect(h1).to_have_css("font-family", re.compile(r"system-ui|sans-serif"))


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
        page.goto(TEST_PAGE_PATH)

        # 选择下拉选项
        cars_select = page.locator("#cars")
        cars_select.select_option("Volvo")

        # 验证选中的值
        expect(cars_select).to_have_value("volvo")

        # 选择另一个选项
        cars_select.select_option("Audi")
        expect(cars_select).to_have_value("audi")

    def test_checkbox(self, page: Page):
        """
        测试复选框

        演示如何勾选和取消勾选复选框。
        """
        page.goto(TEST_PAGE_PATH)

        # 勾选第一个复选框
        checkbox1 = page.locator("#checkbox1")
        checkbox1.check()
        expect(checkbox1).to_be_checked()

        # 勾选第二个复选框
        checkbox2 = page.locator("#checkbox2")
        checkbox2.check()
        expect(checkbox2).to_be_checked()

        # 取消勾选第一个复选框
        checkbox1.uncheck()
        expect(checkbox1).not_to_be_checked()

    def test_radio_button(self, page: Page):
        """
        测试单选按钮

        演示如何选择单选按钮。
        """
        page.goto(TEST_PAGE_PATH)

        # 选择第一个单选按钮
        radio1 = page.locator("#radio1")
        radio1.check()
        expect(radio1).to_be_checked()

        # 选择第二个单选按钮（第一个会自动取消选中）
        radio2 = page.locator("#radio2")
        radio2.check()
        expect(radio2).to_be_checked()
        expect(radio1).not_to_be_checked()


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
        page.goto(TEST_PAGE_PATH)

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
        page.goto(TEST_PAGE_PATH, wait_until="networkidle")

        # 验证标题
        expect(page).to_have_title("Playwright测试页面")

    def test_wait_for_response(self, page: Page):
        """
        测试等待网络响应

        演示如何等待特定的网络请求完成。
        """
        # 开始等待响应
        with page.expect_response("**/*") as response_info:
            page.goto(TEST_PAGE_PATH)

        # 获取响应信息
        response = response_info.value
        assert response.status == 200 or response.status == 304  # 304 for cached resources


class TestPlaywrightInteractions:
    """
    Playwright交互测试类

    演示用户交互操作。
    """

    def test_form_workflow(self, page: Page):
        """
        测试完整的表单工作流程

        演示多个表单元素的组合操作。
        """
        page.goto(TEST_PAGE_PATH)

        # 填写文本输入框
        text_input = page.locator("#text-input")
        text_input.fill("测试文本")

        # 填写数字输入框
        number_input = page.locator("#number-input")
        number_input.fill("456")

        # 选择下拉选项
        cars_select = page.locator("#cars")
        cars_select.select_option("Saab")

        # 勾选复选框
        checkbox1 = page.locator("#checkbox1")
        checkbox1.check()

        # 选择单选按钮
        radio2 = page.locator("#radio2")
        radio2.check()

        # 点击提交按钮
        submit_button = page.locator("#submit-button")
        submit_button.click()

        # 验证结果显示
        result_div = page.locator("#result")
        expect(result_div).to_be_visible()
        expect(result_div).to_contain_text("测试文本")
        expect(result_div).to_contain_text("456")

    def test_keyboard_and_mouse(self, page: Page):
        """
        测试键盘和鼠标操作

        演示键盘输入和鼠标交互。
        """
        page.goto(TEST_PAGE_PATH)

        # 使用键盘输入
        text_input = page.locator("#text-input")
        text_input.click()
        page.keyboard.type("键盘输入测试")

        # 验证输入
        expect(text_input).to_have_value("键盘输入测试")

        # 使用键盘全选并删除（macOS使用Meta+A，其他系统使用Control+A）
        text_input.click()
        import platform
        if platform.system() == "Darwin":  # macOS
            page.keyboard.press("Meta+A")
        else:
            page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        expect(text_input).to_have_value("")

        # 悬停在按钮上
        submit_button = page.locator("#submit-button")
        submit_button.hover()

    def test_javascript_execution(self, page: Page):
        """
        测试JavaScript执行

        演示如何在页面中执行JavaScript代码。
        """
        page.goto(TEST_PAGE_PATH)

        # 执行JavaScript获取标题
        title = page.evaluate("() => document.title")
        assert title == "Playwright测试页面"

        # 执行JavaScript修改元素
        page.evaluate("() => document.getElementById('text-input').value = 'JS输入'")
        text_input = page.locator("#text-input")
        expect(text_input).to_have_value("JS输入")

        # 执行JavaScript获取元素数量
        input_count = page.evaluate("() => document.querySelectorAll('input').length")
        assert input_count > 0


class TestPlaywrightElementLocation:
    """
    Playwright元素定位测试类

    演示各种元素定位方法。
    """

    def test_css_selector(self, page: Page):
        """
        测试CSS选择器定位
        """
        page.goto(TEST_PAGE_PATH)

        # 使用ID选择器
        element_by_id = page.locator("#text-input")
        expect(element_by_id).to_be_visible()

        # 使用class选择器
        elements_by_class = page.locator(".section")
        expect(elements_by_class).to_have_count(7)

        # 使用属性选择器
        element_by_attr = page.locator("input[type='checkbox']")
        expect(element_by_attr).to_have_count(3)

    def test_text_selector(self, page: Page):
        """
        测试文本选择器定位
        """
        page.goto(TEST_PAGE_PATH)

        # 使用文本定位
        link_by_text = page.get_by_text("点击这里访问Example Domains")
        expect(link_by_text).to_be_visible()

        # 使用精确文本匹配
        link_by_exact_text = page.get_by_text("Playwright测试页面", exact=True)
        expect(link_by_exact_text).to_be_visible()

    def test_role_selector(self, page: Page):
        """
        测试角色选择器定位
        """
        page.goto(TEST_PAGE_PATH)

        # 使用角色定位按钮
        button = page.get_by_role("button", name="提交")
        expect(button).to_be_visible()

        # 使用角色定位复选框
        checkbox = page.get_by_role("checkbox", name="选项1")
        expect(checkbox).to_be_visible()

    def test_label_selector(self, page: Page):
        """
        测试标签选择器定位
        """
        page.goto(TEST_PAGE_PATH)

        # 通过label定位输入框
        text_input = page.get_by_label("文本输入：")
        expect(text_input).to_be_visible()

        # 通过placeholder定位
        number_input = page.get_by_placeholder("请输入数字")
        expect(number_input).to_be_visible()


class TestCsdnSearch:
    """
    CSDN博客搜索测试类

    演示在真实网站上进行搜索测试。

    注意：CSDN有反爬虫机制,需要设置合适的User-Agent和浏览器参数。
    """

    def test_search_pytest_on_csdn(self, page: Page):
        """
        测试在CSDN博客搜索"pytest"

        访问CSDN博客首页,在搜索框中输入"pytest",点击搜索按钮。

        注意：CSDN的搜索功能可能不会立即跳转到搜索结果页，
        本测试主要验证搜索框的定位和交互功能。
        """
        # 访问CSDN博客
        page.goto("https://blog.csdn.net/", wait_until="domcontentloaded")

        # 等待页面加载完成
        page.wait_for_timeout(3000)

        # 定位搜索输入框
        search_input = page.locator("#toolbar-search-input")

        # 使用更长的超时时间
        search_input.wait_for(timeout=10000, state="visible")

        # 验证搜索框的placeholder
        expect(search_input).to_have_attribute("placeholder", "搜CSDN")

        # 输入搜索关键词"pytest"
        search_input.fill("pytest")

        # 验证输入框的值
        expect(search_input).to_have_value("pytest")

        # 定位搜索按钮
        search_button = page.locator("#toolbar-search-button")
        expect(search_button).to_be_visible()

        # 验证搜索按钮文本
        expect(search_button).to_contain_text("搜索")

        # 点击搜索按钮
        search_button.click()

        # 等待一下看是否有页面跳转
        page.wait_for_timeout(2000)
