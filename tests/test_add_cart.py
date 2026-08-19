# 5.添加购物车接口
import requests
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"
ADD_CART_URL = BASE_URL + "/coupApply/cms/shoppingJoinCart"

print("=" * 60)
print("  3️⃣ 添加购物车")
print("=" * 60)

# ==================== 第一步：登录获取token ====================
print("📤 第一步：登录获取token...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
login_result = login_response.json()
token = login_result.get('token')

if not token:
    print("❌ 登录失败，无法继续")
    exit()

print(f"✅ 登录成功，token: {token[:20]}...")

# ==================== 第二步：获取商品列表 ====================
print("\n📤 第二步：获取商品列表...")
list_response = requests.get(GOODS_LIST_URL, params={
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 10
})
list_result = list_response.json()
goods_list = list_result.get('goodList', [])

if not goods_list:
    print("❌ 商品列表为空")
    exit()

first_goods = goods_list[0]
print(f"✅ 选择商品: {first_goods.get('name')}, 价格: {first_goods.get('price')}")

# ==================== 第三步：添加购物车 ====================
print("\n📤 第三步：添加购物车...")

json_data = {
    "goods_id": first_goods.get('id'),
    "count": 2,
    "price": first_goods.get('price'),
    "timeStamp": int(time.time())
}

# ⭐ 需要携带token：放在JSON参数里
json_data["token"] = token

headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

print(f"📤 请求参数: {json_data}")

response = requests.post(ADD_CART_URL, json=json_data, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(f"   error_code: {result.get('error_code')}")
print(f"   message: {result.get('message')}")
print(f"   userId: {result.get('userId')}")
print(f"   createTime: {result.get('createTime')}")

cart_list = result.get('cartList', [])
print(f"   购物车商品数: {len(cart_list)}")