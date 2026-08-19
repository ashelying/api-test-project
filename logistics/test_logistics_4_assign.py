# 4.集团分配订单给物流公司
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
ASSIGN_URL = BASE_URL + "/api/order/pc/order/assign"

print("=" * 60)
print("  4️⃣ 集团分配订单给物流公司")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：分配订单
print("\n📤 第二步：分配订单给物流公司...")

# 使用之前的订单号
order_id = "DD20230713164416758"
org_id = "4140913758110176843"  # 物流公司ID

assign_data = {
    "orderId": order_id,
    "orgId": org_id,
    "times": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(assign_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(ASSIGN_URL, json=assign_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 订单分配成功！")
else:
    print(f"\n❌ 分配失败: {result.get('message')}")