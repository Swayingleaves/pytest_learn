import pytest
import requests
from src.utils.logger import LoggerUtil

# 创建日志实例
logger = LoggerUtil()

# 类名+数字编号，执行时会按数字顺序依次执行类里面的用例
class Test01CaseApi:
    # 定义一个类属性
    device_id = ''

    # 后续测试用例的前置条件方法
    @pytest.fixture(scope="class")
    def get_login_token(self):
        # 登录:获取Token, verify=False:忽略SSL证书验证
        response = requests.post("https://172.25.53.92/devapi/auth/login", json={
            "username": "zhengl",
            "password": "Zd@123"
        }, verify=False)
        # 接口实际返回结构
        '''
        {
            "code":200,
            "data":{
                "access_token":"e71f01c5-930f-469c-afd0-ead704538b29",
                "refresh_token":"f89245e3-0113-4874-95ec-147f9fb1d9c3",
                "scope":"app",
                "token_type":"bearer",
                "expires_in":86399
            },
            "msg":"成功",
            "status":true
        }
        '''
        # 返回登录成功后的token并打印
        token = response.json()["data"]["access_token"]
        print(f'获取到的token:{token}')
        # 记录token日志，会打印到控制台，同时存入日志文件--logger.py文件中配置
        logger.info(f'获取到的token:{token}')
        return token

    # 方法名+数字编号，执行时会按数字顺序依次执行用例方法
    # 传入前置条件方法,先获取到TOKEN,再执行下方用例
    def test_01_get_user_info(self, get_login_token):
        """
        测试用例1
        验证简单用户信息是否正确。
        """
        # 从fixture获取登录token
        token = get_login_token

        # 准备调取用户信息接口的入参
        # 接口url
        url = "https://172.25.53.92/devapi/system/v1/user/oneself"
        #  请求头
        headers = {
            "Cookie": f"Authorization={token}"
        }
        # 发送GET请求
        req = requests.get(url, headers=headers, verify=False)
        # 接口实际返回结构
        '''
        {
            "code":200,
            "data":{
                "account":"zhengl",
                "batchId":"",
                "createAccount":"admin",
                "createTime":"2025-04-28 11:07:12",
                "email":"",
                "expired":false,
                "expiryTime":"2029-01-01 00:00:00",
                "id":"1916690632790372353",
                "label":"",
                "name":"郑霖",
                "password":"",
                "phone":"15022223333",
                "roleIds":[
                    "1",
                    "1971131223284334593"
                ],
                "roleName":"管理员,开发人员专用",
                "sex":"2",
                "status":1,
                "updateTime":"2025-08-20 11:04:28",
                "userType":1
            },
            "msg":"成功",
            "status":true
        }
        '''
        # 验证简单的断言，code是否为200
        assert req.json()["code"] == 200
        # 验证返回的用户名是否为zhengl
        assert req.json()["data"]["account"] == "zhengl"


    def test_02_list_query(self, get_login_token):
        """
        测试用例2
        简单验证查询结果是否正确。
        """
        # 从fixture获取登录token
        token = get_login_token
        
        # 准备调取用户信息接口的入参
        # 接口url
        url = "https://172.25.53.92/devapi/terminal/V1/device/list"
        # 请求头
        headers = {
            "Cookie": f"Authorization={token}"
        }
        # 请求参数
        params = {
            "pageSize": 10,
            "pageNo": 1,
            "searchKeywords": "223344"
        }
        # 发送POST请求
        req = requests.post(url, headers=headers, json=params, verify=False)

        # 验证简单的断言,code是否为200
        assert req.json()["code"] == 200
        # 验证返回的结列表中第一条数据的编号是否包含"22"
        assert "22" in req.json()["data"]["list"][0]["deviceId"]
        # 将此用例的返回结果赋值给类属性
        Test01CaseApi.device_id =req.json()["data"]["list"][0]["deviceId"]
        # 验证返回的结列表中第一条数据的编号是否=223345
        assert req.json()["data"]["list"][0]["deviceId"] == '223345'

    def test_03_get_device_conf(self,get_login_token):
        """
        测试用例3
        简单验证查询结果是否正确。
        """
        # 从fixture获取登录token
        token = get_login_token
        
        # 准备调取用户信息接口的入参
        # 接口url
        url = "https://172.25.53.92/devapi/terminal/gatherLog/configStr"
        # 请求头
        headers = {
            "Cookie": f"Authorization={token}"
        }
        # 请求参数
        params = {
            # 可直接赋值传参
            # "deviceId": "112233"
            # 也可直接通过类属性使用前面用例的返回值作为入参
            "deviceId": Test01CaseApi.device_id
        }
        # 发送GET请求 等同于 https://172.25.53.92/devapi/terminal/gatherLog/configStr?deviceId=112233
        req = requests.get(url, headers=headers, params=params, verify=False)
        logger.info(f'获取到的设备配置信息:{req.json()}')
        # 验证简单的断言,code是否为200
        assert req.json()["code"] == 200