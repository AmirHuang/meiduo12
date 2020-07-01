from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from goods.models import GoodsCategory, SKU
from meiduo_mall.utils.my_category import get_categories
from django import http

# from meiduo_mall.utils.my_crumbs import get_crumbs
import time
from datetime import datetime

from meiduo_mall.utils.response_code import RET


class SkuListView(View):
    def get(self, request, category_id, page_num):

        # 1,获取分类信息,获取参数
        categories = get_categories()
        sort = request.GET.get("sort", "default")

        # 1.1 根据sort设置排序方式
        if sort == "price":
            sort_field = "-price"
            sort = "price"
        elif sort == "hot":
            sort_field = "-sales"
            sort = "hot"
        else:
            sort_field = "-create_time"
            sort = "default"

        # 2,获取分类对象
        category = GoodsCategory.objects.get(id=category_id)

        # 3,分页查询
        skus = SKU.objects.filter(category_id=category_id).order_by(sort_field)
        paginator = Paginator(object_list=skus, per_page=5)  # 创建分类对象,每页5条
        page = paginator.page(page_num)  # 获取page_num页
        skus_list = page.object_list  # 获取page_num中的所有的对象
        current_page = page.number  # 当前页
        total_page = paginator.num_pages  # 总页数

        # 拼接数据,返回响应
        context = {
            "categories": categories,
            "category": category,
            "skus_list": skus_list,
            "current_page": current_page,
            "total_page": total_page,
            "sort": sort
        }

        return render(request, 'list.html', context=context)


class HotSkuListView(View):
    def get(self, request, category_id):
        # 1,根据销量获取两个sku对象
        skus = SKU.objects.filter(category_id=category_id).order_by("-sales")[:3]

        # 2,拼接数据
        hot_sku_list = []
        for sku in skus:
            sku_dict = {
                "id": sku.id,
                "default_image_url": sku.default_image_url.url,
                "name": sku.name,
                "price": sku.price
            }
            hot_sku_list.append(sku_dict)

        # 3,返回响应
        return http.JsonResponse({"hot_sku_list": hot_sku_list})
