# 货主（托运人）下单
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"
LOGIN_URL = BASE_URL + "/da/user/login"
ORDER_URL = BASE_URL + "/api/order/customer/orderPlan/create"

print("=" * 60)
print("  2️⃣ 货主下订单")
print("=" * 60)

# 第一步：登录获取Cookie
print("📤 第一步：登录...")
login_response = requests.post(LOGIN_URL, data={
    "user_name": "test01",
    "passwd": "admin123"
})
cookies = login_response.cookies
print(f"✅ 登录成功，Cookie: {cookies}")

# 第二步：构造订单数据
print("\n📤 第二步：构造订单数据...")

order_data = {
    "orderInfo": {
        "template": "define",
        "urgentType": 2,
        "cusName": "总仓",
        "orderType": 1,
        "charter": 2,
        "planType": 1,
        "transStartTime": "2026-08-12 10:00:00",
        "transEndTime": "2026-08-14 10:00:00",
        "orderMark": "货主下单",
        "csld": "1661242770195464193"
    },
    "orderCapacityList": {
        "materialCategoryId": "1676511586856882178",
        "materialCategory": "粮食",
        "materialName": "小麦",
        "materialUnit": "KG",
        "materialUnitId": "1660891402561581058",
        "settlementUnit": "KG",
        "syncMaterialId": "4",
        "billingWeightCoe": None,
        "billingVolumeCoe": None,
        "sendWeightCoe": None,
        "sendVolumeCoe": None,
        "materialSpecList": None,
        "materialId": "1661349087048306690",
        "sendCusId": "1661663745663741954",
        "sendCusName": "码头尖庄仓",
        "receiveCusId": "1661624733406285825",
        "receiveCusName": "502车间",
        "sendAdrId": "1674617286107828226",
        "sendAdrName": "长宁县五谷粮食购销有限责任公司",
        "sendPoid": "1674615819826425857",
        "sendAdrDetail": None,
        "receiveAdrId": "1674208708683337730",
        "receiveAdrName": "五区一区",
        "receivePoid": "1674208399908237313",
        "receiveAdrDetail": "五区一区",
        "materialSpecId": "1661349088147214337",
        "specName": "1",
        "materialNum": 100,
        "materialSpecUnit": "KG",
        "remark": "原粮"
    },
    "orderVehicleList": [],
    "orderBoxList": []
}

print("📤 请求参数:")
print(json.dumps(order_data, ensure_ascii=False, indent=2))

# 第三步：发送请求
print("\n📤 第三步：提交订单...")
headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(ORDER_URL, json=order_data, cookies=cookies, headers=headers)
result = response.json()

print(f"\n📥 响应状态码: {response.status_code}")
print(f"📥 响应内容:")
print(json.dumps(result, ensure_ascii=False, indent=2))

# 提取订单号
order_no = result.get('orderNo')
if order_no:
    print(f"\n✅ 订单创建成功！")
    print(f"   📋 订单号: {order_no}")
else:
    print(f"\n❌ 订单创建失败: {result.get('message')}")