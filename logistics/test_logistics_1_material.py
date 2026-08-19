# 1.获取下单物料信息
import requests
import json

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
MATERIAL_URL = BASE_URL + "/api/order/customer/orderPlan/create"

print("=" * 60)
print("  1️⃣ 获取下单物料信息")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功，Cookie: {cookies}")

# 第二步：获取物料信息（GET请求，携带Cookie）
print("\n📤 第二步：获取物料信息...")
response = requests.get(MATERIAL_URL, cookies=cookies)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

# 提取物料列表
material_list = result.get('material', [])
print(f"\n📦 共 {len(material_list)} 个物料:")
for i, material_id in enumerate(material_list[:5], 1):
    print(f"   {i}. 物料ID: {material_id}")