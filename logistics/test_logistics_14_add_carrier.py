# 15.添加承运商
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
ADD_CARRIER_URL = BASE_URL + "/api/user/pc/carrier/carrier/add"

print("=" * 60)
print("  1️⃣4️⃣ 添加承运商")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：添加承运商
print("\n📤 第二步：添加承运商...")

carrier_data = {
    "bizVehicleType": "2",
    "password": "202cb962ac59075b964b07152d234b70",  # MD5: 123
    "carrierName": "第三车队",
    "creditIdentifier": "91530425MA6Q6UM9XF",
    "belong": 1,
    "legalPerson": "王五",
    "bizLicenseValidUtil": "2027-07-30 00:00:00",
    "address": "北京市朝阳区",
    "transLicenseValidUtil": "2025-07-19 00:00:00",
    "bizScope": "运输",
    "transLicenseNum": "JH789DFG3578032",
    "carrierAlias": "三车队",
    "carrierType": "1",
    "contactName": "赵六",
    "contactTel": "13700000000",
    "contactEmail": "carrier3@example.com",
    "type": "2",
    "registeredFund": "500",
    "transportType": "BCZY001",
    "cooperateYears": "15",
    "provinceCode": "110000",
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(carrier_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(ADD_CARRIER_URL, json=carrier_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 添加承运商成功！")
else:
    print(f"\n❌ 添加失败: {result.get('message')}")