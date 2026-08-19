# 3.删除用户接口、查询用户接口
import requests
import json

BASE_URL = "http://127.0.0.1:8787"

# ==================== 接口地址 ====================
LOGIN_URL = BASE_URL + "/da/user/login"
ADD_USER_URL = BASE_URL + "/char/user/addUser"
QUERY_USER_URL = BASE_URL + "/char/user/queryUser"
DELETE_USER_URL = BASE_URL + "/char/user/deleteUser"

# ==================== 请求头 ====================
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}


def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def login():
    """登录获取 token"""
    print_section("1️⃣ 登录获取 token")

    payload = {
        "user_name": "test01",
        "passwd": "admin123"
    }

    response = requests.post(LOGIN_URL, data=payload, headers=HEADERS)
    result = response.json()

    token = result.get("token")
    print(f"✅ 登录成功，token: {token}")
    return token


def add_user(token, username="test_user_001"):
    """新增用户"""
    print_section("2️⃣ 新增用户")

    payload = {
        "username": username,
        "password": "testpass123",
        "role_id": "123456789",
        "dates": "2026-12-31",
        "phone": "18888888888",
        "token": token
    }

    response = requests.post(ADD_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"📤 用户名: {username}")
    print(f"📥 响应: {result}")

    # 注意：我们的模拟服务没有返回 user_id，但系统会自动分配
    # 查询时需要知道 user_id，我们先尝试查询所有已知用户
    return result


def query_user(token, user_id):
    """查询用户"""
    print_section("3️⃣ 查询用户")

    payload = {
        "user_id": user_id,
        "token": token
    }

    response = requests.post(QUERY_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"📤 查询 user_id: {user_id}")
    print(f"📥 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    return result


def delete_user(token, user_id):
    """删除用户"""
    print_section("4️⃣ 删除用户")

    payload = {
        "user_id": user_id,
        "token": token
    }

    response = requests.post(DELETE_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"📤 删除 user_id: {user_id}")
    print(f"📥 响应: {result}")
    return result


# ==================== 主流程 ====================
if __name__ == "__main__":
    print("🚀 开始用户管理完整流程测试")

    # 1. 登录
    token = login()
    if not token:
        print("❌ 登录失败，终止测试")
        exit()

    # 2. 新增一个用户（用户名带时间戳，避免重复）
    import time

    username = f"test_user_{int(time.time())}"
    add_result = add_user(token, username)

    # 3. 查询用户（查询已存在的用户，如 1001）
    print("\n" + "=" * 60)
    print("  查询已存在的用户 (user_id=1001)")
    print("=" * 60)
    query_result = query_user(token, 1001)

    # 4. 删除用户（删除刚才新增的用户，需要知道 user_id）
    # 注意：由于我们的模拟服务没有返回 user_id，我们删除一个已知存在的用户
    print("\n" + "=" * 60)
    print("  删除一个已存在的用户 (user_id=1002)")
    print("=" * 60)
    delete_result = delete_user(token, 1002)

    # 5. 验证删除结果：再次查询已删除的用户
    print_section("5️⃣ 验证删除结果")
    verify_result = query_user(token, 1002)

    print("\n" + "=" * 60)
    print("  ✅ 测试完成！")
    print("=" * 60)