
import pytest
from playwright.sync_api import sync_playwright,Page, expect


class TestCaseUI:

    """
    测试用例UI类
    包含所有与UI相关的测试用例。
    """

    @classmethod
    def setup_class(cls):
        """
        setup_class
        1、测试类第一个方法之前执行
        2、必须使用 @classmethod 装饰器；
        3、方法名必须严格是 setup_class（pytest 约定）
        类级别设置：整个测试类只登录一次 
        """
        # 手动构建playwright运行环境
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False, slow_mo=500)
        cls.context = cls.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='pytest-playwright-test',
            ignore_https_errors=True
        )
        # 把page存放在类属性中,其他所有的实例对象都可以通过self.page来访问
        cls.page = cls.context.new_page()
        # 登录页地址
        url = "https://172.25.53.92/login"
        # 打开登录页
        cls.page.goto(url)
        # 验证页面标题 可以通过浏览器f12查看到<html>代码中<head><title>标签的内容
        expect(cls.page).to_have_title("登录 - 终端运维保障平台")
        # 定位文本输入框，并填充输入值
        cls.page.locator('[name="username"]').fill('zhengl')
        # 定位密码输入框，并填充输入值
        cls.page.locator('[type="password"]').fill('Zd@123')
        # 定位登录按钮，并点击登录
        cls.page.locator('[type="button"][class="el-button el-button--primary"]').click()

        # 等待登录后跳转完成
        expect(cls.page).to_have_url("https://172.25.53.92/sub/dev/dashboard")

        # 方式1：使用name属性定位用户名输入框
        #page.locator('[name="username"]').fill('zhengl')
        # 方式2：使用placeholder属性定位用户名输入框
        #page.locator('[placeholder="用户名"]').fill('zhengl')
        # 方式3：使用CSS类定位用户名输入框-查找class属性值
        #page.locator('.el-input__inner').fill('zhengl')  # 如果页面只有一个这样的类
        # 方式4：使用更具体的CSS选择器
        #page.locator('input[name="username"]').fill('zhengl')
        # 方式5：使用XPath定位用户名输入框
        #page.locator('//input[@name="username"]').fill('zhengl')
        # 方式6: 使用多个属性定位用户名输入框
        #page.locator('[name="username"][placeholder="用户名"]').fill('zhengl')

        # 如果有id 可以使用id属性定位是最唯一的属性
        #page.locator('#id').fill('zhengl')

    @classmethod
    def teardown_class(cls):
        """
        类级别清理 
        1、整个测试类执行完毕后执行
        2、必须使用 @classmethod 装饰器
        3、方法名必须严格是 teardown_class（pytest 约定）
        """
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    # 在Playwright测试中，page 是一个fixture，pytest会自动注入Page对象。类型注解让IDE知道这是一个Page对象，从而提供相关的方法提示（如 goto(), click(), fill()等）。
    def test_ui_login(self):
        """
        测试UI登录验证
        """
        # setup_class 中已经登录完成，这里验证当前页面,如果已经跳转成功说明登录是成功的
        expect(self.page).to_have_url("https://172.25.53.92/sub/dev/dashboard")

    def test_search(self):
        """
        测试用例UI搜索
        验证用户能够在UI系统中成功搜索。
        """
        # 如果有弹窗，点击取消按钮
        cancel_btn = self.page.get_by_text("取消")
        try:
            cancel_btn.wait_for(state="visible", timeout=2000)
            cancel_btn.click()
        except:
            pass  # 没有弹窗，继续执行
        # 定位span 的值=终端管理 的元素
        self.page.get_by_text("终端管理").click()
        # 等待子菜单可见
        self.page.get_by_text("终端列表").wait_for(state="visible")
        # 点击子菜单中的"终端列表"
        self.page.get_by_text("终端列表").click()
        # 输入搜索关键词
        self.page.locator('input[placeholder="请输入关键词"]').fill('223344')
        # 点击查询按钮并等待结果
        self.page.get_by_text("查询").first.click()
        # 等待搜索结果加载完成
        self.page.wait_for_timeout(2000)
        # 验证搜索结果 - 检查文本存在于页面中
        # 方式1: 验证页面包含文本
        expect(self.page.locator("body")).to_contain_text("223344")
