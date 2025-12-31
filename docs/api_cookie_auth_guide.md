# API Cookie认证测试指南

## 概述

本指南介绍如何在pytest API测试中使用Cookie进行认证。Cookie认证是Web应用中常见的认证方式，特别适用于需要保持会话状态的场景。

## 应用场景

- ✅ 需要登录后才能访问的API接口
- ✅ 需要保持用户会话状态
- ✅ 需要携带用户偏好设置
- ✅ 需要多层认证信息

## 实现方式

### 1. 扩展RequestUtil支持Cookie

已在 `src/utils/request_util.py` 中为GET和POST方法添加了`cookies`参数：

```python
@staticmethod
def get(
    url: str,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    cookies: Optional[Dict] = None,  # 新增
    timeout: int = 30,
    **kwargs
) -> ResponseWrapper:
    """发起GET请求"""
    return RequestUtil._make_request(
        "GET",
        url,
        params=params,
        headers=headers,
        cookies=cookies,  # 传入cookie
        timeout=timeout,
        **kwargs
    )
```

### 2. 使用Fixture提供认证Cookie

#### 方式1：静态Cookie（测试环境）

```python
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
    auth_token = "mock_auth_token_123456"

    # 构造cookie字典
    cookies = {
        "session_id": "abc123xyz",
        "auth_token": auth_token,
        "user_role": "admin"
    }

    return cookies
```

#### 方式2：动态Cookie（真实环境）

```python
@pytest.fixture
def dynamic_auth_token(self):
    """
    动态获取认证token的fixture

    演示如何在fixture中执行API调用来获取认证信息。
    这个fixture模拟了一个真实的登录流程。

    @return Dict 包含认证信息的字典
    """
    # 1. 调用登录API（模拟）
    login_url = settings.get_api_url("/login")
    login_data = {
        "username": "test_user",
        "password": "test_password"
    }

    # 实际使用时，应该调用真实的登录接口
    # from src.utils.request_util import RequestUtil
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
```

### 3. 在测试中使用Cookie

#### 测试1：带Cookie访问受保护的资源

```python
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
```

#### 测试2：带Cookie的POST请求

```python
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
```

#### 测试3：多Cookie组合

```python
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
```

#### 测试4：使用动态获取的Cookie

```python
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
```

## Cookie参数格式

### 单个Cookie

```python
cookies = {
    "session_id": "abc123"
}
```

### 多个Cookie

```python
cookies = {
    "session_id": "abc123",
    "auth_token": "xyz789",
    "user_role": "admin"
}
```

### Cookie属性设置

```python
from requests.cookies import RequestCookieJar

# 创建cookie jar
cookies = RequestCookieJar()

# 设置带属性的cookie
cookies.set(
    name="session_id",
    value="abc123",
    domain=".example.com",
    path="/",
    secure=True,
    httponly=True
)
```

## 最佳实践

### 1. 使用Fixture管理Cookie

将Cookie的获取和管理放在fixture中，实现：
- ✅ 统一的认证流程
- ✅ 方便的复用
- ✅ 清晰的生命周期管理

### 2. 区分测试环境和生产环境

```python
@pytest.fixture
def auth_cookies(settings):
    if settings.ENV == "test":
        # 测试环境：使用mock数据
        return {"mock_token": "test_value"}
    else:
        # 生产环境：调用真实登录
        return call_real_login_api()
```

### 3. Cookie过期处理

```python
@pytest.fixture
def auth_cookies():
    cookies = get_login_cookies()

    # 检查cookie是否过期
    if is_expired(cookies):
        cookies = refresh_cookies()

    return cookies
```

### 4. Session级别Cookie

如果所有测试都需要同一个Cookie，使用session级别fixture：

```python
@pytest.fixture(scope="session")
def global_auth_cookies():
    """
    全局认证Cookie fixture

    整个测试会话中只创建一次，
    提高测试效率。
    """
    return get_login_cookies()
```

## 运行测试

```bash
# 运行所有认证相关测试
pytest tests/test_api/test_api_demo.py::TestAPIAuthentication -v

# 运行单个测试
pytest tests/test_api/test_api_demo.py::TestAPIAuthentication::test_protected_resource_with_auth -v

# 使用-s参数查看详细输出
pytest tests/test_api/test_api_demo.py::TestAPIAuthentication -v -s
```

## 实际应用示例

### 完整的登录流程

```python
@pytest.fixture
def real_auth_cookies(settings):
    """
    真实的登录流程fixture

    演示完整的登录和cookie获取流程。
    """
    from src.utils.request_util import RequestUtil

    # 1. 调用登录API
    login_url = settings.get_api_url("/auth/login")
    login_data = {
        "username": "test_user",
        "password": "test_password"
    }

    response = RequestUtil.post(login_url, json=login_data)

    # 2. 验证登录成功
    assert response.status_code == 200
    assert "token" in response.json

    # 3. 提取认证信息
    auth_data = response.json
    token = auth_data["token"]
    user_id = auth_data["user"]["id"]
    expires = auth_data["expires_at"]

    # 4. 构造cookie
    cookies = {
        "auth_token": token,
        "user_id": str(user_id),
        "expires_at": str(expires)
    }

    return cookies
```

## 注意事项

1. **Cookie安全**：生产环境中，Cookie应该设置`secure`和`httponly`属性
2. **Cookie过期**：注意Cookie的过期时间，及时刷新
3. **Cookie作用域**：确保Cookie的domain和path设置正确
4. **敏感信息**：不要在Cookie中存储敏感信息（如密码）
5. **HTTPS**：使用HTTPS传输Cookie，防止中间人攻击

## 相关文档

- [API测试示例](../test_api/test_api_demo.py)
- [RequestUtil工具](../../src/utils/request_util.py)
- [全局配置](../../src/config/settings.py)
