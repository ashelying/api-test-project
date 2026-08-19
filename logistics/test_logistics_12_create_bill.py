# 13.创建应付对帐单
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
CREATE_BILL_URL = BASE_URL + "/api/order/pc/cost/receiveCost/create/bill"

print("=" * 60)
print("  1️⃣2️⃣ 创建应付对账单")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：创建对账单
print("\n📤 第二步：创建应付对账单...")

bill_data = {
    "billName": "对账",
    "dataType": 2,
    "costBillStatus": 1,
    "dataValue": "DD202307050000004511",
    "ids": ["1676840753024704514"],
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(bill_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(CREATE_BILL_URL, json=bill_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 创建对账单成功！")
    print(f"   📋 对账单号: {result.get('reconciliationNum')}")
else:
    print(f"\n❌ 创建失败: {result.get('message')}")