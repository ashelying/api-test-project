# 16.获取承运商列表
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
CARRIER_LIST_URL = BASE_URL + "/api/user/pc/carrier/cys/findPage"

print("=" * 60)
print("  1️⃣5️⃣ 获取承运商列表")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：获取承运商列表
print("\n📤 第二步：获取承运商列表...")

list_data = {
    "current": 1,
    "size": 20,
    "status": "1",
    "timeType": "0",
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(list_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(CARRIER_LIST_URL, json=list_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    data = result.get('data', {})
    records = data.get('records', [])
    print(f"\n✅ 获取承运商列表成功！")
    print(f"   📊 共 {len(records)} 个承运商")
    for i, carrier in enumerate(records, 1):
        print(f"   {i}. {carrier.get('carrierName')} - {carrier.get('contactTel')}")
else:
    print(f"\n❌ 获取失败: {result.get('message')}")