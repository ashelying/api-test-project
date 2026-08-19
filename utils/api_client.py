# 创建统一API客户端
import requests
import json
from datetime import datetime


class APIClient:
    """统一的API请求客户端"""

    def __init__(self, base_url="http://127.0.0.1:8787"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.cookies = None

    def login(self, username="test01", password="admin123"):
        """登录获取认证信息"""
        url = f"{self.base_url}/da/user/login"
        data = {"user_name": username, "passwd": password}
        response = self.session.post(url, data=data)
        result = response.json()

        if result.get('msg_code') == 200:
            self.token = result.get('token')
            self.cookies = response.cookies
            print(f"✅ 登录成功，token: {self.token[:20] if self.token else 'None'}...")
            return True
        else:
            print(f"❌ 登录失败: {result}")
            return False

    def post_json(self, path, data, need_token=True, need_cookie=True):
        """发送POST JSON请求"""
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json;charset=UTF-8"}

        if need_token and self.token:
            data['token'] = self.token

        if need_cookie and self.cookies:
            self.session.cookies.update(self.cookies)

        response = self.session.post(url, json=data, headers=headers)
        return response

    def post_form(self, path, data, need_token=True, need_cookie=True):
        """发送POST表单请求"""
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        if need_token and self.token:
            data['token'] = self.token

        if need_cookie and self.cookies:
            self.session.cookies.update(self.cookies)

        response = self.session.post(url, data=data, headers=headers)
        return response

    def get(self, path, params=None, need_cookie=True):
        """发送GET请求"""
        url = f"{self.base_url}{path}"

        if need_cookie and self.cookies:
            self.session.cookies.update(self.cookies)

        response = self.session.get(url, params=params)
        return response


# 全局客户端实例
client = APIClient()