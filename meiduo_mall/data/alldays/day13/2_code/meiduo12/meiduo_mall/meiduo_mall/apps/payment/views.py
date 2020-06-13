from alipay import AliPay
from django.shortcuts import render
from django import http
from django.views import View
from meiduo_mall.utils.response_code import RET
from django.conf import settings
from orders.models import OrderInfo
from .models import Payment
class AlipayView(View):
    def get(self,request,order_id):

        #0,取出订单对象
        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except Exception as e:
            return http.HttpResponseForbidden('非法请求')

        #1,准备公钥私钥
        app_private_key_string = open(settings.APLIPAY_PRIVATE_KEY).read()
        alipay_public_key_string = open(settings.APLIPAY_PUBLIC_KEY).read()

        #2,创建alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2", # RSA 或者 RSA2
            debug = False  # 默认False
        )

        #3,生成订单字符串
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount + order.freight),
            subject="美多商城订单",
            return_url=settings.ALIPAY_RETURN_URL,
        )

        #4,生成跳转url
        alipay_url = settings.ALIPAY_URL + order_string


        return http.JsonResponse({"code":RET.OK,"alipay_url":alipay_url})

class PaymentStatusView(View):
    def get(self,request):
        #1,获取参数
        dict_data = request.GET.dict()
        sign = dict_data.pop("sign")

        #2,校验参数
        app_private_key_string = open(settings.APLIPAY_PRIVATE_KEY).read()
        alipay_public_key_string = open(settings.APLIPAY_PUBLIC_KEY).read()

        #2,创建alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2", # RSA 或者 RSA2
            debug = False  # 默认False
        )
        success = alipay.verify(dict_data, sign)

        if not success:
            return http.HttpResponseForbidden("非法请求")

        #3,数据入库(payment, status)
        order_id = dict_data.get("out_trade_no")
        trade_id = dict_data.get("trade_no")
        Payment.objects.create(
            order_id=order_id,
            trade_id=trade_id
        )
        OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])

        #4,返回响应
        return render(request,'pay_success.html',context={"trade_id":trade_id})