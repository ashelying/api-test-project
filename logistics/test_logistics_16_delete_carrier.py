# 17.删除承运商
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
DELETE_CARRIER_URL = BASE_URL + "/api/user/pc/carrier/carrier/delete"

print("=" * 60)
print("  1️⃣6️⃣ 删除承运商")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：删除承运商
print("\n📤 第二步：删除承运商...")

delete_data = {
    "carrierId": "1666722201231867906",
    "current": 1,
    "size": 20,
    "status": "1",
    "timeType": "0",
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(delete_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(DELETE_CARRIER_URL, json=delete_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 删除承运商成功！")
else:
    print(f"\n❌ 删除失败: {result.get('message')}")