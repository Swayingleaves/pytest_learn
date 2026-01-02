import pytest
import requests

class TestCase1:

    @pytest.fixture(scope="class")
    def get_login_token(self):
        
        # 登录 获取Token
        # response = requests.post("https://jsonplaceholder.typicode.com/login", json={
        #     "username": "testuser",
        #     "password": "testpassword"
        # })

        # # 验证返回状态码是否为200
        # assert response.status_code == 200

        # # 验证返回JSON数据是否包含token字段
        # assert "token" in response.json()

        # return response.json()["token"]

        # 假设登录成功后返回的token为固定值
        return "testtoken123"

    def test_case1(self, get_login_token):
        """
        测试用例1

        验证简单的断言是否为True。
        """
        # 从fixture获取登录token
        token = get_login_token
        
        # 验证简单的断言是否为True
        assert True

    def test_api(self, get_login_token):
        """
        测试API接口

        验证API返回的状态码是否为200。
        """
        # 1、从fixture获取登录token
        token = get_login_token

        # 2、调用API接口（假设为POST /login） token 设置在headers中 或者 cookie里
        headers = {
            "Authorization": f"Bearer {token}"
        }
        #==================POST请求==================
        # 3、构造请求参数
        query_params = {
            "page": 1,
            "limit": 10
        }
        # 4.1 发送POST请求 如果请求参数是body 则需要设置json参数
        response = requests.post("https://jsonplaceholder.typicode.com/userPage", json=query_params, headers=headers)

        # 验证返回状态码是否为200
        assert response.status_code == 200

        # 验证返回JSON数据是否包含token字段
        assert "data" in response.json()

        #==================GET请求直接在url中传递参数==================
        # 4.2 发送GET请求直接在url中传递参数
        response_get = requests.get("https://jsonplaceholder.typicode.com/posts/1", headers=headers)

        # 验证get请求返回状态码是否为200
        assert response_get.status_code == 200

        # 验证get请求返回JSON数据是否包含userId字段
        assert "title" in response_get.json()

        #============GET请求参数传递方式==================
        # 4.3 发送GET请求参数传递方式
        get_params = {
            "id": 1
        }
        response_get = requests.get("https://jsonplaceholder.typicode.com/posts/detail", headers=headers, params=get_params)

        # 验证get请求返回状态码是否为200
        assert response_get.status_code == 200

        # 验证get请求返回JSON数据是否包含userId字段
        assert "title" in response_get.json()