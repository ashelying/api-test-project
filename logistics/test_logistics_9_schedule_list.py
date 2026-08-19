# 9.获取调度单详情
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
SCHEDULE_LIST_URL = BASE_URL + "/api/order/pc/schedule/findPage"

print("=" * 60)
print("  9️⃣ 获取调度单页面列表数据")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：获取调度单列表
print("\n📤 第二步：获取调度单列表...")

schedule_data = {
    "current": 1,
    "size": 20,
    "scheduleMapStatus": 1,
    "dataType": "2",
    "dataValue": "DDU202307141340531792",
    "timeStamp": int(time.time())
}

print(f"📤 请求参数:")
print(json.dumps(schedule_data, ensure_ascii=False, indent=2))

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(SCHEDULE_LIST_URL, json=schedule_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    data = result.get('data', {})
    records = data.get('records', {})
    print(f"\n✅ 获取调度单列表成功！")
    print(f"   📊 当前页: {data.get('current')}")
    print(f"   📊 总页数: {data.get('pages')}")
else:
    print(f"\n❌ 获取失败: {result.get('message')}")