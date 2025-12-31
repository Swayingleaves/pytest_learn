"""
API测试示例

本文件演示如何使用pytest进行API接口测试。

API测试要点：
1. 发送HTTP请求
2. 验证响应状态码
3. 验证响应数据
4. 处理异常情况

使用的工具：
- requests库：发送HTTP请求
- ResponseWrapper：封装响应对象

@author Test Engineer
@date 2025/01/01
"""

import pytest


class TestAPIUsers:
    """
    用户API测试类

    使用https://jsonplaceholder.typicode.com作为测试API
    这是一个免费的假API服务
    """

    def test_get_users_list(self, settings):
        """
        测试获取用户列表

        使用GET请求获取所有用户。
        """
        from src.utils.request_util import RequestUtil

        # 发送GET请求
        url = settings.get_api_url("/users")
        response = RequestUtil.get(url)

        # 验证响应状态码
        assert response.status_code == 200

        # 验证响应数据是列表
        assert isinstance(response.json, list)

        # 验证有用户数据
        assert len(response.json) > 0

        # 验证用户数据结构
        first_user = response.json[0]
        assert "id" in first_user
        assert "name" in first_user
        assert "email" in first_user

    def test_get_single_user(self, settings):
        """
        测试获取单个用户

        使用GET请求获取指定用户。
        """
        from src.utils.request_util import RequestUtil

        # 获取ID为1的用户
        url = settings.get_api_url("/users/1")
        response = RequestUtil.get(url)

        # 验证响应状态码
        assert response.status_code == 200

        # 验证返回的用户ID
        assert response.json["id"] == 1

    def test_get_nonexistent_user(self, settings):
        """
        测试获取不存在的用户

        验证API对无效请求的响应。
        """
        from src.utils.request_util import RequestUtil

        # 尝试获取不存在的用户
        url = settings.get_api_url("/users/9999")
        response = RequestUtil.get(url)

        # 验证404状态码
        assert response.status_code == 404


class TestAPIPosts:
    """
    帖子API测试类
    """

    def test_get_posts_list(self, settings):
        """
        测试获取帖子列表
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/posts")
        response = RequestUtil.get(url)

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) > 0

    def test_get_single_post(self, settings):
        """
        测试获取单个帖子
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/posts/1")
        response = RequestUtil.get(url)

        assert response.status_code == 200
        assert response.json["id"] == 1
        assert "title" in response.json
        assert "body" in response.json

    def test_create_post(self, settings):
        """
        测试创建帖子

        使用POST请求创建新帖子。
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/posts")

        # 帖子数据
        post_data = {
            "title": "Test Title",
            "body": "Test body content",
            "userId": 1
        }

        # 发送POST请求
        response = RequestUtil.post(url, json=post_data)

        # 验证201 Created状态码
        assert response.status_code == 201

        # 验证响应包含创建的数据
        assert response.json["title"] == post_data["title"]
        assert response.json["body"] == post_data["body"]
        assert response.json["userId"] == post_data["userId"]


class TestAPIValidation:
    """
    API响应验证测试类

    演示各种响应验证方法。
    """

    def test_response_headers(self, settings):
        """
        测试响应头验证
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/users/1")
        response = RequestUtil.get(url)

        # 验证Content-Type头
        assert "Content-Type" in response.headers
        assert "application/json" in response.headers["Content-Type"]

    def test_response_time(self, settings):
        """
        测试响应时间

        验证API响应速度是否在可接受范围内。
        """
        from src.utils.request_util import RequestUtil

        import time

        url = settings.get_api_url("/users")
        start_time = time.time()

        response = RequestUtil.get(url)

        end_time = time.time()
        response_time = end_time - start_time

        # 验证响应时间小于1秒
        assert response_time < 1.0
        assert response.status_code == 200


class TestAPIAuthentication:
    """
    API认证测试类

    演示如何使用Cookie进行API认证。
    场景：模拟需要登录后才能访问的API接口。
    """

    @pytest.fixture
    def auth_cookies(self):
        """
        模拟认证Cookie的fixture

        在实际项目中，这个fixture会：
        1. 调用登录API获取token
        2. 将token转换为cookie格式
        3. 返回cookie字典供测试使用

        @return Dict 认证Cookie字典
        """
        # 模拟从登录API获取的认证token
        # 实际场景中，这里应该调用登录API
        auth_token = "mock_auth_token_123456"

        # 构造cookie字典
        cookies = {
            "session_id": "abc123xyz",
            "auth_token": auth_token,
            "user_role": "admin"
        }

        return cookies

    def test_protected_resource_with_auth(self, settings, auth_cookies):
        """
        测试带Cookie访问受保护的资源

        使用auth_cookies fixture获取认证信息，
        然后在请求中携带cookie访问受保护的API。
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/users")

        # 带cookie发送GET请求
        response = RequestUtil.get(
            url,
            cookies=auth_cookies  # 传入认证cookie
        )

        # 验证请求成功
        assert response.status_code == 200

    def test_protected_post_with_auth(self, settings, auth_cookies):
        """
        测试带Cookie的POST请求

        演示需要认证的POST请求如何携带cookie。
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/posts")

        post_data = {
            "title": "需要认证的帖子",
            "body": "只有登录用户才能发布",
            "userId": 1
        }

        # 带cookie发送POST请求
        response = RequestUtil.post(
            url,
            json=post_data,
            cookies=auth_cookies  # 传入认证cookie
        )

        # 验证请求成功
        assert response.status_code == 201

    def test_multiple_cookies_scenario(self, settings, auth_cookies):
        """
        测试多Cookie组合场景

        演示同时携带多个cookie进行请求。
        """
        from src.utils.request_util import RequestUtil

        # 组合多个cookie
        combined_cookies = {
            **auth_cookies,  # 认证cookie
            "preference": "dark_mode",  # 用户偏好
            "language": "zh-CN"  # 语言设置
        }

        url = settings.get_api_url("/users")
        response = RequestUtil.get(
            url,
            cookies=combined_cookies
        )

        # 验证请求成功
        assert response.status_code == 200

    @pytest.fixture
    def dynamic_auth_token(self):
        """
        动态获取认证token的fixture

        演示如何在fixture中执行API调用来获取认证信息。
        这个fixture模拟了一个真实的登录流程。

        @return Dict 包含认证信息的字典
        """
        # 1. 调用登录API（模拟）
        # 注意：实际场景中应该调用真实的登录接口
        # from src.utils.request_util import RequestUtil
        # login_url = settings.get_api_url("/login")
        # login_data = {"username": "test_user", "password": "test_password"}
        # login_response = RequestUtil.post(login_url, json=login_data)

        # 模拟登录成功返回的token
        auth_info = {
            "token": "generated_token_" + str(hash("test_user")),
            "expires_in": 3600,
            "user_id": 999
        }

        # 2. 构造cookie
        cookies = {
            "access_token": auth_info["token"],
            "user_id": str(auth_info["user_id"])
        }

        return cookies

    def test_with_dynamic_auth(self, settings, dynamic_auth_token):
        """
        使用动态获取的认证token进行测试

        演示如何使用fixture动态获取认证信息。
        """
        from src.utils.request_util import RequestUtil

        url = settings.get_api_url("/posts")

        # 使用fixture中动态获取的cookie
        response = RequestUtil.get(
            url,
            cookies=dynamic_auth_token
        )

        # 验证请求成功
        assert response.status_code == 200
