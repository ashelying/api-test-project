# 6.删除购物车商品接口
import requests
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"
ADD_CART_URL = BASE_URL + "/coupApply/cms/shoppingJoinCart"
DEL_CART_URL = BASE_URL + "/coupApply/cms/delCart"

print("=" * 60)
print("  1️⃣ 删除购物车商品")
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

# 第三步：先添加一个商品到购物车（确保有东西可删）
print("\n📤 第三步：先添加商品到购物车...")
add_data = {
    "goods_id": first_goods.get('id'),
    "count": 1,
    "price": first_goods.get('price'),
    "token": token
}
add_response = requests.post(ADD_CART_URL, json=add_data, headers={
    "Content-Type": "application/json;charset=UTF-8"
})
print(f"✅ 添加购物车成功")

# 第四步：删除购物车商品
print("\n📤 第四步：删除购物车商品...")
del_data = {
    "productId": first_goods.get('id'),
    "timeStamp": int(time.time())
}
# 表单提交，需要把token也加进去
del_data["token"] = token

headers_form = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(DEL_CART_URL, data=del_data, headers=headers_form)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(f"   error_code: {result.get('error_code')}")
print(f"   message: {result.get('message')}")
print(f"   createTime: {result.get('createTime')}")

if result.get('error_code') == '0000':
    print("\n✅ 删除购物车商品成功！")
else:
    print(f"\n❌ 删除失败: {result.get('message')}")