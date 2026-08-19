# 11.SRM 系统推送运量出库信息
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
SRM_URL = BASE_URL + "/rpc/srm/inventory"

print("=" * 60)
print("  🔟 SRM系统推送运量出库信息")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：推送出库信息
print("\n📤 第二步：推送运量出库信息...")

srm_data = {
    "scheduleNo": "DDU202307141437136374",
    "actionTime": "2026-08-13 10:00:00",
    "boxSpec": "40尺寸",
    "containerNo": "AJ-YJ-20-0006",
    "vehicleNo": "晋WC6799",
    "wareHouseName": "原料生产基地",
    "wareHouseAddr": "翠屏长江之源",
    "weightNo": "3567890",
    "materialList": [
        {
            "materialCode": "202306281022",
            "materialName": "高梁",
            "materialUnit": "KG",
            "materialNum": "150.125"
        }
    ]
}

print(f"📤 请求参数:")
print(json.dumps(srm_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(SRM_URL, json=srm_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ SRM推送成功！")
else:
    print(f"\n❌ 推送失败: {result.get('message')}")