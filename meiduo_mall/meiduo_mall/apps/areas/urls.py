from django.conf.urls import url
from . import views

app_name = 'areas'
urlpatterns = [
    url(r'^areas/$', views.AreaView.as_view())
]
