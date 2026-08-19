# 1.获取商品列表接口

import requests

BASE_URL = "http://127.0.0.1:8787"
GOODS_LIST_URL = BASE_URL + "/coupApply/cms/goodsList"

print("=" * 60)
print("  1️⃣ 获取商品列表")
print("=" * 60)

# GET请求：参数放在 params 里
params = {
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 10
}

print(f"📤 请求参数: {params}")

response = requests.get(GOODS_LIST_URL, params=params)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(f"   error_code: {result.get('error_code')}")
print(f"   server_time: {result.get('server_time')}")

# 打印商品列表
goods_list = result.get('goodList', [])
print(f"\n📦 共 {len(goods_list)} 个商品:")
for i, goods in enumerate(goods_list, 1):
    print(f"   {i}. ID: {goods.get('id')}, 名称: {goods.get('name')}, 价格: {goods.get('price')}")