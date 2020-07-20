import json

from django.db import transaction
from django.shortcuts import render
from goods.models import SKU
from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView
from django_redis import get_redis_connection
from django import http
from decimal import Decimal

from meiduo_mall.utils.response_code import RET
from orders import OrderInfo, OrderGoods
from users.models import Address
from django.utils import timezone
from django.core.paginator import Paginator


class OrderSettlementView(MyLoginRequiredMiXinView):
    def get(self, request):

        # 1,查询用户的地址
        try:
            addresses = request.user.addresses.filter(is_deleted=False).all()
        except Exception as e:
            addresses = None

        # 2,查询用户所有的勾选的商品
        user = request.user
        redis_conn = get_redis_connection("cart")
        cart_dict = redis_conn.hgetall("cart_%s" % user.id)
        cart_selected_list = redis_conn.smembers("cart_selected_%s" % user.id)

        # 3将商品的编号转换商品的数据
        sku_list = []
        # 总数量,总金额
        total_count = 0
        total_amount = Decimal(0.0)
        for sku_id in cart_selected_list:
            sku = SKU.objects.get(id=sku_id)
            sku_dict = {
                "id": sku.id,
                "default_image_url": sku.default_image_url.url,
                "name": sku.name,
                "price": sku.price,
                "count": int(cart_dict[sku_id]),
                "amount": sku.price * int(cart_dict[sku_id])
            }
            sku_list.append(sku_dict)

            # 累加
            total_count += int(cart_dict[sku_id])
            total_amount += (sku.price * int(cart_dict[sku_id]))

        # 3,1运费,实付款
        freight = Decimal(10.0)
        payment_amount = total_amount + freight

        # 4,拼接数据,返回响应
        context = {
            "addresses": addresses,
            "skus": sku_list,
            "total_count": total_count,
            "total_amount": total_amount,
            "freight": freight,
            "payment_amount": payment_amount
        }
        return render(request, 'place_order.html', context=context)


class OrderCommitView(MyLoginRequiredMiXinView):

    @transaction.atomic
    def post(self, request):
        # 1,获取参数
        dict_data = json.loads(request.body.decode())
        address_id = dict_data.get("address_id")
        pay_method = dict_data.get("pay_method")
        user = request.user

        # 2,校验参数
        # 2.1为空校验
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden("参数不全")

        # 2.2地址校验
        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return http.HttpResponseForbidden('地址不存在')

        # 2.3支付方式校验
        pay_method = int(pay_method)
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM["CASH"], OrderInfo.PAY_METHODS_ENUM["ALIPAY"]]:
            return http.HttpResponseForbidden("支付方式有误")

        # 2.4构建订单编号(只要能尽量保证所有的用户都不重复即可)
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + "%06d" % user.id

        # 2.5创建支付状态
        if pay_method == OrderInfo.PAY_METHODS_ENUM["CASH"]:
            status = OrderInfo.ORDER_STATUS_ENUM["UNSEND"]
        else:
            status = OrderInfo.ORDER_STATUS_ENUM["UNPAID"]

        # TODO 设置保存点
        sid = transaction.savepoint()

        # 3,数据入库(订单信息)
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,
            total_amount=Decimal(0.0),
            freight=Decimal(10.0),
            pay_method=pay_method,
            status=status,
        )

        # 4,订单商品信息入库
        redis_conn = get_redis_connection("cart")
        cart_dict = redis_conn.hgetall("cart_%s" % user.id)
        cart_selected_list = redis_conn.smembers("cart_selected_%s" % user.id)

        for sku_id in cart_selected_list:
            while True:
                # 4.1获取商品对象,数量
                sku = SKU.objects.get(id=sku_id)
                count = int(cart_dict[sku_id])

                # 4.2判断库存是否足够
                if count > sku.stock:
                    # TODO 回滚
                    transaction.savepoint_rollback(sid)
                    return http.HttpResponseForbidden("库存不足")

                # TODO 模拟并发下单
                import time
                time.sleep(5)

                # 4.3减少库存,增加销量
                # sku.stock -= count
                # sku.sales += count
                # sku.save()

                # TODO 乐观锁解决并发下单问题
                # 数据准备
                old_stock = sku.stock
                old_sales = sku.sales

                new_stock = old_stock - count
                new_sales = old_sales + count

                # update方法返回的整数,表示影响的行数
                ret = SKU.objects.filter(id=sku_id, stock=old_stock).update(stock=new_stock, sales=new_sales)

                if ret == 0:
                    # transaction.savepoint_rollback(sid) #TODO回滚
                    # return http.HttpResponseForbidden("系统繁忙")
                    continue

                # 4.4设置order信息,累加
                order.total_count += count
                order.total_amount += (count * sku.price)

                # 4.5创建订单商品信息对象
                OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=count,
                    price=sku.price,
                )
                break  # 一定要break

        # 5.提交订单
        order.save()
        transaction.savepoint_commit(sid)  # TODO 提交
        # 6.清空redis中选中的商品
        redis_conn.hdel("cart_%s" % user.id, *cart_selected_list)
        redis_conn.srem("cart_selected_%s" % user.id, *cart_selected_list)

        # 7,返回响应
        context = {
            "code": RET.OK,
            "order_id": order_id,
            "payment_amount": order.total_amount + order.freight,
            "pay_method": pay_method
        }
        return http.JsonResponse(context)


class OrderSuccessView(MyLoginRequiredMiXinView):
    def get(self, request):
        # 1,获取参数
        order_id = request.GET.get("order_id")
        payment_amount = request.GET.get("payment_amount")
        pay_method = request.GET.get("pay_method")

        # 2,拼接数据,渲染页面
        context = {
            "order_id": order_id,
            "payment_amount": payment_amount,
            "pay_method": pay_method,
        }
        return render(request, 'order_success.html', context=context)


class UserOrderInfoView(MyLoginRequiredMiXinView):
    def get(self, request, page_num):
        # 1,查询用户的所有订单
        orders = request.user.orders.order_by("-create_time")

        # 1,1处理支付方式,和状态
        for order in orders:
            order.paymethod_name = OrderInfo.PAY_METHOD_CHOICES[order.pay_method - 1][1]
            order.status_name = OrderInfo.ORDER_STATUS_CHOICES[order.status - 1][1]

        # 2,分页
        paginate = Paginator(object_list=orders, per_page=3)
        page = paginate.page(page_num)
        orders_list = page.object_list  # 当前页对象列表
        current_page = page.number  # 当前页
        total_page = paginate.num_pages  # 总页数

        # 2,携带数据渲染
        context = {
            "orders": orders_list,
            "current_page": current_page,
            "total_page": total_page
        }
        return render(request, 'user_center_order.html', context=context)
