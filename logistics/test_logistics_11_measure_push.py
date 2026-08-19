# 12.计量系统推送入库、退货量
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
MEASURE_URL = BASE_URL + "/order/feign/dbjlxt"

print("=" * 60)
print("  1️⃣1️⃣ 计量系统推送入库、退货量")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：推送计量数据
print("\n📤 第二步：推送计量数据...")

measure_data = {
    "exceptOther": 100.125,
    "spareNum1": 150.125,
    "productNet": 100.125,
    "weightNo": "104077",
    "product": "高梁",
    "status": "部分退货",
    "finalFlag": "1",
    "dataStatus": "1",
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(measure_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(MEASURE_URL, json=measure_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 计量数据推送成功！")
else:
    print(f"\n❌ 推送失败: {result.get('message')}")