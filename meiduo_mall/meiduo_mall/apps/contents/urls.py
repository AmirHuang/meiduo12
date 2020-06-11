from django.conf.urls import url
from . import views

app_name = 'contents'

urlpatterns = [
    url(r'^$', views.IndexView.as_view())
]
