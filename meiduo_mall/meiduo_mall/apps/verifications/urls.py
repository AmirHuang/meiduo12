from django.conf.urls import url
from . import views
app_name = 'verifications'
urlpatterns = [
    url(r'^image_codes/(?P<image_code_id>.+)/$', views.ImageCodeView.as_view()),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),
]
