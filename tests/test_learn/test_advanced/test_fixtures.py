"""
Fixtures深入理解示例

本文件详细介绍pytest的fixture功能。

什么是Fixture？
- Fixture是pytest的核心功能
- 用于准备测试数据、设置测试环境、清理资源
- 使用@pytest.fixture装饰器定义
- 可以声明依赖关系，自动注入

Fixture的作用域（scope）：
- function: 每个测试函数执行一次（默认）
- class: 每个测试类执行一次
- module: 每个测试模块执行一次
- session: 整个测试会话执行一次

Fixture生命周期：
1. 创建：按依赖关系创建fixture
2. 注入：将返回值传递给测试函数
3. 清理：执行teardown代码

@author Test Engineer
@date 2025/01/01
"""

import pytest


class TestFixturesBasic:
    """
    Fixture基础测试类

    演示fixture的基本用法。
    """

    @pytest.fixture
    def sample_data(self):

        """
        创建一个示例数据fixture

        这个fixture会在每个测试函数执行前创建。

        @return Dict 示例数据
        """
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "age": 25
        }
        return data

    def test_use_sample_data(self, sample_data):
        """
        测试使用fixture

        fixture会自动作为参数传入测试函数。
        """
        # 使用fixture提供的数据
        assert sample_data["name"] == "Test User"
        assert sample_data["email"] == "test@example.com"

    def test_data_independence(self, sample_data):
        """
        测试数据独立性

        每个测试函数都会获取新的fixture数据，
        修改不会影响其他测试。
        """
        # 修改数据
        sample_data["age"] = 30
        assert sample_data["age"] == 30


class TestFixtureScopes:
    """
    Fixture作用域测试类

    演示不同作用域的fixture行为。
    """

    # Module级别的计数器
    module_counter = 0

    @pytest.fixture(scope="module")
    def module_data(self):
        """
        Module级别的fixture

        在同一个模块的所有测试中只创建一次。

        @return str 模块数据
        """
        TestFixtureScopes.module_counter += 1
        return {"counter": TestFixtureScopes.module_counter}

    @pytest.fixture(scope="class")
    def class_data(self):
        """
        Class级别的fixture

        在同一个测试类的所有测试中只创建一次。
        """
        return {"class_name": self.__class__.__name__}

    def test_module_scope_1(self, module_data):
        """
        测试模块作用域1
        """
        assert module_data["counter"] == 1

    def test_module_scope_2(self, module_data):
        """
        测试模块作用域2

        使用同一个module_data fixture
        """
        # counter仍然是1，因为是同一个module实例
        assert module_data["counter"] == 1


class TestFixtureDependencies:
    """
    Fixture依赖测试类

    演示fixture之间的依赖关系。
    """

    @pytest.fixture
    def base_value(self):
        """
        基础值fixture
        """
        return 10

    @pytest.fixture
    def calculated_value(self, base_value):
        """
        计算值fixture

        依赖于base_value fixture。
        pytest会自动按依赖顺序创建fixture。
        """
        return base_value * 2

    def test_dependency_injection(self, base_value, calculated_value):
        """
        测试依赖注入

        fixture按依赖顺序自动注入。
        """
        assert base_value == 10
        assert calculated_value == 20

    def test_independent_calculation(self, calculated_value):
        """
        测试独立使用依赖的fixture
        """
        # 即使只请求calculated_value，
        # base_value也会被创建
        assert calculated_value == 20


class TestFixtureTeardown:
    """
    Fixture清理测试类

    演示如何使用yield进行资源清理。
    """

    @pytest.fixture
    def resource_with_cleanup(self):
        """
        模拟需要清理的资源

        使用yield关键字返回数据，
        yield之后的代码在测试完成后执行（清理）。
        """
        # 模拟资源创建
        resource = {"data": "created"}
        print("\n  资源创建")

        # 使用yield返回资源
        yield resource

        # 测试完成后执行清理
        print("  资源清理")
        # 实际场景中可能是：关闭文件、关闭数据库连接等

    def test_with_cleanup(self, resource_with_cleanup):
        """
        测试使用需要清理的资源
        """
        assert resource_with_cleanup["data"] == "created"


class TestFixtureAutouse:
    """
    自动使用Fixture测试类

    演示如何使用autouse自动应用fixture。
    """

    @pytest.fixture(autouse=True)
    def automatic_setup(self):
        """
        自动应用的fixture

        设置autouse=True后，所有测试会自动使用这个fixture，
        无需在测试函数中显式声明。

        @return str 设置信息
        """
        print("\n  自动设置执行")
        return "setup_done"

    def test_autouse_1(self):
        """
        测试自动使用fixture 1
        """
        # automatic_setup会被自动执行
        assert True

    def test_autouse_2(self):
        """
        测试自动使用fixture 2
        """
        assert True


class TestFixtureReturnVsYield:
    """
    Return和Yield对比测试类

    演示return和yield的区别。
    """

    @pytest.fixture
    def using_return(self):
        """
        使用return的fixture

        简单场景使用return即可。
        """
        data = {"method": "return", "value": 42}
        return data

    @pytest.fixture
    def using_yield(self):
        """
        使用yield的fixture

        需要清理资源时使用yield。
        """
        data = {"method": "yield", "value": 42}
        yield data  # 返回数据

        # 清理代码
        print("  cleanup code")

    def test_return_fixture(self, using_return):
        """
        测试return方式的fixture
        """
        assert using_return["value"] == 42

    def test_yield_fixture(self, using_yield):
        """
        测试yield方式的fixture
        """
        assert using_yield["method"] == "yield"
