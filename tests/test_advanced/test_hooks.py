"""
Pytest钩子示例

本文件介绍pytest的钩子函数（Hooks）。

什么是钩子函数？
- 钩子函数是在测试生命周期特定时刻自动调用的函数
- 用于自定义pytest的行为
- 在conftest.py中定义

常见钩子函数：
1. pytest_configure - pytest配置初始化
2. pytest_collection_modifyitems - 修改收集的测试用例
3. pytest_runtest_setup - 测试执行前设置
4. pytest_runtest_teardown - 测试执行后清理
5. pytest_runtest_makereport - 生成测试报告
6. pytest_sessionstart - 会话开始
7. pytest_sessionend - 会话结束

@author Test Engineer
@date 2025/01/01
"""

import pytest


class TestHooksDemo:
    """
    钩子函数演示测试类

    这些测试用例用于演示钩子函数的作用。
    注意：钩子函数通常在conftest.py中定义，
    这里只是演示它们的效果。
    """

    def test_hook_example_1(self):
        """
        钩子函数测试示例1
        """
        assert True

    def test_hook_example_2(self):
        """
        钩子函数测试示例2
        """
        result = 2 + 2
        assert result == 4

    def test_hook_example_3(self):
        """
        钩子函数测试示例3
        """
        message = "hook test"
        assert "hook" in message


class TestMarkerHooks:
    """
    标记相关测试类

    演示如何使用pytest.mark和各种标记。
    """

    @pytest.mark.smoke
    def test_smoke_test(self):
        """
        冒烟测试标记

        @pytest.mark.smoke 用于标记冒烟测试
        冒烟测试是最基本的测试，确保主要功能正常
        """
        assert True

    @pytest.mark.api
    def test_api_test(self):
        """
        API测试标记

        @pytest.mark.api 用于标记API测试
        """
        assert True

    @pytest.mark.ui
    def test_ui_test(self):
        """
        UI测试标记

        @pytest.mark.ui 用于标记UI测试
        """
        assert True

    @pytest.mark.regression
    def test_regression_test(self):
        """
        回归测试标记

        @pytest.mark.regression 用于标记回归测试
        回归测试确保新代码没有破坏现有功能
        """
        assert True

    @pytest.mark.slow
    @pytest.mark.api
    def test_slow_api_test(self):
        """
        多标记测试

        一个测试可以同时有多个标记
        这个测试同时标记为slow和api
        """
        assert True
