"""
Page Object模式示例

本文件演示如何使用Page Object模式编写UI测试。

什么是Page Object模式？
- 将页面抽象为对象
- 页面元素定位和操作封装在Page类中
- 测试用例只关注业务流程
- 提高代码复用性和可维护性

Page Object的好处：
1. 页面元素集中管理
2. 页面操作封装复用
3. 测试代码更清晰
4. 元素定位变更只需改一处

Page Object设计原则：
1. 页面元素定位器作为类的属性
2. 页面操作封装为类的方法
3. 不要在Page Object中写断言
4. 一个页面一个Page类

@author Test Engineer
@date 2025/01/01
"""


class TestPageObjectDemo:
    """
    Page Object模式演示测试类

    注意：由于这是一个示例项目，可能没有真实可测试的网站。
    下面的代码展示了Page Object的正确使用方式。
    """

    def test_login_page_structure(self):
        """
        测试LoginPage的结构

        演示Page Object的类结构定义。
        """
        # ========================================
        # 这是一个Page Object的示例结构
        # ========================================

        class LoginPage:
            """
            登录页面Page Object

            封装登录页面的所有元素和操作。
            """

            # ====================================
            # 元素定位器 - 使用By类定位元素
            # ====================================
            USERNAME_INPUT = "username"  # 用户名输入框
            PASSWORD_INPUT = "password"  # 密码输入框
            LOGIN_BUTTON = "login-btn"   # 登录按钮
            ERROR_MESSAGE = "error-msg"  # 错误消息

            def __init__(self, driver):
                """
                初始化Page Object

                @param driver WebDriver实例
                """
                self.driver = driver

            def open(self, url):
                """
                打开页面

                @param url 页面URL
                """
                self.driver.get(url)

            def enter_username(self, username):
                """
                输入用户名

                @param username 用户名
                """
                username_input = self.driver.find_element_by_id(
                    self.USERNAME_INPUT
                )
                username_input.clear()
                username_input.send_keys(username)

            def enter_password(self, password):
                """
                输入密码

                @param password 密码
                """
                password_input = self.driver.find_element_by_id(
                    self.PASSWORD_INPUT
                )
                password_input.clear()
                password_input.send_keys(password)

            def click_login(self):
                """
                点击登录按钮
                """
                login_button = self.driver.find_element_by_id(
                    self.LOGIN_BUTTON
                )
                login_button.click()

            def get_error_message(self):
                """
                获取错误消息

                @return str 错误消息文本
                """
                error_element = self.driver.find_element_by_id(
                    self.ERROR_MESSAGE
                )
                return error_element.text

            def login(self, username, password):
                """
                完整的登录流程

                @param username 用户名
                @param password 密码
                """
                self.enter_username(username)
                self.enter_password(password)
                self.click_login()

        # 验证Page Object结构
        assert hasattr(LoginPage, "USERNAME_INPUT")
        assert hasattr(LoginPage, "PASSWORD_INPUT")
        assert hasattr(LoginPage, "open")
        assert hasattr(LoginPage, "login")

    def test_search_page_structure(self):
        """
        测试SearchPage的结构

        演示另一个Page Object的示例。
        """
        class SearchPage:
            """
            搜索页面Page Object
            """

            SEARCH_INPUT = "search-input"
            SEARCH_BUTTON = "search-button"
            RESULTS = "search-results"

            def __init__(self, driver):
                self.driver = driver

            def open(self, url):
                self.driver.get(url)

            def enter_search_term(self, term):
                input_element = self.driver.find_element_by_id(
                    self.SEARCH_INPUT
                )
                input_element.clear()
                input_element.send_keys(term)

            def click_search(self):
                button = self.driver.find_element_by_id(
                    self.SEARCH_BUTTON
                )
                button.click()

            def search(self, term):
                """
                完整搜索流程

                @param term 搜索词
                """
                self.enter_search_term(term)
                self.click_search()

            def get_results_count(self):
                """
                获取搜索结果数量

                @return int 结果数量
                """
                results = self.driver.find_elements_by_css_selector(
                    f"#{self.RESULTS} > div"
                )
                return len(results)

        # 验证结构
        assert hasattr(SearchPage, "SEARCH_INPUT")
        assert hasattr(SearchPage, "search")


class TestPageObjectBestPractices:
    """
    Page Object最佳实践测试类

    演示Page Object的设计原则和最佳实践。
    """

    def test_page_object_principles(self):
        """
        测试Page Object设计原则

        验证Page Object是否遵循设计原则。
        """

        class ProductPage:
            """
            产品页面Page Object

            遵循Page Object设计原则：
            1. 元素定位器作为类属性
            2. 页面操作封装为方法
            3. 不包含断言
            4. 返回其他Page Object（页面跳转）
            """

            # 元素定位器
            ADD_TO_CART_BUTTON = "add-to-cart"
            QUANTITY_INPUT = "quantity"
            PRODUCT_NAME = "product-name"
            PRICE = "product-price"

            def __init__(self, driver):
                self.driver = driver

            def open_product(self, product_id):
                """打开产品详情页"""
                url = f"/products/{product_id}"
                self.driver.get(url)
                return self

            def set_quantity(self, quantity):
                """设置购买数量"""
                quantity_input = self.driver.find_element_by_id(
                    self.QUANTITY_INPUT
                )
                quantity_input.clear()
                quantity_input.send_keys(str(quantity))
                return self

            def add_to_cart(self):
                """添加到购物车"""
                button = self.driver.find_element_by_id(
                    self.ADD_TO_CART_BUTTON
                )
                button.click()
                # 返回购物车页面或其他Page Object
                from tests.test_ui.test_page_object import CartPage
                return CartPage(self.driver)

            def get_product_name(self):
                """获取产品名称"""
                name_element = self.driver.find_element_by_id(
                    self.PRODUCT_NAME
                )
                return name_element.text

            def get_price(self):
                """获取产品价格"""
                price_element = self.driver.find_element_by_id(
                    self.PRICE
                )
                return price_element.text

        class CartPage:
            """购物车页面Page Object"""

            def __init__(self, driver):
                self.driver = driver

            def open(self):
                self.driver.get("/cart")
                return self

        # 验证设计原则
        assert hasattr(ProductPage, "ADD_TO_CART_BUTTON")
        assert hasattr(ProductPage, "add_to_cart")
        assert hasattr(ProductPage, "set_quantity")
        assert hasattr(ProductPage, "get_product_name")


# ========================================
# 页面交互示例
# ========================================
#
# 实际测试用例示例：
#
# def test_add_product_to_cart(browser, base_url):
#     """
#     测试添加产品到购物车
#     """
#     # 创建Page Object
#     product_page = ProductPage(browser)
#
#     # 打开产品页面
#     product_page.open(base_url + "/product/123")
#
#     # 设置数量并添加到购物床
#     product_page.set_quantity(2).add_to_cart()
#
#     # 切换到购物车页面
#     cart_page = CartPage(browser)
#
#     # 验证购物车内容
#     assert cart_page.get_item_count() == 2
#
