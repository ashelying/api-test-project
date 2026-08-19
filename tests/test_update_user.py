# 4.修改用户接口
import requests
import json

BASE_URL = "http://127.0.0.1:8787"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

# ==================== 接口地址 ====================
LOGIN_URL = BASE_URL + "/da/user/login"
ADD_USER_URL = BASE_URL + "/char/user/addUser"
QUERY_USER_URL = BASE_URL + "/char/user/queryUser"
UPDATE_USER_URL = BASE_URL + "/char/user/updateUser"


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


def add_user(token, username, phone):
    """新增用户"""
    print_section("2️⃣ 新增用户（准备修改）")

    payload = {
        "username": username,
        "password": "old_password_123",
        "role_id": "123456789",
        "dates": "2026-12-31",
        "phone": phone,
        "token": token
    }

    response = requests.post(ADD_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"📤 用户名: {username}")
    print(f"📤 手机号: {phone}")
    print(f"📥 响应: {result}")

    if result.get("msg_code") == 200:
        print("✅ 用户创建成功！")
    return result


def query_user(token, user_id):
    """查询用户"""
    print_section("3️⃣ 修改前查询用户信息")

    payload = {
        "user_id": user_id,
        "token": token
    }

    response = requests.post(QUERY_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"📤 查询 user_id: {user_id}")
    print(f"📥 修改前数据:")
    if result.get("data"):
        for key, value in result["data"].items():
            print(f"     {key}: {value}")
    else:
        print(f"     {result.get('msg')}")

    return result


def update_user(token, user_id, new_data):
    """修改用户"""
    print_section("4️⃣ 修改用户信息")

    payload = {
        "user_id": user_id,
        "username": new_data.get("username"),
        "password": new_data.get("password"),
        "role_id": new_data.get("role_id"),
        "dates": new_data.get("dates"),
        "phone": new_data.get("phone"),
        "token": token
    }

    print(f"📤 修改 user_id: {user_id}")
    print("📤 修改内容:")
    for key, value in new_data.items():
        print(f"     {key}: {value}")

    response = requests.post(UPDATE_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"\n📥 响应: {result}")

    if result.get("msg_code") == 200:
        print("✅ 修改成功！")
    return result


def verify_update(token, user_id):
    """验证修改结果"""
    print_section("5️⃣ 验证修改结果")

    payload = {
        "user_id": user_id,
        "token": token
    }

    response = requests.post(QUERY_USER_URL, data=payload, headers=HEADERS)
    result = response.json()

    print(f"📤 再次查询 user_id: {user_id}")
    print("📥 修改后数据:")
    if result.get("data"):
        for key, value in result["data"].items():
            print(f"     {key}: {value}")
    else:
        print(f"     {result.get('msg')}")

    return result


# ==================== 主流程 ====================
if __name__ == "__main__":
    print("🚀 开始修改用户接口测试")

    # 1. 登录
    token = login()
    if not token:
        print("❌ 登录失败，终止测试")
        exit()

    # 2. 新增一个用户（作为修改对象）
    import time

    username = f"update_user_{int(time.time())}"
    phone = f"188{int(time.time()) % 100000000:08d}"
    add_result = add_user(token, username, phone)

    if add_result.get("msg_code") != 200:
        print("❌ 新增用户失败，无法继续")
        exit()

    # 注意：我们的模拟服务没有返回 user_id，所以用 1003（第一个新增的用户）
    # 实际项目中，新增接口会返回 user_id
    user_id = 1003
    print(f"\n💡 本次测试使用 user_id: {user_id}")

    # 3. 修改前查询
    query_before = query_user(token, user_id)

    # 4. 修改用户（修改所有字段）
    new_user_data = {
        "username": "updated_username",
        "password": "new_password_456",
        "role_id": "987654321",
        "dates": "2027-06-30",
        "phone": "13999999999"
    }

    update_result = update_user(token, user_id, new_user_data)

    # 5. 验证修改结果
    query_after = verify_update(token, user_id)

    print("\n" + "=" * 60)
    print("  ✅ 修改用户测试完成！")
    print("=" * 60)