"""
测试目录配置文件

此conftest.py文件只对tests目录下的测试生效。
可以在这里定义tests目录级别的fixtures和钩子。

@author Test Engineer
@date 2025/01/01
"""

import pytest


# ========================================
# 测试目录级别Fixtures
# ========================================

@pytest.fixture
def test_data_file(settings):
    """
    获取测试数据文件路径

    @param settings 全局配置对象
    @return Path 测试数据文件路径
    """
    return settings.TEST_DATA_FILE


@pytest.fixture
def temp_dir(tmp_path):
    """
    提供临时目录

    用于测试中需要临时文件或目录的场景。

    @param tmp_path pytest内置的临时目录fixture
    @return Path 临时目录路径
    """
    return tmp_path


# ========================================
# 常用测试数据Fixtures
# ========================================

@pytest.fixture
def sample_user():
    """
    返回示例用户数据

    @return Dict 用户数据字典
    """
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "username": "testuser"
    }


@pytest.fixture
def sample_post():
    """
    返回示例帖子数据

    @return Dict 帖子数据字典
    """
    return {
        "userId": 1,
        "id": 1,
        "title": "Test Post Title",
        "body": "This is the test post body content."
    }


# ========================================
# 标记相关配置
# ========================================

def pytest_collection_modifyitems(config, items):
    """
    测试用例收集修改钩子

    对测试用例进行排序和标记。

    @param config pytest配置对象
    @param items 收集到的测试用例列表
    """
    # 按文件名排序测试用例
    items.sort(key=lambda item: (item.fspath, item.name))
