from django.shortcuts import render
from django.views import View
from django import http

from meiduo_mall.utils.response_code import RET
from .models import Area


class AreaView(View):
    def get(self,request):
        #1,获取参数area_id
        area_id = request.GET.get("area_id")

        #2,判断area_id是否有值
        if area_id: #(市,区)

            #3.1 获取上级区域
            area = Area.objects.get(id=area_id)

            #3.2 获取上级区域的子级区域
            sub_data = area.subs.all()

            #3.3 数据转换
            sub_data_list = []
            for sub in sub_data:
                sub_dict = {
                    "id":sub.id,
                    "name":sub.name
                }
                sub_data_list.append(sub_dict)

            #3.4 数据拼接
            context = {
                "code":RET.OK,
                "errmsg":"ok",
                "sub_data":{
                    "id":area.id,
                    "name":area.name,
                    "subs":sub_data_list
                }
            }

            return http.JsonResponse(context)

        else:# (省)

            #4.1 查询数据
            areas =  Area.objects.filter(parent__isnull=True).all()

            #4.2 数据转换
            areas_list = []
            for area in areas:
                area_dict = {
                    "id":area.id,
                    "name":area.name
                }
                areas_list.append(area_dict)

            #4.3 拼接数据
            context = {
                "code":RET.OK,
                "errmsg":"OK",
                "province_list":areas_list
            }

            return http.JsonResponse(context)
