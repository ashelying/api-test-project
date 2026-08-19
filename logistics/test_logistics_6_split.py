# 6.物流公司拆分订单
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
SPLIT_URL = BASE_URL + "/api/order/pc/logisticsOrder/handSplitOrder"

print("=" * 60)
print("  6️⃣ 物流公司拆分订单")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：拆分订单
print("\n📤 第二步：拆分订单...")

split_data = {
    "list": [
        {
            "itemId": "1679423155475509250",  # 物料ID
            "itemNum": 100,                   # 总数量
            "splitNum": 50                    # 拆分数量
        }
    ]
}

print(f"📤 请求参数:")
print(json.dumps(split_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(SPLIT_URL, json=split_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 订单拆分成功！")
    print(f"   📊 物流状态: {result.get('logisticsStatus')}")
else:
    print(f"\n❌ 拆分失败: {result.get('message')}")