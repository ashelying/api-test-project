#1.用户登录接口
import requests

# 接口地址
BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"

# 请求参数（根据文档示例）
payload = {
    "user_name": "test01",
    "passwd": "admin123"
}

# 请求头（表单提交）
headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

# 发送POST请求
response = requests.post(LOGIN_URL, data=payload, headers=headers)

# 打印响应结果
print("状态码:", response.status_code)
print("响应内容:", response.text)

# 如果返回JSON，可以解析
if response.status_code == 200:
    result = response.json()
    print("\n===== 解析结果 =====")
    print("msg:", result.get("msg"))
    print("msg_code:", result.get("msg_code"))
    print("error_code:", result.get("error_code"))
    print("token:", result.get("token"))