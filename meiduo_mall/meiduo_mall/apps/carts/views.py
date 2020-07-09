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
                    "count": int(count),
                    "id": sku.id
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
                return render(request, 'cart.html')

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
                    "count": int(count_selected["count"]),
                    "id": sku.id
                }
                sku_list.append(sku_dict)

            # 6,返回响应
            context = {
                "sku_carts": sku_list
            }
            # 3,返回响应
            return render(request, 'cart.html', context=context)

    def put(self, request):
        # 1,获取参数
        dict_data = json.loads(request.body.decode())
        sku_id = dict_data.get("sku_id")
        count = dict_data.get("count")
        selected = dict_data.get("selected", True)

        # 2,校验参数
        # 2.1 为空校验
        if not all([sku_id, count]):
            return http.HttpResponseForbidden("参数不全")

        # 2.2 sku_id对应的商品对象是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden('商品不存在')

        # 2.3 将count整数化
        try:
            count = int(count)
        except Exception as e:
            return http.HttpResponseForbidden('count数量有误')

        # 3,判断用户状态
        user = request.user
        if user.is_authenticated:
            # 3.1 获取redis对象
            redis_conn = get_redis_connection("cart")

            # 3.2 修改数据
            redis_conn.hset("cart_%s" % user.id, sku_id, count)

            if selected:
                redis_conn.sadd("cart_selected_%s" % user.id, sku_id)
            else:
                redis_conn.srem("cart_selected_%s" % user.id, sku_id)

            # 3.3 拼接数据返回响应
            context = {
                "code": RET.OK,
                "cart_sku": {
                    "default_image_url": sku.default_image_url.url,
                    "name": sku.name,
                    "price": str(sku.price),
                    "amount": str(sku.price * count),
                    "selected": selected,
                    "count": int(count),
                    "id": sku.id
                }
            }
            return http.JsonResponse(context)
        else:
            # 4.1 获取cookie中数据
            cookie_cart = request.COOKIES.get("cart")

            # 4.2 字典转换
            cookie_dict = {}
            if cookie_cart:
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

            # 4.3 修改
            cookie_dict[sku_id] = {
                "count": count,
                "selected": selected
            }

            # 4.4 转换并返回
            context = {
                "code": RET.OK,
                "cart_sku": {
                    "default_image_url": sku.default_image_url.url,
                    "name": sku.name,
                    "price": str(sku.price),
                    "amount": str(sku.price * count),
                    "selected": selected,
                    "count": int(count),
                    "id": sku.id
                }
            }
            response = http.JsonResponse(context)
            cookie_cart = base64.b64encode(pickle.dumps(cookie_dict)).decode()
            response.set_cookie("cart", cookie_cart)
            return response

    def delete(self, request):
        # 1,获取参数
        dict_data = json.loads(request.body.decode())
        sku_id = dict_data.get("sku_id")

        # 2,校验参数
        # 2.1 为空校验
        if not sku_id:
            return http.HttpResponseForbidden("参数不全")

        # 2.2 sku_id对应的商品对象是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden('商品不存在')

        # 3 判断用户登录状态
        user = request.user
        if user.is_authenticated:
            # 3.3 获取redis对象
            redis_conn = get_redis_connection("cart")
            pipeline = redis_conn.pipeline()

            # 3.3 删除数据
            pipeline.hdel("cart_%s" % user.id, sku_id)
            pipeline.srem("cart_selected_%s" % user.id, sku_id)
            pipeline.execute()

            # 3.4 返回响应
            return http.JsonResponse({"code": RET.OK, "errmsg": "success"})
        else:
            # 4.1获取cookie数据
            cookie_cart = request.COOKIES.get("cart")

            # 4.2字典转换
            cookie_dict = {}
            if cookie_cart:
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

            # 4.3删除数据
            if sku_id in cookie_dict:
                del cookie_dict[sku_id]

            # 4.4返回响应
            response = http.JsonResponse({"code": RET.OK, "errmsg": "success"})
            cookie_cart = base64.b64encode(pickle.dumps(cookie_dict)).decode()
            response.set_cookie("cart", cookie_cart)
            return response


class CartSelectedAllView(View):
    def put(self, request):
        # 1,获取参数
        selected = json.loads(request.body.decode()).get("selected", True)

        # 2,判断用户状态
        user = request.user
        if user.is_authenticated:
            # 2.1获取redis对象,获取数据
            redis_conn = get_redis_connection("cart")
            cart_dict = redis_conn.hgetall("cart_%s" % user.id)
            sku_id_list = cart_dict.keys()

            # 2.2全选数据
            if selected:
                redis_conn.sadd("cart_selected_%s" % user.id, *sku_id_list)
            else:
                redis_conn.srem("cart_selected_%s" % user.id, *sku_id_list)

            # 2.3返回响应
            return http.JsonResponse({"code": RET.OK, "errmsg": "success"})
        else:
            # 3.1 获取cookie中的数据
            cookie_cart = request.COOKIES.get("cart")

            # 3.2 转换字典
            cookie_dict = {}
            if cookie_cart:
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

            # 3.3 修改全选状态
            for sku_id in cookie_dict:
                cookie_dict[sku_id]["selected"] = selected

            # 3.4 返回响应
            response = http.JsonResponse({"code": RET.OK, "errmsg": "success"})
            cookie_cart = base64.b64encode(pickle.dumps(cookie_dict)).decode()
            response.set_cookie("cart", cookie_cart)
            return response


class CartSimpleView(View):
    def get(self, request):

        # 1,判断用户状态
        user = request.user

        if user.is_authenticated:
            # 2,1获取redis对象,取出数据
            redis_conn = get_redis_connection("cart")
            cart_dict = redis_conn.hgetall("cart_%s" % user.id)

            # 2,2拼接数据
            sku_list = []
            for sku_id, count in cart_dict.items():
                sku = SKU.objects.get(id=sku_id)
                sku_dict = {
                    "id": sku.id,
                    "name": sku.name,
                    "default_image_url": sku.default_image_url.url,
                    "count": int(count)
                }
                sku_list.append(sku_dict)

            # 2.3返回响应
            context = {
                "cart_skus": sku_list
            }
            return http.JsonResponse(context)
        else:
            # 3.1 获取cookie数据
            cookie_cart = request.COOKIES.get("cart")

            # 3.2字典转换
            cookie_dict = {}
            if cookie_cart:
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

            # 3.3拼接数据
            sku_list = []
            for sku_id, count_selected in cookie_dict.items():
                sku = SKU.objects.get(id=sku_id)
                sku_dict = {
                    "id": sku.id,
                    "name": sku.name,
                    "default_image_url": sku.default_image_url.url,
                    "count": int(count_selected["count"])
                }
                sku_list.append(sku_dict)

            # 3.4返回
            context = {
                "cart_skus": sku_list
            }
            return http.JsonResponse(context)
