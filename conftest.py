"""
Pytest全局配置文件

此文件是pytest的配置文件，会自动被pytest加载。
在这里定义全局可用的fixtures和钩子函数。

@author Test Engineer
@date 2025/01/01
"""

import pytest
import sys
from pathlib import Path

# ========================================
# 路径配置 - 将src目录添加到Python路径
# ========================================
# 这样可以在测试文件中直接导入src包下的模块
def add_src_to_path():
    """
    将src目录添加到Python路径

    这样测试文件可以直接使用：
        from src.utils.logger import get_logger
    """
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

add_src_to_path()


# ========================================
# 全局Fixtures
# ========================================

@pytest.fixture(scope="session")
def settings():
    """
    全局配置fixture

    提供对全局配置对象Settings的访问。
    使用session作用域，确保整个测试会话期间只创建一次。

    @return Settings 配置对象实例
    """
    from src.config.settings import Settings
    return Settings()


@pytest.fixture(scope="session")
def logger():
    """
    日志器fixture

    提供统一的日志记录功能。
    使用session作用域，确保日志器在整个会话期间一致。

    @return LoggerUtil 日志工具实例
    """
    from src.utils.logger import LoggerUtil
    return LoggerUtil()


@pytest.fixture(scope="function")
def timer():
    """
    测试计时器fixture

    用于测量测试执行时间，帮助识别慢测试。

    使用示例：
        def test_something(timer):
            with timer:
                # 执行测试代码
                pass
            print(f"测试耗时: {timer.elapsed:.2f}秒")

    @return TimerContext 测试计时器上下文
    """
    import time

    class Timer:
        """计时器类"""

        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.elapsed = 0

        def __enter__(self):
            """进入上下文时开始计时"""
            self.start_time = time.time()
            return self

        def __exit__(self, *args):
            """退出上下文时停止计时"""
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time

    return Timer()


# ========================================
# 测试目录级别Fixtures
# ========================================

@pytest.fixture
def test_data_file(settings):
    """
    获取测试数据文件路径

    @param settings 全局配置对象
    @return Path 测试数据文件路径
    """
    return settings.TEST_DATA_FILE


@pytest.fixture
def temp_dir(tmp_path):
    """
    提供临时目录

    用于测试中需要临时文件或目录的场景。

    @param tmp_path pytest内置的临时目录fixture
    @return Path 临时目录路径
    """
    return tmp_path


# ========================================
# 常用测试数据Fixtures
# ========================================

@pytest.fixture
def sample_user():
    """
    返回示例用户数据

    @return Dict 用户数据字典
    """
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "username": "testuser"
    }


@pytest.fixture
def sample_post():
    """
    返回示例帖子数据

    @return Dict 帖子数据字典
    """
    return {
        "userId": 1,
        "id": 1,
        "title": "Test Post Title",
        "body": "This is the test post body content."
    }


# ========================================
# Playwright测试Fixtures
# ========================================

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
        "slow_mo": 200,  # 慢动作模式，每个操作后暂停200毫秒
        "headless": False  # False 显示浏览器窗口 True 为无头模式不显示浏览器界面
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


@pytest.fixture(scope="class")
def ui_browser_and_context(browser_type_launch_args, browser_context_args):
    """
    UI测试用浏览器和上下文（类级别）

    提供整个测试类共享的浏览器实例和上下文，只启动一次。

    @param browser_type_launch_args 浏览器启动参数
    @param browser_context_args 浏览器上下文参数
    @return tuple (browser, context)
    """
    from playwright.sync_api import sync_playwright

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(**browser_type_launch_args)
    context = browser.new_context(**browser_context_args)

    yield browser, context

    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture(scope="class")
def logged_in_page(ui_browser_and_context, expect):
    """
    已登录的页面对象（类级别）

    自动执行登录操作，整个测试类只登录一次。

    @param ui_browser_and_context 浏览器和上下文
    @param expect Playwright断言工具
    @return 已登录的页面对象
    """
    browser, context = ui_browser_and_context
    page = context.new_page()

    # 登录
    url = "https://172.25.53.92/login"
    page.goto(url)
    expect(page).to_have_title("登录 - 终端运维保障平台")
    page.locator('[name="username"]').fill('zhengl')
    page.locator('[type="password"]').fill('Zd@123')
    page.locator('[type="button"][class="el-button el-button--primary"]').click()
    expect(page).to_have_url("https://172.25.53.92/sub/dev/dashboard")

    yield page


# ========================================
# Pytest Hooks (钩子函数)
# ========================================
def pytest_runtest_setup(item):
    """
    测试执行前钩子

    在每个测试用例执行前调用。

    使用场景：
    - 测试前的数据准备
    - 检查测试前置条件
    - 打印测试开始信息
    - 记录测试开始时间

    @param item 当前执行的测试用例
    """
    # 打印测试用例名称
    print(f"测试前执行")


def pytest_runtest_teardown(item, nextitem):
    """
    测试执行后钩子

    在每个测试用例执行后调用（无论成功或失败）。

    使用场景：
    - 清理测试数据
    - 关闭资源（文件、数据库连接等）
    - 打印测试结束信息

    @param item 当前执行的测试用例
    @param nextitem 下一个要执行的测试用例（可能是None）
    """
    # 打印测试完成信息
    print(f"测试后执行")

