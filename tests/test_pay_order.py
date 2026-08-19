# 订单支付接口
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"
PLACE_ORDER_URL = BASE_URL + "/coupApply/cms/placeAnOrder"
PAY_ORDER_URL = BASE_URL + "/coupApply/cms/orderPay"

print("=" * 60)
print("  3️⃣ 订单支付")
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

# 第三步：提交订单（先创建订单）
print("\n📤 第三步：提交订单...")
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
    "token": token
}

headers = {"Content-Type": "application/json;charset=UTF-8"}
order_response = requests.post(PLACE_ORDER_URL, json=order_data, headers=headers)
order_result = order_response.json()

if order_result.get('error_code') != '0000':
    print(f"❌ 提交订单失败: {order_result}")
    exit()

order_number = order_result.get('orderNumber')
user_id = order_result.get('userId')
print(f"✅ 订单创建成功！订单号: {order_number}")

# 第四步：支付订单
print("\n📤 第四步：支付订单...")
pay_data = {
    "orderNumber": order_number,
    "userId": user_id,
    "timeStamp": int(time.time()),
    "token": token  # token放在最外层
}

print(f"📤 支付参数: {pay_data}")

response = requests.post(PAY_ORDER_URL, json=pay_data, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2)) # 格式化输出

if result.get('error_code') == '0000':
    print(f"\n✅ 订单支付成功！")
    print(f"   🕐 支付时间: {result.get('create')}")
else:
    print(f"\n❌ 支付失败: {result.get('message')}")