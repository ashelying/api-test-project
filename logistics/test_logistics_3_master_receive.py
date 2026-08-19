# 3.集团接收货主订单
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
MASTER_RECEIVE_URL = BASE_URL + "/api/order/pc/order/master/receive"

print("=" * 60)
print("  3️⃣ 集团接收货主订单")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功，Cookie: {cookies}")

# 第二步：集团接收订单
print("\n📤 第二步：集团接收订单...")

# 使用上一个接口返回的订单号
order_id = "DD20230713164416758"  # 从上一个测试获取

receive_data = {
    "orderId": order_id,
    "times": int(time.time())
}

print(f"📤 请求参数: {receive_data}")

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(MASTER_RECEIVE_URL, json=receive_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 集团接收订单成功！")
else:
    print(f"\n❌ 接收失败: {result.get('message')}")