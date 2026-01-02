"""
自定义标记示例

本文件介绍pytest的自定义标记功能。

什么是标记（Markers）？
- 标记是对测试用例进行分类的方式
- 使用@pytest.mark.标记名添加标记
- 可以在pytest.ini中注册自定义标记

常用内置标记：
- @pytest.mark.skip - 跳过测试
- @pytest.mark.skipif - 条件跳过测试
- @pytest.mark.xfail - 预期失败
- @pytest.mark.parametrize - 参数化测试

标记的用途：
1. 测试分类：按功能模块分类
2. 选择执行：只运行特定类型的测试
3. 条件执行：根据条件跳过测试
4. 标记依赖：标记有依赖关系的测试

@author Test Engineer
@date 2025/01/01
"""

import pytest


class TestSkipAndSkipif:
    """
    跳过测试示例类

    演示如何使用skip和skipif标记。
    """

    @pytest.mark.skip(reason="这个测试被跳过，因为功能还未实现")
    def test_skipped_function(self):
        """
        被跳过的测试

        使用@pytest.mark.skip跳过这个测试。
        运行时不会执行此测试。
        """
        assert False  # 不会执行到这里

    @pytest.mark.skipif(
        True,  # 可以使用条件表达式
        reason="条件为True时跳过"
    )
    def test_skipif_condition(self):
        """
        条件跳过的测试

        当skipif的条件为True时，测试会被跳过。
        """
        assert False


class TestXFail:
    """
    预期失败测试类

    演示如何使用xfail标记预期失败的测试。
    """

    @pytest.mark.xfail(reason="已知bug，修复后应通过")
    def test_expected_to_fail(self):
        """
        预期失败的测试

        使用@pytest.mark.xfail标记预期失败的测试。
        如果测试失败，报告为xfail（expectedly failed）
        如果测试通过，报告为xpass（unexpectedly passed）
        """
        # 这个测试预期会失败
        assert False

    @pytest.mark.xfail(reason="功能应该能正常工作")
    def test_expected_to_pass(self):
        """
        预期会通过的测试

        如果这个测试通过，报告为xpass。
        """
        assert True


class TestCustomMarkers:
    """
    自定义标记测试类

    演示如何使用自定义标记进行测试分类。
    """

    @pytest.mark.user
    def test_user_login(self):
        """
        用户模块测试 - 登录功能
        """
        assert True

    @pytest.mark.user
    def test_user_logout(self):
        """
        用户模块测试 - 登出功能
        """
        assert True

    @pytest.mark.order
    def test_order_create(self):
        """
        订单模块测试 - 创建订单
        """
        assert True

    @pytest.mark.order
    def test_order_cancel(self):
        """
        订单模块测试 - 取消订单
        """
        assert True

    @pytest.mark.payment
    def test_payment_process(self):
        """
        支付模块测试 - 处理支付
        """
        assert True


class TestMarksExecution:
    """
    标记执行示例类

    演示如何使用标记选择测试执行。
    """

    @pytest.mark.smoke
    def test_smoke_1(self):
        """
        冒烟测试1
        """
        assert True

    @pytest.mark.smoke
    def test_smoke_2(self):
        """
        冒烟测试2
        """
        assert True

    def test_normal_test(self):
        """
        普通测试
        """
        assert True


# ========================================
# 使用命令行运行特定标记的测试
# ========================================
#
# 运行所有smoke标记的测试：
# pytest -m smoke
#
# 运行smoke或user标记的测试：
# pytest -m "smoke or user"
#
# 运行smoke和user标记的测试：
# pytest -m "smoke and user"
#
# 排除smoke标记的测试：
# pytest -m "not smoke"
#
