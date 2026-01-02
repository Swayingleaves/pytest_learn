
import pytest
from playwright.sync_api import sync_playwright,Page, expect


class Test01CaseUI:
    # 定义一个类属性，后续赋值使用
    device_id = ''
    """
    UI测试用例类
    包含所有与UI相关的测试用例。
    """
    """
    属性定位方式：
    方式1：使用name属性定位用户名输入框
    page.locator('[name="username"]').fill('zhengl')
    方式2：使用placeholder属性定位用户名输入框
    page.locator('[placeholder="用户名"]').fill('zhengl')
    方式3：使用CSS类定位用户名输入框-查找class属性值
    page.locator('.el-input__inner').fill('zhengl')  # 如果页面只有一个这样的类
    方式4：使用更具体的CSS选择器
    page.locator('input[name="username"]').fill('zhengl')
    方式5：使用XPath定位用户名输入框
    page.locator('//input[@name="username"]').fill('zhengl')
    方式6: 使用多个属性定位用户名输入框
    page.locator('[name="username"][placeholder="用户名"]').fill('zhengl')

    如果有id 可以使用id属性定位是最唯一的属性
    page.locator('#id').fill('zhengl')
    """

    @classmethod
    def setup_class(cls):
        """
        setup_class
        1、测试类第一个方法之前执行，作为后续测试用例的前置条件
        2、必须使用 @classmethod 装饰器；
        3、方法名必须严格是 setup_class（pytest 约定）
        类级别设置：整个测试类只登录一次 
        """
        # 手动构建playwright运行环境
        cls.playwright = sync_playwright().start() # 启动playwright环境
        cls.browser = cls.playwright.chromium.launch(headless=False, slow_mo=200) # 启动浏览器 headless=False 表示不隐藏浏览器窗口 slow_mo=200 表示每个操作之间等待200毫秒
        cls.context = cls.browser.new_context( # 创建一个新的浏览器上下文
            viewport={'width': 1280, 'height': 720}, # 设置浏览器窗口大小
            ignore_https_errors=True # 忽略HTTPS错误(例如ssl证书类)，继续执行测试
        )
        # 把page存放在类属性中,其他所有的实例对象都可以通过self.page来访问
        cls.page = cls.context.new_page()  # 有了上下文才能创建page，并把page存放在类属性中，便于后面全局使用
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

    @classmethod
    def teardown_class(cls):
        """
        类级别清理 
        1、整个测试类执行完毕后执行,用于清理测试环境,如关闭浏览器、关闭数据库连接等,作为所有用例执行完毕的后续操作
        2、必须使用 @classmethod 装饰器
        3、方法名必须严格是 teardown_class（pytest 约定）
        """
        cls.context.close() # 关闭浏览器上下文
        cls.browser.close() # 关闭浏览器
        cls.playwright.stop() # 停止playwright环境

    def test_01_ui_login(self):
        """
        测试UI登录验证
        """
        # setup_class 中已经登录跳转完成，这里验证登录成功落地页是否是预期的
        expect(self.page).to_have_url("https://172.25.53.92/sub/dev/dashboard")

    def test_02_search(self):
        """
        测试用例UI搜索
        验证用户是否能够在UI系统中成功搜索。
        """
        # 如果有弹窗，点击取消按钮
        cancel_btn = self.page.get_by_text("取消")  # 通过”取消“二字文本定位按钮
        try:
            cancel_btn.wait_for(state="visible", timeout=2000)  # 等待取消按钮可见，最多等待2秒
            cancel_btn.click()  # 点击取消按钮
        except:
            pass  # 没有弹窗，继续执行
        #  通过”终端管理“文本定位一级菜单按钮，并点击，打开子菜单
        self.page.get_by_text("终端管理").click() 
        # 等待”终端列表“子菜单可见
        self.page.get_by_text("终端列表").wait_for(state="visible")
        # 点击子菜单中的"终端列表"
        self.page.get_by_text("终端列表").click()
        # 定位某个搜索条件输入框，并输入搜索关键词
        self.page.locator('input[placeholder="请输入关键词"]').fill('223344')
        # 定位查询按钮，并点击等待结果,'first'指当前页面匹配上多个元素时，取第一个操作
        self.page.get_by_text("查询").first.click()
        # 等待搜索结果加载完成
        self.page.wait_for_timeout(2000)

        # 验证搜索结果 - 检查表格第一条数据/第一行(tr=1---因为tr=0是表头)的第二列”终端编号“字段(td=1)是否等于搜索关键词"223344"
        expect(self.page.locator("tr").nth(1).locator("td").nth(1)).to_have_text("223344")
        # 将搜索结果中的终端编号保存到类属性中，后续用例可以使用,并使用strip方法去掉首尾空格
        Test01CaseUI.device_id = self.page.locator("tr").nth(1).locator("td").nth(1).text_content().strip()

    def test_03_search_detail(self):
        """
        测试用例UI搜索结果验证
        验证搜索结果是否符合预期。
        """
        # 点击表格第一行第二列中的 <a> 标签链接，打开详情页
        # 使用 force=True 强制点击（即使元素可能被遮挡）
        self.page.locator("tr").nth(1).locator("td").nth(1).locator("a").click(force=True)
        # 等待详情页面加载完成
        self.page.wait_for_timeout(5000)
        # 验证详情页面的URL是否包含预期的终端编号参数
        expect(self.page).to_have_url(f"https://172.25.53.92/sub/dev/devList/devListDetail?deviceId={Test01CaseUI.device_id}&deviceType=8")
        