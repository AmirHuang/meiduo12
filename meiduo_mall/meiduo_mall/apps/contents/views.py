from django.shortcuts import render
from django.views import View

from contents.models import ContentCategory
from goods.models import GoodsChannel
from meiduo_mall.utils.my_category import get_categories


class IndexView(View):
    def get(self, request):
        # 1,获取分类信息
        categories = get_categories()

        # 4,拼接广告数据
        contents = {}
        content_catetories = ContentCategory.objects.all()
        for content_catetory in content_catetories:
            contents[content_catetory.key] = content_catetory.content_set.order_by('sequence')

        # 5,拼接数据,返回响应
        context = {
            "categories": categories,
            "contents": contents
        }

        return render(request, 'index.html', context=context)
