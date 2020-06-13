from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$',views.IndexView.as_view()),
    #获取网站logo
    # url(r'^favicon.ico$',RedirectView.as_view(url='static/favicon.ico')),
    url(r'^favicon.ico$',RedirectView.as_view(url='static/mei_duo_logo.ico'))

]