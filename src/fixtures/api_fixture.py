"""
API测试Fixtures

提供API测试所需的fixtures，包括：
- 基础URL配置
- 请求会话管理
- 常用测试数据

@author Test Engineer
@date 2025/01/01
"""

import pytest
from typing import Dict, Any


class APIFixtures:
    """
    API测试fixtures类

    包含所有API测试相关的fixtures定义。
    使用类组织可以避免命名冲突，便于管理。

    使用示例：
        class TestUserAPI:
            def test_get_user(self, api_base_url, api_session):
                # 使用fixtures
                pass
    """

    @pytest.fixture
    def api_base_url(self, settings) -> str:
        """
        获取API基础URL

        @param settings 全局配置对象
        @return str API基础URL
        """
        return settings.BASE_URL

    @pytest.fixture
    def api_session(self) -> object:
        """
        获取API请求会话

        使用会话可以复用TCP连接，提高请求效率。

        @return Session 会话对象
        """
        import requests
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        return session

    @pytest.fixture
    def valid_user_data(self) -> Dict[str, Any]:
        """
        返回有效的用户测试数据

        用于创建用户、登录等测试场景。

        @return Dict 用户数据字典
        """
        return {
            "name": "Test User",
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }

    @pytest.fixture
    def test_post_data(self) -> Dict[str, Any]:
        """
        返回测试帖子数据

        用于创建帖子、更新帖子等测试场景。

        @return Dict 帖子数据字典
        """
        return {
            "title": "Test Title",
            "body": "This is the test body content.",
            "userId": 1
        }


# 创建实例供直接导入使用
api_fixtures = APIFixtures()
