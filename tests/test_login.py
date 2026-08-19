import pytest
from utils.api_client import client, APIClient


class TestLogin:
    """登录接口测试"""

    def test_login_success(self):
        """测试登录成功"""
        result = client.login("test01", "admin123")
        assert result == True
        assert client.token is not None

    def test_login_fail(self):
        """测试登录失败"""
        # 创建新客户端，避免影响其他测试
        temp_client = APIClient()
        result = temp_client.login("wrong_user", "wrong_pass")
        assert result == False