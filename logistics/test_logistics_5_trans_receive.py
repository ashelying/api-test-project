# 5.物流公司接单
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
TRANS_RECEIVE_URL = BASE_URL + "/api/order/pc/order/trans/receive"

print("=" * 60)
print("  5️⃣ 物流公司接单")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：物流公司接单
print("\n📤 第二步：物流公司接单...")

# 使用之前的订单号
order_id = "DD20230713164416758"

receive_data = {
    "orderId": order_id,
    "times": int(time.time())
}

print(f"📤 请求参数: {receive_data}")

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(TRANS_RECEIVE_URL, json=receive_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 物流公司接单成功！")
else:
    print(f"\n❌ 接单失败: {result.get('message')}")