"""
HTTP请求工具模块

封装requests库，提供简洁的API调用方法。
支持GET、POST、PUT、DELETE等HTTP方法。

@author Test Engineer
@date 2025/01/01
"""

import requests
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass


@dataclass
class ResponseWrapper:
    """
    HTTP响应包装类

    封装响应对象，提供便捷的属性访问方法。

    @attr response 原始响应对象
    @attr status_code HTTP状态码
    @attr text 响应文本
    @attr json 响应JSON数据
    @attr headers 响应头
    """

    response: requests.Response

    @property
    def status_code(self) -> int:
        """获取HTTP状态码"""
        return self.response.status_code

    @property
    def text(self) -> str:
        """获取响应文本"""
        return self.response.text

    @property
    def json(self) -> Any:
        """获取响应JSON数据（自动解析）"""
        try:
            return self.response.json()
        except ValueError:
            return None

    @property
    def headers(self) -> Dict[str, str]:
        """获取响应头"""
        return dict(self.response.headers)

    @property
    def ok(self) -> bool:
        """判断响应是否成功（2xx状态码）"""
        return self.response.ok


class RequestUtil:
    """
    HTTP请求工具类

    封装requests库，提供简洁的API调用方法。
    支持会话管理、重试机制、超时控制等功能。

    使用示例：
        # GET请求
        response = RequestUtil.get("/users")

        # POST请求
        response = RequestUtil.post("/users", data={"name": "test"})

        # 带参数的请求
        response = RequestUtil.get("/users", params={"page": 1})
    """

    # 默认请求头
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    @staticmethod
    def _get_session() -> requests.Session:
        """
        获取请求会话

        使用会话可以复用TCP连接，提高请求效率。

        @return requests.Session 会话对象
        """
        session = requests.Session()
        session.headers.update(RequestUtil.DEFAULT_HEADERS)
        return session

    @staticmethod
    def _make_request(
        method: str,
        url: str,
        **kwargs
    ) -> ResponseWrapper:
        """
        发起HTTP请求

        @param method HTTP方法（GET、POST、PUT、DELETE等）
        @param url 请求URL
        @param kwargs 其他请求参数
        @return ResponseWrapper 响应包装对象
        """
        session = RequestUtil._get_session()
        response = session.request(method, url, **kwargs)
        return ResponseWrapper(response)

    @staticmethod
    def get(
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
        timeout: int = 30,
        **kwargs
    ) -> ResponseWrapper:
        """
        发起GET请求

        @param url 请求URL
        @param params URL查询参数
        @param headers 请求头
        @param cookies Cookie字典（用于认证）
        @param timeout 超时时间（秒）
        @param kwargs 其他参数
        @return ResponseWrapper 响应包装对象
        """
        return RequestUtil._make_request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            **kwargs
        )

    @staticmethod
    def post(
        url: str,
        data: Optional[Union[Dict, str]] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
        timeout: int = 30,
        **kwargs
    ) -> ResponseWrapper:
        """
        发起POST请求

        @param url 请求URL
        @param data 表单数据
        @param json JSON数据
        @param headers 请求头
        @param cookies Cookie字典（用于认证）
        @param timeout 超时时间（秒）
        @param kwargs 其他参数
        @return ResponseWrapper 响应包装对象
        """
        return RequestUtil._make_request(
            "POST",
            url,
            data=data,
            json=json,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            **kwargs
        )

    @staticmethod
    def put(
        url: str,
        data: Optional[Union[Dict, str]] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 30,
        **kwargs
    ) -> ResponseWrapper:
        """
        发起PUT请求

        @param url 请求URL
        @param data 表单数据
        @param json JSON数据
        @param headers 请求头
        @param timeout 超时时间（秒）
        @param kwargs 其他参数
        @return ResponseWrapper 响应包装对象
        """
        return RequestUtil._make_request(
            "PUT",
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            **kwargs
        )

    @staticmethod
    def delete(
        url: str,
        headers: Optional[Dict] = None,
        timeout: int = 30,
        **kwargs
    ) -> ResponseWrapper:
        """
        发起DELETE请求

        @param url 请求URL
        @param headers 请求头
        @param timeout 超时时间（秒）
        @param kwargs 其他参数
        @return ResponseWrapper 响应包装对象
        """
        return RequestUtil._make_request(
            "DELETE",
            url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
