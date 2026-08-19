import pytest
from utils.api_client import client


class TestGoods:
    """商品接口测试"""

    @classmethod
    def setup_class(cls):
        """测试前登录"""
        client.login()

    def test_get_goods_list(self):
        """测试获取商品列表"""
        response = client.get("/coupApply/cms/goodsList",
                              params={"msgType": "getHandsetListOfCust", "page": 1, "size": 10})
        assert response.status_code == 200
        result = response.json()
        assert result.get('error_code') == '0000'
        assert 'goodList' in result
        print(f"✅ 获取商品列表成功，共 {len(result.get('goodList', []))} 个商品")

    def test_get_product_detail(self):
        """测试获取商品详情"""
        # 先获取商品列表
        list_response = client.get("/coupApply/cms/goodsList",
                                   params={"msgType": "getHandsetListOfCust", "page": 1, "size": 10})
        goods_list = list_response.json().get('goodList', [])

        if goods_list:
            pro_id = goods_list[0].get('id')
            response = client.post_json("/coupApply/cms/productDetail",
                                        {"pro_id": pro_id, "page": 1, "size": 20},
                                        need_token=False)
            assert response.status_code == 200
            result = response.json()
            assert result.get('error_code') == '0000'
            assert 'item' in result
            print(f"✅ 获取商品详情成功，商品ID: {pro_id}")
        else:
            pytest.skip("商品列表为空")

    def test_add_to_cart(self):
        """测试添加购物车"""
        # 先获取商品列表
        list_response = client.get("/coupApply/cms/goodsList",
                                   params={"msgType": "getHandsetListOfCust", "page": 1, "size": 10})
        goods_list = list_response.json().get('goodList', [])

        if goods_list:
            goods = goods_list[0]
            response = client.post_json("/coupApply/cms/shoppingJoinCart", {
                "goods_id": goods['id'],
                "count": 2,
                "price": goods['price']
            })
            assert response.status_code == 200
            result = response.json()
            assert result.get('error_code') == '0000'
            print(f"✅ 添加购物车成功，商品: {goods['name']}")
        else:
            pytest.skip("商品列表为空")