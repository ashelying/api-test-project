# 三、物流项目接口实战 创建物流项目的测试工具
import requests
import json

BASE_URL = "http://127.0.0.1:8787"


class LogisticsClient:
    """物流项目API客户端"""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.cookies = None

    def login(self):
        """登录获取Cookie"""
        login_url = self.base_url + "/da/user/login"
        data = {
            "user_name": "test01",
            "passwd": "admin123"
        }
        response = self.session.post(login_url, data=data)

        # 获取Cookie
        self.cookies = response.cookies
        print(f"✅ 登录成功，Cookie: {self.cookies}")
        return self.cookies

    def post(self, path, json_data=None, need_cookie=True):
        """发送POST请求"""
        url = self.base_url + path
        headers = {"Content-Type": "application/json;charset=UTF-8"}

        if need_cookie and self.cookies:
            # 将Cookie添加到请求中
            self.session.cookies.update(self.cookies)

        response = self.session.post(url, json=json_data, headers=headers)
        return response

    def get(self, path, params=None, need_cookie=True):
        """发送GET请求"""
        url = self.base_url + path
        headers = {}

        if need_cookie and self.cookies:
            self.session.cookies.update(self.cookies)

        response = self.session.get(url, params=params, headers=headers)
        return response

    def pretty_print(self, data):
        """美化打印JSON"""
        print(json.dumps(data, ensure_ascii=False, indent=2))