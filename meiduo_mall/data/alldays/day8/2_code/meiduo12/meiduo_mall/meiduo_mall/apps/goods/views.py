from django.shortcuts import render
from django.views import View

from goods.models import GoodsCategory
from meiduo_mall.utils.my_category import get_categories


class SkuListView(View):
    def get(self,request,category_id,page_num):

        #1,获取分类信息
        categories = get_categories()

        #2,获取分类对象
        category = GoodsCategory.objects.get(id=category_id)

        #拼接数据,返回响应
        context = {
            "categories":categories,
            "category":category
        }

        return render(request,'list.html',context=context)
