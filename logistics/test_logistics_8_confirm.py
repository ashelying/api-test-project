# 8.获取调度单页面列表数据
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
CONFIRM_URL = BASE_URL + "/api/order/app/schedule/confirm"

print("=" * 60)
print("  8️⃣ 司机确认运输")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功")

# 第二步：司机确认
print("\n📤 第二步：司机确认运输...")

confirm_data = {
    "scheduleNo": "DDU202307141409506827",  # 调度单号
    "timeStamp": int(time.time())
}

print(f"📤 请求参数: {confirm_data}")

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(CONFIRM_URL, json=confirm_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('code') == 20000:
    print(f"\n✅ 司机确认成功！")
    print(f"   📊 调度状态: {result.get('scheduleNoStatus')}")
else:
    print(f"\n❌ 确认失败: {result.get('message')}")