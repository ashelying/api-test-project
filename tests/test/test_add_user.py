# 2.新增用户接口
import requests

# 接口地址
BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
ADD_USER_URL = BASE_URL + "/char/user/addUser"

print("=" * 50)
print("📝 第一步：先登录获取 token")
print("=" * 50)

# ==================== 1. 先登录获取 token ====================
login_payload = {
    "user_name": "test01",
    "passwd": "admin123"
}

headers_form = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

login_response = requests.post(LOGIN_URL, data=login_payload, headers=headers_form)
login_result = login_response.json()

print(f"登录状态码: {login_response.status_code}")
print(f"登录响应: {login_result}")

# 提取 token
token = login_result.get("token")
print(f"✅ 获取到 token: {token}")

if not token:
    print("❌ 登录失败，无法继续")
    exit()

print("\n" + "=" * 50)
print("📝 第二步：调用新增用户接口")
print("=" * 50)

# ==================== 2. 新增用户 ====================
# 准备新增用户的参数
add_user_payload = {
    "username": "test_new_user",           # 用户名
    "password": "newpass123",              # 密码
    "role_id": "123456789",                # 角色ID
    "dates": "2026-12-31",                 # 有效期
    "phone": "18888888888",                # 手机号
    "token": token                         # 必须携带 token！
}

print("📤 请求参数:")
for key, value in add_user_payload.items():
    print(f"   {key}: {value}")

# 发送请求（仍然是表单格式）
response = requests.post(ADD_USER_URL, data=add_user_payload, headers=headers_form)

print("\n📥 响应结果:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 解析 JSON
if response.status_code == 200:
    result = response.json()
    print("\n===== 解析结果 =====")
    print(f"msg: {result.get('msg')}")
    print(f"msg_code: {result.get('msg_code')}")
    print(f"error_code: {result.get('error_code')}")
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")