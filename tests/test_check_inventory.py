# 9.校验商品库存
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"
CHECK_INVENTORY_URL = BASE_URL + "/coupApply/cms/shoppingInventory"

print("=" * 60)
print("  3️⃣ 校验商品库存")
print("=" * 60)

# 第一步：登录
print("📤 第一步：登录获取token...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
token = login_response.json().get('token')
print(f"✅ 登录成功，token: {token[:20]}...")

# 第二步：获取商品列表
print("\n📤 第二步：获取商品列表...")
list_response = requests.get(GOODS_LIST_URL, params={
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 10
})
goods_list = list_response.json().get('goodList', [])
first_goods = goods_list[0]

print(f"✅ 选择商品: {first_goods.get('name')}")
print(f"📊 商品库存: {first_goods.get('stock')}")

# 第三步：校验库存（正常情况）
print("\n📤 第三步：校验库存（正常情况）...")
check_data = {
    "goodsId": first_goods.get('id'),
    "count": 10,  # 小于库存
    "timeStamp": int(time.time()),
    "token": token
}

headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(CHECK_INVENTORY_URL, json=check_data, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

# 解析状态
status = result.get('status')
status_map = {
    "0": "✅ 库存正常",
    "1": "❌ 库存不足"
}
print(f"\n📊 库存状态: {status_map.get(str(status), '未知状态')}")

# 第四步：校验库存（不足情况）
print("\n📤 第四步：校验库存（不足情况）...")
check_data_low = {
    "goodsId": first_goods.get('id'),
    "count": 999,  # 大于库存
    "timeStamp": int(time.time()),
    "token": token
}

response = requests.post(CHECK_INVENTORY_URL, json=check_data_low, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

status = result.get('status')
print(f"\n📊 库存状态: {status_map.get(str(status), '未知状态')}")