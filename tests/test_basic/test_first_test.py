"""
第一个测试示例

本文件演示如何编写最基本的pytest测试用例。

什么是pytest？
- pytest是Python最流行的测试框架
- 简单易用，语法简洁
- 强大的fixture功能
- 丰富的插件生态

测试文件命名规范：
- 文件名必须以test_开头 或 以_test结尾
- 例如：test_*.py 或 *_test.py

测试函数命名规范：
- 函数名必须以test_开头
- 例如：test_add(), test_user_login()

@author Test Engineer
@date 2025/01/01
"""


class TestBasicConcepts:
    """
    测试基础概念类

    pytest中的测试类：
    - 类名以Test开头
    - 不需要继承任何类
    - pytest会自动发现并执行
    """

    def test_hello_world(self):
        """
        第一个测试函数

        最简单的测试：验证一个简单的条件。

        断言(Assertion)：
        - assert关键字用于检查条件
        - 如果条件为False，测试失败
        - 如果条件为True，测试通过
        """
        # 简单的断言：1 + 1 等于 2
        assert 1 + 1 == 2

    def test_string_operations(self):
        """
        测试字符串操作

        演示如何使用assert进行字符串断言。
        """
        # 创建字符串
        message = "Hello, Pytest!"

        # 断言字符串内容
        assert message == "Hello, Pytest!"

        # 断言字符串包含某个子串
        assert "Hello" in message

        # 断言字符串长度
        assert len(message) == 14

    def test_list_operations(self):
        """
        测试列表操作

        演示如何测试列表相关操作。
        """
        # 创建列表
        fruits = ["apple", "banana", "orange"]

        # 断言列表长度
        assert len(fruits) == 3

        # 断言列表包含某个元素
        assert "apple" in fruits

        # 断言列表第一个元素
        assert fruits[0] == "apple"

    def test_dictionary_operations(self):
        """
        测试字典操作

        演示如何测试字典相关操作。
        """
        # 创建字典
        user = {
            "name": "Alice",
            "age": 25,
            "city": "Beijing"
        }

        # 断言键存在
        assert "name" in user

        # 断言键值对
        assert user["name"] == "Alice"
        assert user.get("age") == 25

    def test_boolean_operations(self):
        """
        测试布尔值操作

        演示如何测试布尔条件。
        """
        # 布尔值断言
        assert True is True
        assert False is False

        # 条件断言
        x = 10
        assert x > 0
        assert x >= 10
        assert x < 100

        # None判断
        value = None
        assert value is None

        not_none_value = "test"
        assert not_none_value is not None


class TestMathOperations:
    """
    数学运算测试类

    演示更复杂的测试场景。
    """

    def test_addition(self):
        """
        测试加法运算
        """
        assert 5 + 3 == 8
        assert 0 + 0 == 0
        assert -1 + 1 == 0

    def test_subtraction(self):
        """
        测试减法运算
        """
        assert 10 - 5 == 5
        assert 5 - 10 == -5
        assert 0 - 0 == 0

    def test_multiplication(self):
        """
        测试乘法运算
        """
        assert 4 * 3 == 12
        assert 0 * 100 == 0
        assert (-2) * 3 == -6

    def test_division(self):
        """
        测试除法运算
        """
        assert 10 / 2 == 5
        assert 9 / 3 == 3

    def test_power(self):
        """
        测试幂运算
        """
        assert 2 ** 3 == 8
        assert 10 ** 2 == 100
