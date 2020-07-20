from django.shortcuts import render
from django.views import View
from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView


class OrderSettlementView(MyLoginRequiredMiXinView):
    def get(self, request):

        # 1,查询用户的地址
        try:
            addresses = request.user.addresses.filter(is_deleted=False).all()
        except Exception as e:
            addresses = None

        # 2,拼接数据,返回响应
        context = {
            "addresses": addresses
        }
        return render(request, 'place_order.html', context=context)
