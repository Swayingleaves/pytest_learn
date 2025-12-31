"""
Playwright测试配置

本文件为Playwright测试提供额外的fixtures和钩子。

@author Test Engineer
@date 2025/01/01
"""

import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    配置浏览器启动参数

    设置浏览器启动时的参数，如慢动作模式（用于调试）。

    @param browser_type_launch_args 默认的浏览器启动参数
    @return 更新后的浏览器启动参数
    """
    return {
        **browser_type_launch_args,
        "slow_mo": 500,  # 慢动作模式，每个操作后暂停500毫秒
        "headless": False  # 显示浏览器窗口
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    配置浏览器上下文

    设置浏览器上下文参数，如viewport大小、忽略HTTPS错误等。

    @param browser_context_args 默认的浏览器上下文参数
    @return 更新后的浏览器上下文参数
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "zh-CN",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "extra_http_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    }


@pytest.fixture
def page(page):
    """
    配置页面

    为每个测试页面设置额外配置，如默认超时时间。

    @param page Playwright页面对象
    @return 配置后的页面对象
    """
    page.set_default_timeout(30000)  # 30秒
    page.set_default_navigation_timeout(30000)
    return page


def pytest_configure(config):
    """
    pytest配置钩子

    注册Playwright相关的自定义标记。
    """
    config.addinivalue_line("markers", "slow_browser: 慢速浏览器测试")
    config.addinivalue_line("markers", "skip_firefox: 跳过Firefox浏览器")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试结果钩子

    在测试失败时自动截图。

    @param item 测试用例
    @param call 测试调用信息
    """
    outcome = yield
    report = outcome.get_result()

    # 只在测试执行完成且失败时截图
    if report.when == "call" and report.failed:
        # 获取page fixture（如果存在）
        if "page" in item.fixturenames:
            page = item.funcargs["page"]

            # 生成截图文件名
            test_name = item.name
            screenshot_path = f"screenshots/{test_name}.png"

            # 确保目录存在
            import os
            os.makedirs("screenshots", exist_ok=True)

            # 截图
            page.screenshot(path=screenshot_path, full_page=True)

            print(f"\n  📸 失败截图已保存: {screenshot_path}")
