# 提交订单接口
import requests
import json

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"
PLACE_ORDER_URL = BASE_URL + "/coupApply/cms/placeAnOrder"

print("=" * 60)
print("  2️⃣ 提交订单")
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
print(f"✅ 选择商品: {first_goods.get('name')}, 价格: {first_goods.get('price')}")

# 第三步：提交订单
print("\n📤 第三步：提交订单...")

# ⭐ 构造嵌套JSON
order_data = {
    "goods_id": first_goods.get('id'),
    "number": 2,
    "propertyChildIds": "2:9",
    "inviter_id": 127839112,
    "price": first_goods.get('price'),
    "freight_insurance": "0.00",
    "discount_code": "002399",
    "consignee_info": {
        "name": "张三",
        "phone": 13800000000,
        "address": "北京市海淀区西三环北路74号院4栋3单元1008"
    },
    "token": token  # token放在最外层
}

print("📤 请求参数（嵌套JSON）:")
print(json.dumps(order_data, ensure_ascii=False, indent=2))

headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

response = requests.post(PLACE_ORDER_URL, json=order_data, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

if result.get('error_code') == '0000':
    print(f"\n✅ 提交订单成功！")
    print(f"   📋 订单号: {result.get('orderNumber')}")
    print(f"   👤 用户ID: {result.get('userId')}")
    print(f"   🕐 创建时间: {result.get('createTime')}")
else:
    print(f"\n❌ 提交订单失败: {result.get('message')}")
    