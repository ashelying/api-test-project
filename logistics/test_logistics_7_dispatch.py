# 7.调度派车
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
DISPATCH_URL = BASE_URL + "/api/order/pc/logisticsOrder/handCapacityDispatch"

print("=" * 60)
print("  7️⃣ 调度派车")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：调度派车
print("\n📤 第二步：调度派车...")

dispatch_data = {
    "logisticsOrderId": "WL2023071411141721972",
    "itemId": "16794264872418631691",
    "dispatchNum": 50,
    "carrierId": "1661558222301904898",
    "carrierName": "长凡贸易有限公司",
    "driverId": "1661573945107611649",
    "driverName": "李斯",
    "driverPhone": "15810108888",
    "vehicleId": 1661574934279684098,
    "vehicleNo": "川AL6826",
    "vehicleColor": 2,
    "vehicleDistinguishNo": "AL6826",
    "vehicleType": "1657997625979293698",
    "vehicleTypeName": "自卸车"
}

print(f"📤 请求参数:")
print(json.dumps(dispatch_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(DISPATCH_URL, json=dispatch_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 调度派车成功！")
    print(f"   📋 调度单号: {result.get('scheduleNo')}")
    print(f"   📊 物流状态: {result.get('logisticsStatus')}")
else:
    print(f"\n❌ 调度失败: {result.get('message')}")