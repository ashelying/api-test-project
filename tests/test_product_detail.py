# 2.获取商品详情接口
import requests
import json

BASE_URL = "http://127.0.0.1:8787"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"
PRODUCT_DETAIL_URL = BASE_URL + "/coupApply/cms/productDetail"

print("=" * 60)
print("  2️⃣ 获取商品详情")
print("=" * 60)

# 第一步：先获取商品列表，拿到商品ID
print("📤 第一步：获取商品列表...")
list_response = requests.get(GOODS_LIST_URL, params={
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 10
})
list_result = list_response.json()
goods_list = list_result.get('goodList', [])

if not goods_list:
    print("❌ 商品列表为空，无法测试")
    exit()

# 取第一个商品
first_goods = goods_list[0]
pro_id = first_goods.get('id')
print(f"✅ 获取到商品ID: {pro_id}")

print("\n📤 第二步：获取商品详情...")

# 第二步：用商品ID获取详情
# ⭐ 注意：这里是 json 参数，不是 data！
json_data = {
    "pro_id": pro_id,
    "page": 1,
    "size": 20
}

# JSON提交需要设置 Content-Type: application/json
headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

print(f"📤 请求参数: {json_data}")

response = requests.post(PRODUCT_DETAIL_URL, json=json_data, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(f"   error_code: {result.get('error_code')}")
print(f"   server_time: {result.get('server_time')}")

# 打印商品详情
item = result.get('item')
if item:
    print(f"\n📦 商品详情:")
    if isinstance(item, dict):
        for key, value in item.items():
            print(f"   {key}: {value}")
    else:
        print(f"   {item}")
else:
    print("   暂无详情数据")
