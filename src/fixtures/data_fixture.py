"""
测试数据Fixtures

提供测试数据相关的fixtures，包括：
- 简单测试数据
- 复杂嵌套数据
- 参数化测试数据

@author Test Engineer
@date 2025/01/01
"""

import pytest
from typing import List, Dict, Any


class DataFixtures:
    """
    测试数据fixtures类

    提供各种类型的测试数据，用于数据驱动测试。

    使用示例：
        @pytest.mark.parametrize("input,expected", test_add_data)
        def test_add(input, expected):
            pass
    """

    # ========================================
    # 加法测试数据
    # ========================================
    # 格式：(输入a, 输入b, 预期结果)
    test_add_data = [
        (1, 1, 2),
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ]

    # ========================================
    # 乘法测试数据
    # ========================================
    test_multiply_data = [
        (2, 3, 6),
        (0, 5, 0),
        (-2, 3, -6),
        (10, 10, 100),
    ]

    # ========================================
    # 用户数据列表
    # ========================================
    @pytest.fixture
    def users_list(self) -> List[Dict[str, Any]]:
        """
        返回用户列表数据

        @return List[Dict] 用户字典列表
        """
        return [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
        ]

    # ========================================
    # 配置数据
    # ========================================
    @pytest.fixture
    def app_config(self) -> Dict[str, Any]:
        """
        返回应用配置数据

        @return Dict 配置字典
        """
        return {
            "app_name": "Test App",
            "version": "1.0.0",
            "debug": True,
            "max_users": 100,
            "timeout": 30
        }


# 创建实例供直接导入使用
data_fixtures = DataFixtures()
