# 测试异常情况
import requests

BASE_URL = "http://127.0.0.1:8787"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

# 先登录获取 token
login_response = requests.post(
    BASE_URL + "/da/user/login",
    data={"user_name": "test01", "passwd": "admin123"},
    headers=HEADERS
)
token = login_response.json().get("token")

print("=" * 60)
print("  🧪 异常情况测试")
print("=" * 60)

# ==================== 测试1：查询不存在的用户 ====================
print("\n【测试1】查询不存在的用户 (user_id=9999)")
response = requests.post(
    BASE_URL + "/char/user/queryUser",
    data={"user_id": 9999, "token": token},
    headers=HEADERS
)
print(f"响应: {response.json()}")

# ==================== 测试2：删除不存在的用户 ====================
print("\n【测试2】删除不存在的用户 (user_id=9999)")
response = requests.post(
    BASE_URL + "/char/user/deleteUser",
    data={"user_id": 9999, "token": token},
    headers=HEADERS
)
print(f"响应: {response.json()}")

# ==================== 测试3：不携带 token 查询 ====================
print("\n【测试3】不携带 token 查询用户")
response = requests.post(
    BASE_URL + "/char/user/queryUser",
    data={"user_id": 1001},  # 没有 token
    headers=HEADERS
)
print(f"响应: {response.json()}")

# ==================== 测试4：使用错误的 token ====================
print("\n【测试4】使用错误的 token 查询用户")
response = requests.post(
    BASE_URL + "/char/user/queryUser",
    data={"user_id": 1001, "token": "wrong_token"},
    headers=HEADERS
)
print(f"响应: {response.json()}")