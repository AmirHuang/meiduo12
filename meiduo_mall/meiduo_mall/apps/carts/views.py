import json
from django import http
from django.shortcuts import render
from django.views import View
from goods.models import SKU
from django_redis import get_redis_connection
from meiduo_mall.utils.response_code import RET
import pickle
import base64


class CartView(View):
    def post(self, request):
        # 1,获取参数
        dict_data = json.loads(request.body.decode())
        sku_id = dict_data.get("sku_id")
        count = dict_data.get("count")
        selected = dict_data.get("selected", True)
        user = request.user

        # 2,校验参数
        # 2.1为空校验
        if not all([sku_id, count]):
            return http.HttpResponseForbidden("参数不全")

        # 2.2判断count是否是整数
        try:
            count = int(count)
        except Exception as e:
            return http.HttpResponseForbidden("购买的数量错误")

        # 2,2校验商品对象是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden("商品不存在")

        # 2,3校验库存是否充足
        if count > sku.stock:
            return http.HttpResponseForbidden("库存不足")

        # 3,判断用户状态
        if user.is_authenticated:
            # 3,1获取redis对象
            redis_conn = get_redis_connection("cart")

            # 3,2添加数据到redis
            redis_conn.hincrby("cart_%s" % user.id, sku_id, count)

            if selected:
                redis_conn.sadd("cart_selected_%s" % user.id, sku_id)

            # 3,返回响应
            return http.JsonResponse({"code": RET.OK})
        else:
            # 4,1获取cookie中的购物车数据
            cookie_cart = request.COOKIES.get("cart")

            # 4,2判断,转换成字典
            cookie_dict = {}
            if cookie_cart:
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

            # 4,3累加count
            if sku_id in cookie_dict:
                count += cookie_dict[sku_id].get("count", 0)

            # 4,4设置新的数据
            cookie_dict[sku_id] = {
                "count": count,
                "selected": selected
            }

            # 4,5设置cookie,返回响应
            response = http.JsonResponse({"code": RET.OK})
            cookie_cart = base64.b64encode(pickle.dumps(cookie_dict)).decode()
            response.set_cookie("cart", cookie_cart)

            return response

    def get(self, request):

        # 1,判断用户登陆状态
        user = request.user
        if user.is_authenticated:
            # 1,获取redis数据
            redis_conn = get_redis_connection("cart")
            cart_dict = redis_conn.hgetall("cart_%s" % user.id)
            cart_selected_list = redis_conn.smembers("cart_selected_%s" % user.id)

            # 2,拼接数据
            sku_list = []
            for sku_id, count in cart_dict.items():
                sku = SKU.objects.get(id=sku_id)
                sku_dict = {
                    "default_image_url": sku.default_image_url.url,
                    "name": sku.name,
                    "price": str(sku.price),
                    "amount": str(sku.price * int(count)),
                    "selected": str(sku_id in cart_selected_list),
                    "count": int(count)
                }
                sku_list.append(sku_dict)

            context = {
                "sku_carts": sku_list
            }
            # 3,返回响应
            return render(request, 'cart.html', context=context)
        else:
            # 4,获取cookie中的数据
            cookie_cart = request.COOKIES.get("cart")

            if not cookie_cart:
                return render(request, 'detail.html')

            # 5,数据转换
            cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))
            sku_list = []

            for sku_id, count_selected in cookie_dict.items():
                sku = SKU.objects.get(id=sku_id)
                sku_dict = {
                    "default_image_url": sku.default_image_url.url,
                    "name": sku.name,
                    "price": str(sku.price),
                    "amount": str(sku.price * int(count_selected["count"])),
                    "selected": str(count_selected["selected"]),
                    "count": int(count_selected["count"])
                }
                sku_list.append(sku_dict)

            # 6,返回响应
            context = {
                "sku_carts": sku_list
            }
            # 3,返回响应
            return render(request, 'cart.html', context=context)
