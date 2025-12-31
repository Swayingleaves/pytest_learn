"""
钩子函数示例测试

本文件演示pytest钩子函数的实际效果。
运行此文件时，conftest.py中定义的钩子函数会被触发。

@author Test Engineer
@date 2025/01/01
"""

import pytest


class TestHookBasic:
    """
    基础钩子测试类

    演示最基本的钩子函数效果。
    """

    def test_hook_demo_1(self):
        """
        钩子演示测试1

        运行此测试时，会触发以下钩子：
        - pytest_runtest_setup: 测试开始前
        - pytest_runtest_makereport: 生成测试报告
        - pytest_runtest_teardown: 测试完成后
        """
        assert 1 + 1 == 2

    def test_hook_demo_2(self):
        """
        钩子演示测试2

        观察控制台输出，可以看到钩子函数的执行顺序。
        """
        message = "pytest hooks"
        assert "hooks" in message


class TestHookMarkers:
    """
    标记相关钩子测试类

    演示钩子函数如何处理测试标记。
    """

    @pytest.mark.smoke
    def test_with_smoke_marker(self):
        """
        冒烟测试

        pytest_collection_modifyitems 钩子会给此测试添加 fast 标记
        """
        assert True

    @pytest.mark.api
    @pytest.mark.slow
    def test_slow_api_test(self):
        """
        慢速API测试

        pytest_runtest_setup 钩子会检测到 slow 标记并打印警告
        """
        assert True

    @pytest.mark.regression
    def test_regression_marker(self):
        """
        回归测试

        pytest_configure 钩子会注册此自定义标记
        """
        assert True


class TestHookResults:
    """
    测试结果相关钩子测试类

    演示不同测试结果如何触发钩子函数。
    """

    def test_passing_test(self):
        """
        通过的测试

        pytest_runtest_makereport 会记录通过状态
        """
        assert True

    def test_failing_test(self):
        """
        失败的测试

        pytest_runtest_makereport 会记录失败信息
        """
        # 这个测试会失败，用于演示失败时的钩子行为
        assert False

    @pytest.mark.skip(reason="演示跳过钩子")
    def test_skipped_test(self):
        """
        跳过的测试

        pytest_runtest_makereport 会记录跳过信息
        """
        assert True


class TestHookWithFixtures:
    """
    结合Fixture的钩子测试类

    演示钩子和fixture如何协同工作。
    """

    @pytest.fixture
    def sample_data(self):
        """
        测试数据fixture
        """
        return {"name": "hook_test", "value": 100}

    def test_with_fixture(self, sample_data):
        """
        使用fixture的测试

        钩子函数在fixture设置和清理时都会执行
        """
        assert sample_data["value"] == 100
        assert sample_data["name"] == "hook_test"


def test_hook_demo_function():
    """
    独立测试函数（不在类中）

    演示钩子函数对独立函数同样有效
    """
    result = [1, 2, 3]
    assert len(result) == 3
    assert 2 in result
