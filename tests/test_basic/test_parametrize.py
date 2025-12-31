"""
参数化测试示例

本文件演示pytest的参数化测试功能。

什么是参数化测试？
- 参数化测试允许使用不同的数据运行同一个测试
- 使用@pytest.mark.parametrize装饰器
- 大大减少重复代码，提高测试覆盖率

参数化测试的优点：
1. 代码复用：一次编写，多次运行
2. 数据驱动：测试逻辑与测试数据分离
3. 易维护：修改测试逻辑只需改一处

@author Test Engineer
@date 2025/01/01
"""

import pytest


class TestParametrizeBasic:
    """
    基础参数化测试类

    使用@pytest.mark.parametrize装饰器定义测试数据。
    """

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (1, 1, 2),      # 正数加法
            (0, 0, 0),      # 零加法
            (-1, 1, 0),     # 负数加法
            (100, 200, 300), # 大数加法
        ]
    )
    def test_add(self, a, b, expected):
        """
        测试加法运算

        @param a 第一个加数
        @param b 第二个加数
        @param expected 预期结果
        """
        assert a + b == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (3, 2, 6),       # 3 * 2 = 6
            (0, 5, 0),       # 零乘法
            (-2, 3, -6),     # 负数乘法
            (10, 10, 100),   # 10 * 10 = 100
        ]
    )
    def test_multiply(self, a, b, expected):
        """
        测试乘法运算
        """
        assert a * b == expected


class TestParametrizeWithIds:
    """
    带自定义ID的参数化测试

    可以为每组数据指定自定义ID，使测试输出更易读。
    """

    @pytest.mark.parametrize(
        "input,expected",
        [
            ("hello", "HELLO"),  # 测试小写转大写
            ("World", "WORLD"),
            ("PyTest", "PYTEST"),
        ],
        ids=["lower_to_upper", "mixed_to_upper", "proper_to_upper"]
    )
    def test_upper(self, input, expected):
        """
        测试字符串大写转换
        """
        assert input.upper() == expected


class TestParametrizeStrings:
    """
    字符串参数化测试
    """

    @pytest.mark.parametrize(
        "text,substring,expected",
        [
            ("hello world", "hello", True),    # 包含子串
            ("hello world", "python", False),  # 不包含子串
            ("pytest is great", "pytest", True),
            ("", "test", False),               # 空字符串
        ]
    )
    def test_string_contains(self, text, substring, expected):
        """
        测试字符串包含关系

        @param text 主字符串
        @param substring 要查找的子串
        @param expected 预期结果（是否包含）
        """
        result = substring in text
        assert result == expected


class TestParametrizeAPI:
    """
    API测试参数化示例

    演示如何将API测试数据参数化。
    """

    @pytest.mark.parametrize(
        "status_code,expected_message",
        [
            (200, "OK"),      # 成功响应
            (404, "Not Found"),  # 页面未找到
            (500, "Server Error"),  # 服务器错误
        ],
        ids=["success", "not_found", "server_error"]
    )
    def test_http_status_codes(self, status_code, expected_message):
        """
        测试HTTP状态码

        验证不同状态码和对应的消息。
        注意：这里只是验证映射关系，实际测试需要发送真实请求。
        """
        # 模拟状态码和消息的映射
        status_messages = {
            200: "OK",
            404: "Not Found",
            500: "Server Error"
        }

        assert status_messages.get(status_code) == expected_message


class TestParametrizeEdgeCases:
    """
    边界值参数化测试

    测试各种边界情况。
    """

    @pytest.mark.parametrize(
        "value,expected_type",
        [
            (0, int),          # 零
            (1, int),          # 正整数
            (-1, int),         # 负整数
            (3.14, float),     # 浮点数
            (True, bool),      # 布尔值True
            (False, bool),     # 布尔值False
            ("", str),         # 空字符串
            ([], list),        # 空列表
            ({}, dict),        # 空字典
            (None, type(None)), # None值
        ],
        ids=[
            "zero", "positive", "negative",
            "float", "true", "false",
            "empty_string", "empty_list",
            "empty_dict", "none"
        ]
    )
    def test_type_detection(self, value, expected_type):
        """
        测试类型检测

        验证不同值的类型是否符合预期。
        """
        assert isinstance(value, expected_type)


class TestMultipleParametrize:
    """
    多参数化标记组合

    可以同时使用多个parametrize装饰器，
    会自动组合所有参数组合。
    """

    @pytest.mark.parametrize("x", [1, 2, 3])
    @pytest.mark.parametrize("y", [10, 20])
    def test_combined_params(self, x, y):
        """
        测试组合参数

        x有3个值，y有2个值，总共会运行6次测试。

        参数组合：
        - x=1, y=10
        - x=1, y=20
        - x=2, y=10
        - x=2, y=20
        - x=3, y=10
        - x=3, y=20
        """
        # 计算结果
        result = x + y

        # 验证结果
        assert isinstance(result, int)
        assert result > 0
