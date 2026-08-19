import pytest
from utils.api_client import client

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """测试环境初始化"""
    # 登录
    client.login()
    yield
    print("\n✅ 所有测试完成！")

@pytest.fixture
def api_client():
    """提供API客户端"""
    return client

@pytest.fixture
def sample_goods():
    """提供测试商品"""
    from utils.api_client import client
    response = client.get("/coupApply/cms/goodsList",
                          params={"msgType": "getHandsetListOfCust", "page": 1, "size": 10})
    goods_list = response.json().get('goodList', [])
    return goods_list[0] if goods_list else None