# 14.获取应付对账单详情及运费
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
BILL_DETAIL_URL = BASE_URL + "/api/order/pc/cost/payCost/page"

print("=" * 60)
print("  1️⃣3️⃣ 获取应付对账单详情及运费")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：获取对账单详情
print("\n📤 第二步：获取对账单详情...")

detail_data = {
    "current": 1,
    "size": 200,
    "dataType": 1,
    "costBillId": "DZ49696155887125490326557131668",
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(detail_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(BILL_DETAIL_URL, json=detail_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    data = result.get('data', {})
    records = data.get('records', [])
    print(f"\n✅ 获取对账单详情成功！")
    print(f"   📊 共 {len(records)} 条记录")
else:
    print(f"\n❌ 获取失败: {result.get('message')}")
