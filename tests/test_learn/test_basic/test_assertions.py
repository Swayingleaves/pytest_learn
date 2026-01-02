"""
断言示例

本文件详细介绍pytest中各种断言的使用方法。

什么是断言？
- 断言是测试的核心，用于验证实际结果是否符合预期
- pytest使用Python的assert关键字
- 当断言失败时，会抛出AssertionError

常用断言类型：
1. 相等断言：assert a == b
2. 不等断言：assert a != b
3. 包含断言：assert x in y
4. 真假断言：assert True / assert False
5. 异常断言：assert raises(Exception)
6. 近似断言：assert abs(a - b) < epsilon

@author Test Engineer
@date 2025/01/01
"""


class TestEqualityAssertions:
    """
    相等性断言测试类

    演示各种相等性断言的使用方法。
    """

    def test_equal_integers(self):
        """
        测试整数相等
        """
        a = 10
        b = 10
        # 断言两个值相等
        assert a == b

    def test_equal_strings(self):
        """
        测试字符串相等
        """
        str1 = "hello"
        str2 = "hello"
        assert str1 == str2

    def test_equal_lists(self):
        """
        测试列表相等

        列表内容完全相同时才相等
        """
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        assert list1 == list2

    def test_equal_dicts(self):
        """
        测试字典相等

        字典内容完全相同时才相等
        """
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 1, "b": 2}
        assert dict1 == dict2


class TestInequalityAssertions:
    """
    不等性断言测试类
    """

    def test_not_equal(self):
        """
        测试不等断言
        """
        assert 10 != 20
        assert "apple" != "banana"


class TestMembershipAssertions:
    """
    成员断言测试类

    验证某个元素是否在容器中。
    """

    def test_in_list(self):
        """
        测试元素在列表中
        """
        colors = ["red", "green", "blue"]
        assert "red" in colors
        assert "yellow" not in colors

    def test_in_string(self):
        """
        测试子串在字符串中
        """
        message = "Hello, World!"
        assert "Hello" in message
        assert "world" not in message  # 注意大小写

    def test_key_in_dict(self):
        """
        测试键在字典中
        """
        person = {"name": "Alice", "age": 30}
        assert "name" in person
        assert "email" not in person


class TestTypeAssertions:
    """
    类型断言测试类

    验证对象的类型。
    """

    def test_type_check(self):
        """
        测试对象类型
        """
        text = "hello"
        number = 42

        # 使用isinstance检查类型
        assert isinstance(text, str)
        assert isinstance(number, int)

    def test_multiple_types(self):
        """
        测试多种类型

        数字可以是int或float
        """
        int_val = 10
        float_val = 10.5

        assert isinstance(int_val, (int, float))
        assert isinstance(float_val, (int, float))


class TestBooleanAssertions:
    """
    布尔断言测试类
    """

    def test_true(self):
        """
        测试True条件
        """
        result = (10 > 5)
        assert result is True

    def test_false(self):
        """
        测试False条件
        """
        result = (10 < 5)
        assert result is False

    def test_none(self):
        """
        测试None值
        """
        empty_value = None
        assert empty_value is None

    def test_not_none(self):
        """
        测试非None值
        """
        value = "something"
        assert value is not None


class TestExceptionAssertions:
    """
    异常断言测试类

    演示如何使用pytest.raises捕获异常。
    """

    def test_exception_division_by_zero(self):
        """
        测试除零异常

        使用pytest.raises上下文管理器捕获异常。
        """
        import pytest

        # 定义会抛出异常的代码
        with pytest.raises(ZeroDivisionError):
            # 这行代码会抛出ZeroDivisionError
            result = 10 / 0

    def test_exception_index_error(self):
        """
        测试索引异常
        """
        import pytest

        with pytest.raises(IndexError):
            my_list = [1, 2, 3]
            _ = my_list[10]  # 索引超出范围

    def test_exception_with_message(self):
        """
        测试异常消息

        可以验证异常消息是否包含特定内容。
        """
        import pytest

        with pytest.raises(ValueError, match="invalid"):
            # 抛出包含"invalid"的ValueError
            int("not_a_number")


class TestApproximateAssertions:
    """
    近似断言测试类

    对于浮点数，由于精度问题，不适合使用精确相等。
    使用pytest.approx进行近似比较。
    """

    def test_float_approximate(self):
        """
        测试浮点数近似相等

        0.1 + 0.2 在计算机中可能不等于 0.3
        使用approx可以处理这种情况
        """
        import pytest

        result = 0.1 + 0.2
        # 使用approx进行近似比较
        assert result == pytest.approx(0.3, abs=1e-10)

    def test_list_approximate(self):
        """
        测试列表中浮点数的近似相等
        """
        import pytest

        result = [0.1 + 0.2, 0.2 + 0.3]
        expected = [0.3, 0.5]
        assert result == pytest.approx(expected, abs=1e-10)
