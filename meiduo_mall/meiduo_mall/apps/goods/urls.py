# _*_ coding: utf-8 _*_
# @time     : 2020/06/22
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.conf.urls import url
from . import views

app_name = 'goods'
urlpatterns = [
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$',views.SkuListView.as_view()),
    url(r'^hot/(?P<category_id>\d+)/$',views.HotSkuListView.as_view()),
    # url(r'^detail/(?P<sku_id>\d+)/$',views.SKUDetailView.as_view()),
    # url(r'^detail/visit/(?P<category_id>\d+)/$',views.GoodsVisitView.as_view()),
]