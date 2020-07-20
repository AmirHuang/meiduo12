import pickle
import base64
from django_redis import get_redis_connection


def merge_cookie_redis_cart(request, user, response):
    """
    :param request: 为了获取cookie数据
    :param user: 为了获取redis数据
    :param response: 为了清空cookie数据
    :return:
    """
    # 1,获取cookie数据
    cookie_cart = request.COOKIES.get("cart")

    # 2,判断cookie是否存在,如果有转换
    if not cookie_cart:
        return response

    cookie_dict = {}
    if cookie_cart:
        cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

    # 3,合并数据
    redis_conn = get_redis_connection("cart")
    for sku_id, count_selected in cookie_dict.items():
        redis_conn.hset("cart_%s" % user.id, sku_id, count_selected["count"])

        if count_selected["selected"]:
            redis_conn.sadd("cart_selected_%s" % user.id, sku_id)
        else:
            redis_conn.srem("cart_selected_%s" % user.id, sku_id)

    # 4,清除cookie,返回响应
    response.delete_cookie("cart")
    return response
