from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

# ==================== 模拟数据 ====================
users = {
    "test01": {
        "password": "admin123",
        "token": "0115930862970452224",
        "user_id": 1001
    },
    "test02": {
        "password": "admin456",
        "token": "0115930862970452225",
        "user_id": 1002
    }
}

user_db = {
    1001: {"username": "test01", "password": "admin123", "phone": "13800000000", "dates": "2023-12-31",
           "role_id": "123456789"},
    1002: {"username": "test02", "password": "admin456", "phone": "13900000000", "dates": "2024-12-31",
           "role_id": "987654321"}
}
next_user_id = 1003


# ==================== 1. 用户登录接口 ====================
@app.route('/da/user/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    passwd = request.form.get('passwd')

    if user_name in users and users[user_name]['password'] == passwd:
        return jsonify({
            "msg": "登录成功",
            "msg_code": 200,
            "error_code": None,
            "token": users[user_name]['token']
        })
    else:
        return jsonify({
            "msg": "用户名或密码错误",
            "msg_code": 400,
            "error_code": "1001",
            "token": None
        })


# ==================== 2. 新增用户接口 ====================
@app.route('/char/user/addUser', methods=['POST'])
def add_user():
    global next_user_id
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        role_id = request.form.get('role_id')
        dates = request.form.get('dates')
        phone = request.form.get('phone')
        token = request.form.get('token')

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "msg": "登录信息校验失败",
                "msg_code": 401,
                "error_code": "1002"
            })

        user_id = next_user_id
        next_user_id += 1
        user_db[user_id] = {
            "username": username,
            "password": password,
            "phone": phone,
            "dates": dates,
            "role_id": role_id
        }

        return jsonify({
            "msg": "用户添加成功",
            "msg_code": 200,
            "error_code": None
        })
    except Exception as e:
        return jsonify({
            "msg": f"添加失败: {str(e)}",
            "msg_code": 500,
            "error_code": "1003"
        })


# ==================== 3. 查询用户接口 ====================
@app.route('/char/user/queryUser', methods=['POST'])
def query_user():
    try:
        user_id = int(request.form.get('user_id'))
        if user_id in user_db:
            return jsonify({
                "msg": "查询成功",
                "msg_code": 200,
                "error_code": None,
                "data": user_db[user_id]
            })
        else:
            return jsonify({
                "msg": "用户不存在",
                "msg_code": 404,
                "error_code": "1004"
            })
    except:
        return jsonify({
            "msg": "参数错误",
            "msg_code": 400,
            "error_code": "1005"
        })


# ==================== 4. 删除用户接口 ====================
@app.route('/char/user/deleteUser', methods=['POST'])
def delete_user():
    try:
        user_id = int(request.form.get('user_id'))
        if user_id in user_db:
            del user_db[user_id]
            return jsonify({
                "msg": "删除成功",
                "msg_code": 200,
                "error_code": None
            })
        else:
            return jsonify({
                "msg": "用户不存在",
                "msg_code": 404,
                "error_code": "1004"
            })
    except:
        return jsonify({
            "msg": "参数错误",
            "msg_code": 400,
            "error_code": "1005"
        })


# ==================== 5. 修改用户接口 ====================
@app.route('/char/user/updateUser', methods=['POST'])
def update_user():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        role_id = request.form.get('role_id')
        dates = request.form.get('dates')
        phone = request.form.get('phone')
        token = request.form.get('token')
        user_id = int(request.form.get('user_id'))

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "msg": "登录信息校验失败",
                "msg_code": 401,
                "error_code": "1002"
            })

        if user_id in user_db:
            user_db[user_id].update({
                "username": username,
                "password": password,
                "phone": phone,
                "dates": dates,
                "role_id": role_id
            })
            return jsonify({
                "msg": "修改成功",
                "msg_code": 200,
                "error_code": None
            })
        else:
            return jsonify({
                "msg": "用户不存在",
                "msg_code": 404,
                "error_code": "1004"
            })
    except Exception as e:
        return jsonify({
            "msg": f"修改失败: {str(e)}",
            "msg_code": 500,
            "error_code": "1003"
        })


# ==================== 6. 获取商品列表接口 ====================
@app.route('/coupApply/cms/goodsList', methods=['GET'])
def goods_list():
    mock_goods = [
        {"id": "18382788819", "name": "iPhone 15 Pro", "price": "128", "stock": 100},
        {"id": "33809635011", "name": "MacBook Pro", "price": "188", "stock": 50},
        {"id": "1234499012", "name": "AirPods Pro", "price": "68", "stock": 200}
    ]
    return jsonify({
        "goodList": mock_goods,
        "error": "",
        "error_code": "0000",
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })


# ==================== 7. 获取商品详情接口（修复版） ====================
@app.route('/coupApply/cms/productDetail', methods=['POST'])
def product_detail():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        pro_id = data.get('pro_id') if data else None

        if not pro_id:
            return jsonify({
                "error": "缺少商品ID",
                "error_code": "1001",
                "item": {}
            })

        mock_detail = {
            "id": pro_id,
            "name": "iPhone 15 Pro",
            "price": "128",
            "stock": 100,
            "description": "A17 Pro 芯片，钛金属边框，USB-C 接口",
            "specs": "6.1英寸，256GB，黑色钛金属"
        }
        return jsonify({
            "item": mock_detail,
            "error": "",
            "error_code": "0000",
            "server_time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1002",
            "item": {}
        })


# ==================== 8. 添加购物车接口 ====================
@app.route('/coupApply/cms/shoppingJoinCart', methods=['POST'])
def add_cart():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        goods_id = data.get('goods_id') if data else None
        count = data.get('count') if data else 1
        price = data.get('price') if data else "0"
        token = data.get('token') if data else None

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001",
                "message": "请先登录"
            })

        return jsonify({
            "cartList": [{"goods_id": goods_id, "count": count, "price": price}],
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": "",
            "error_code": "0000",
            "message": "success",
            "translate_language": "zh-CN",
            "userId": "2929549245116909803"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1002",
            "message": "添加失败"
        })


# ==================== 9. 删除购物车接口 ====================
@app.route('/coupApply/cms/delCart', methods=['POST'])
def del_cart():
    try:
        # 表单提交，用 request.form
        product_id = request.form.get('productId')
        time_stamp = request.form.get('timeStamp')
        token = request.form.get('token')

        # 校验 token
        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001",
                "message": "请先登录"
            })

        if not product_id:
            return jsonify({
                "error": "缺少商品ID",
                "error_code": "1002",
                "message": "删除失败"
            })

        return jsonify({
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": "",
            "error_code": "0000",
            "message": "success",
            "translate_language": "zh-CN",
            "userId": "2929549245116909803"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1003",
            "message": "删除失败"
        })


# ==================== 10. 提交订单 ====================
@app.route('/coupApply/cms/placeAnOrder', methods=['POST'])
def place_order():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        token = data.get('token') if data else None

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001",
                "message": "请先登录"
            })

        # 生成订单号
        import random
        order_number = str(int(time.time() * 1000)) + str(random.randint(100, 999))

        return jsonify({
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": "",
            "error_code": "0000",
            "message": "提交订单成功",
            "orderNumber": order_number,
            "userId": "3036812012882072604",
            "translate_language": "zh-CN"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1002",
            "message": "提交订单失败"
        })


# ==================== 11. 订单支付 ====================
@app.route('/coupApply/cms/orderPay', methods=['POST'])
def order_pay():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        order_number = data.get('orderNumber') if data else None
        user_id = data.get('userId') if data else None
        token = data.get('token') if data else None

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001",
                "message": "请先登录"
            })

        if not order_number:
            return jsonify({
                "error": "缺少订单号",
                "error_code": "1002",
                "message": "支付失败"
            })

        return jsonify({
            "create": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": "",
            "error_code": "0000",
            "message": "订单支付成功",
            "translate_language": "zh-CN"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1003",
            "message": "支付失败"
        })


# ==================== 12. 校验订单状态 ====================
@app.route('/coupApply/cms/checkOrderStatus', methods=['POST'])
def check_order_status():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        order_number = data.get('orderNumber') if data else None
        token = data.get('token') if data else None

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001"
            })

        # 模拟订单状态（随机返回 0, 1, 2）
        import random
        status = str(random.randint(0, 2))
        return jsonify({
            "queryTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": "",
            "error_code": "0000",
            "status": status,
            "translate_language": "zh-CN"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1002"
        })


# ==================== 13. 校验物流状态 ====================
@app.route('/coupApply/cms/checkLogisticsStatus', methods=['POST'])
def check_logistics_status():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        order_number = data.get('orderNumber') if data else None
        token = data.get('token') if data else None

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001"
            })

        # 模拟物流状态（随机返回 0, 1, 2, 3）
        import random
        status = str(random.randint(0, 3))
        return jsonify({
            "queryTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": "",
            "error_code": "0000",
            "status": status,
            "translate_language": "zh-CN"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1002"
        })


# ==================== 14. 校验商品库存 ====================
@app.route('/coupApply/cms/shoppingInventory', methods=['POST'])
def check_inventory():
    try:
        data = request.get_json()
        if data is None:
            data = request.form.to_dict()

        goods_id = data.get('goodsId') if data else None
        count = int(data.get('count', 0)) if data else 0
        token = data.get('token') if data else None

        valid_tokens = [u['token'] for u in users.values()]
        if not token or token not in valid_tokens:
            return jsonify({
                "error": "未授权",
                "error_code": "1001"
            })

        # 模拟库存判断：库存100
        stock = 100
        if count > stock:
            return jsonify({
                "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": "商品库存不足",
                "error_code": "0000",
                "status": "1",
                "translate_language": "zh-CN"
            })
        else:
            return jsonify({
                "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": "",
                "error_code": "0000",
                "status": "0",
                "translate_language": "zh-CN"
            })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_code": "1002"
        })

# ==================== 物流项目模拟接口 ====================

# 1. 获取下单物料信息
@app.route('/api/order/customer/orderPlan/create', methods=['GET'])
def get_material():
    mock_material = [
        "1676511586856882178", "1676511586856882134",
        "1676511524756882178", "1676590766856882178",
        "1676511586812182178"
    ]
    return jsonify({
        "code": 20000,
        "data": True,
        "material": mock_material,
        "message": "操作成功"
    })

# 2. 货主下订单
@app.route('/api/order/customer/orderPlan/create', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": True,
            "message": "操作成功",
            "orderNo": "DD" + str(int(time.time())) + str(random.randint(100, 999))
        })
    except:
        return jsonify({
            "code": 20000,
            "data": True,
            "message": "操作成功",
            "orderNo": "DD20230713164416758"
        })

# 3. 集团接收订单
@app.route('/api/order/pc/order/master/receive', methods=['POST'])
def master_receive():
    return jsonify({
        "code": 20000,
        "data": True,
        "message": "操作成功"
    })

# 4. 集团分配订单
@app.route('/api/order/pc/order/assign', methods=['POST'])
def assign_order():
    return jsonify({
        "code": 20000,
        "data": True,
        "message": "操作成功"
    })

# 5. 物流公司接单
@app.route('/api/order/pc/order/trans/receive', methods=['POST'])
def trans_receive():
    return jsonify({
        "code": 20000,
        "data": True,
        "message": "操作成功"
    })

# 6. 物流公司拆分订单
@app.route('/api/order/pc/logisticsOrder/handSplitOrder', methods=['POST'])
def split_order():
    return jsonify({
        "code": 20000,
        "data": True,
        "logisticsStatus": "1",
        "message": "操作成功"
    })

# 7. 调度派车（添加这个接口）
@app.route('/api/order/pc/logisticsOrder/handCapacityDispatch', methods=['POST'])
def dispatch():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": True,
            "logisticsStatus": "1",
            "message": "操作成功",
            "scheduleNo": "DDU" + str(int(time.time())) + str(random.randint(100, 999))
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": False,
            "message": str(e)
        })

# 8. 司机确认运输
@app.route('/api/order/app/schedule/confirm', methods=['POST'])
def confirm_transport():
    return jsonify({
        "code": 20000,
        "data": True,
        "message": "司机确认成功",
        "scheduleNoStatus": "1"
    })

# ==================== 9. 获取调度单页面列表数据 ====================
@app.route('/api/order/pc/schedule/findPage', methods=['POST'])
def schedule_list():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": {
                "current": 1,
                "pages": "1",
                "records": {
                    "logisticsOrderNo": "W202307130000001793",
                    "scheduleNo": "DDU202307141340531792",
                    "createTime": "2026-08-13 10:00:00",
                    "executiveOrg": "物流公司",
                    "logisticsStatus": "1"
                }
            },
            "message": "操作成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": None,
            "message": str(e)
        })

# ==================== 10. SRM系统推送运量出库信息 ====================
@app.route('/rpc/srm/inventory', methods=['POST'])
def srm_push():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": {
                "countId": None,
                "maxLimit": None,
                "optimizeCountSql": True,
                "pages": "1"
            },
            "message": "处理成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": None,
            "message": str(e)
        })

# ==================== 11. 计量系统推送入库、退货量 ====================
@app.route('/order/feign/dbjlxt', methods=['POST'])
def measure_push():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": True,
            "message": "处理成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": False,
            "message": str(e)
        })

# ==================== 12. 创建应付对账单 ====================
@app.route('/api/order/pc/cost/receiveCost/create/bill', methods=['POST'])
def create_bill():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": True,
            "message": "操作成功",
            "reconciliationNum": "DZ" + str(int(time.time())) + str(random.randint(100, 999))
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": False,
            "message": str(e)
        })

# ==================== 13. 获取应付对账单详情及运费 ====================
@app.route('/api/order/pc/cost/payCost/page', methods=['POST'])
def bill_detail():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": {
                "current": "1",
                "pages": "1",
                "records": [
                    {
                        "carrierName": "第一车队",
                        "driverName": "张飞",
                        "freightPrice": 53,
                        "logisticsOrderNo": "W202307040000001541",
                        "costBillId": "1676121546600480768"
                    }
                ]
            },
            "message": "操作成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": None,
            "message": str(e)
        })

# ==================== 14. 添加承运商 ====================
@app.route('/api/user/pc/carrier/carrier/add', methods=['POST'])
def add_carrier():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": True,
            "message": "操作成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": False,
            "message": str(e)
        })

# ==================== 15. 获取承运商列表 ====================
@app.route('/api/user/pc/carrier/cys/findPage', methods=['POST'])
def carrier_list():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "data": {
                "current": 1,
                "pages": 1,
                "records": [
                    {
                        "carrierId": "1661558222301904898",
                        "carrierName": "长凡贸易有限公司",
                        "contactTel": "15810108888",
                        "legalPerson": "张三"
                    },
                    {
                        "carrierId": "1661558222301904899",
                        "carrierName": "第二车队",
                        "contactTel": "13900000000",
                        "legalPerson": "李四"
                    }
                ]
            },
            "message": "操作成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": None,
            "message": str(e)
        })

# ==================== 16. 删除承运商 ====================
@app.route('/api/user/pc/carrier/carrier/delete', methods=['POST'])
def delete_carrier():
    try:
        data = request.get_json()
        return jsonify({
            "code": 20000,
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": [],
            "message": "操作成功"
        })
    except Exception as e:
        return jsonify({
            "code": 50000,
            "data": None,
            "message": str(e)
        })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Flask 测试服务启动中...")
    print("📡 服务地址: http://127.0.0.1:8787")
    print("👤 测试账号: test01 / admin123")
    print("👤 测试账号: test02 / admin456")
    print("=" * 50)
    app.run(host='127.0.0.1', port=8787, debug=True)