# Pytest-Playwright 测试指南

## 概述

[Playwright](https://playwright.dev/) 是微软开发的现代化浏览器自动化测试工具，支持Chromium、Firefox和WebKit三大浏览器引擎。pytest-playwright是Playwright的pytest插件，提供了便捷的fixture支持和测试功能。

## 安装

### 1. 安装依赖

```bash
# 安装playwright和pytest插件
pip install pytest-playwright

# 安装浏览器（首次使用必须）
playwright install chromium

# 安装全部
playwright install
```

### 2. 验证安装

```bash
# 运行测试
pytest tests/test_playwright/test_playwright_demo.py -v

# 指定浏览器运行
pytest tests/test_playwright/ --browser chromium
pytest tests/test_playwright/ --browser firefox
pytest tests/test_playwright/ --browser webkit
```

## 核心特性

### 1. 自动等待机制

Playwright会自动等待元素可操作，无需显式等待：

```python
def test_auto_wait(page: Page):
    page.goto("https://example.com")

    # Playwright自动等待元素出现、可见、可点击
    page.click("button")  # 自动等待按钮可点击
    page.fill("input[name='email']", "test@example.com")  # 自动等待输入框可用
```

### 2. 多浏览器支持

pytest-playwright提供三种浏览器的fixture：

```python
def test_chromium(page):
    """默认使用Chromium"""
    page.goto("https://example.com")

@pytest.mark.skip_browser("firefox")
def test_not_firefox(page):
    """跳过Firefox浏览器"""

def test_with_all_browsers(page):
    """在所有安装的浏览器中运行"""
    pass
```

运行指定浏览器：
```bash
# Chromium（默认）
pytest test_playwright_demo.py --browser chromium

# Firefox
pytest test_playwright_demo.py --browser firefox

# WebKit（Safari）
pytest test_playwright_demo.py --browser webkit

# 同时运行多个浏览器
pytest test_playwright_demo.py --browser chromium --browser firefox
```

### 3. 内置Fixtures

pytest-playwright提供以下fixtures：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `browser_type_launch_args` | Session | 启动浏览器的参数 |
| `browser_context_args` | Session | 浏览器上下文参数 |
| `browser` | Session | 浏览器实例 |
| `context` | Function | 浏览器上下文（类似隐身模式） |
| `page` | Function | 页面对象（最常用） |

### 4. Page Object模式

推荐使用Page Object模式组织测试代码：

```python
class LoginPage:
    """登录页面对象"""

    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")

    def login(self, username, password):
        """登录方法"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

def test_login_with_page_object(page: Page):
    """使用Page Object模式测试登录"""
    login_page = LoginPage(page)
    page.goto("https://example.com/login")
    login_page.login("testuser", "password123")
    # 验证登录成功...
```

## 常用API

### 1. 页面导航

```python
# 访问URL
page.goto("https://example.com")

# 前进/后退
page.go_back()
page.go_forward()

# 刷新页面
page.reload()
```

### 2. 元素定位

```python
# CSS选择器（推荐）
page.locator("button")
page.locator("#submit-btn")
page.locator(".btn-primary")

# 文本选择器
page.get_by_text("Submit")
page.get_by_text("Login", exact=True)

# 角色选择器（无障碍访问）
page.get_by_role("button", name="Submit")

# 标签选择器
page.get_by_label("Email")

# 占位符选择器
page.get_by_placeholder("Enter your email")

# Alt文本选择器（图片）
page.get_by_alt_text("Logo")

# 测试ID选择器（推荐用于测试）
page.get_by_test_id("submit-button")
```

### 3. 元素操作

```python
# 点击
page.click("button")

# 填写表单
page.fill("input[name='email']", "test@example.com")

# 选择下拉选项
page.select_option("select#country", "China")

# 勾选/取消勾选复选框
page.check("input[type='checkbox']")
page.uncheck("input[type='checkbox']")

# 单选按钮
page.check("input[type='radio'][value='yes']")

# 上传文件
page.set_input_files("input[type='file']", "path/to/file.pdf")

# 悬停
page.hover("button")

# 聚焦
page.focus("input[name='email']")

# 获取文本内容
text = page.locator("h1").text_content()

# 获取属性值
href = page.locator("a").get_attribute("href")
```

### 4. 断言（推荐使用expect）

```python
from playwright.sync_api import expect

# 断言页面标题
expect(page).to_have_title("Example Domain")

# 断言元素可见
expect(page.locator("h1")).to_be_visible()

# 断言元素存在
expect(page.locator("h1")).to_be_attached()

# 断言元素文本
expect(page.locator("h1")).to_have_text("Example Domain")

# 断言元素属性
expect(page.locator("a")).to_have_attribute("href", "https://example.com")

# 断言输入框值
expect(page.locator("input")).to_have_value("test@example.com")

# 断言CSS属性
expect(page.locator("button")).to_have_css("background-color", "rgb(0, 128, 0)")

# 断言复选框状态
expect(page.locator("input[type='checkbox']")).to_be_checked()

# 断言元素数量
expect(page.locator("li")).to_have_count(5)

# 断言URL
expect(page).to_have_url("https://example.com/login")
```

### 5. 等待操作

```python
# Playwright会自动等待，通常不需要显式等待

# 等待导航完成
page.wait_for_load_state("networkidle")

# 等待特定元素
page.wait_for_selector(".loaded")

# 等待超时时间
page.wait_for_timeout(1000)  # 等待1秒（不推荐）

# 等待URL
page.wait_for_url("https://example.com/success")

# 等待特定请求/响应
with page.expect_response("**/api/data") as response_info:
    page.click("button")
response = response_info.value
```

## 高级功能

### 1. 截图和视频

```python
# 截图
page.screenshot(path="screenshot.png")
page.screenshot(path="fullpage.png", full_page=True)

# 只截取某个元素
page.locator("div.header").screenshot(path="header.png")

# 视频录制（需要在browser_context_args中配置）
# 在conftest.py中:
# browser_context_args = {"record_video_dir": "videos/"}
```

### 2. 网络拦截

```python
# 拦截请求
def handle_route(route):
    # 修改请求
    route.continue_(headers={"Authorization": "Bearer token"})

page.route("**/api/**", handle_route)

# 拦截并mock响应
page.route("**/api/data", lambda route: route.fulfill(
    status=200,
    body='{"mock": "data"}'
))

# 监听请求
def log_request(request):
    print(f"Request: {request.url}")

page.on("request", log_request)
```

### 3. 多标签页

```python
# 创建新页面
new_page = context.new_page()
new_page.goto("https://example.com")

# 等待新标签页打开
with page.expect_popup() as popup_info:
    page.click("a[target='_blank']")
new_page = popup_info.value
```

### 4. 执行JavaScript

```python
# 执行JavaScript代码
result = page.evaluate("() => document.title")
assert result == "Example Domain"

# 传递参数
result = page.evaluate("(a, b) => a + b", 1, 2)
assert result == 3

# 在元素上执行
element = page.locator("button")
element.evaluate("el => el.click()")
```

### 5. 下载文件

```python
# 开始下载
with page.expect_download() as download_info:
    page.click("button#download")

download = download_info.value
# 保存文件
download.save_as("path/to/save/file.pdf")
```

## 测试配置

### conftest.py配置

```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """配置浏览器启动参数"""
    return {
        **browser_type_launch_args,
        "headless": True,  # 无头模式
        "slow_mo": 100,    # 减慢操作速度（毫秒）
    }
```

### 失败时自动截图

在 `conftest.py` 中添加钩子：

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            screenshot_path = f"screenshots/{item.name}.png"
            import os
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)
```

## 运行测试

### 基本命令

```bash
# 运行所有playwright测试
pytest tests/test_playwright/

# 运行指定测试文件
pytest tests/test_playwright/test_playwright_demo.py -v

# 运行指定测试函数
pytest tests/test_playwright/test_playwright_demo.py::test_page_title -v

# 显示浏览器窗口（非无头模式）
pytest tests/test_playwright/ --headed

# 调试模式
pytest tests/test_playwright/ --debug

# 慢速模式（减慢操作）
pytest tests/test_playwright/ --slowmo 1000
```

### 并行执行

```bash
# 安装pytest-xdist
pip install pytest-xdist

# 并行执行测试（使用多个浏览器上下文）
pytest tests/test_playwright/ -n 4

# 并行执行测试（使用多个浏览器实例）
pytest tests/test_playwright/ --workers 4
```

### 选择浏览器

```bash
# 测试Chromium
pytest tests/test_playwright/ --browser chromium

# 测试Firefox
pytest tests/test_playwright/ --browser firefox

# 测试WebKit
pytest tests/test_playwright/ --browser webkit

# 测试所有浏览器
pytest tests/test_playwright/ --browser chromium --browser firefox --browser webkit
```

## 最佳实践

### 1. 使用定位器而非文本

```python
# ❌ 不推荐：使用硬编码的CSS选择器
page.click("div > div.container > button:nth-child(2)")

# ✅ 推荐：使用语义化的定位器
page.get_by_role("button", name="Submit")
```

### 2. 使用Page Object模式

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.submit = page.get_by_role("button", name="Login")
```

### 3. 使用expect断言

```python
# ✅ 推荐：使用expect（自动重试）
expect(page.locator("h1")).to_have_text("Welcome")

# ❌ 不推荐：使用普通断言（不等待）
assert page.locator("h1").text_content() == "Welcome"
```

### 4. 避免使用wait_for_timeout

```python
# ❌ 不推荐：硬编码等待
page.wait_for_timeout(5000)

# ✅ 推荐：使用自动等待或明确的等待条件
expect(page.locator(".loaded")).to_be_visible()
```

### 5. 使用测试ID

在HTML中添加 `data-testid` 属性：

```html
<button data-testid="submit-button">Submit</button>
```

测试中使用：

```python
page.get_by_test_id("submit-button").click()
```

### 6. 设置合理的超时

```python
# 设置页面默认超时
page.set_default_timeout(30000)  # 30秒

# 设置导航超时
page.set_default_navigation_timeout(60000)  # 60秒

# 单次操作设置超时
page.click("button", timeout=5000)
```

## 注意事项

1. **浏览器版本**：Playwright会下载特定版本的浏览器，确保不要手动更新这些浏览器

2. **无头模式**：默认使用无头模式，使用 `--headed` 参数可以看到浏览器窗口

3. **网络状态**：某些测试可能在网络不稳定时失败，使用 `wait_until="networkidle"` 等待网络空闲

4. **并发测试**：Playwright支持并行测试，但要注意资源限制和测试独立性

5. **清理资源**：每个测试使用独立的browser context，确保测试之间互不影响

## 相关资源

- [Playwright官方文档](https://playwright.dev/python/)
- [pytest-playwright文档](https://pytest-playwright.readthedocs.io/)
- [项目示例](../test_playwright/test_playwright_demo.py)
- [测试配置](conftest.py)
