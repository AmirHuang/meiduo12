from django.conf.urls import url
from . import views

app_name = 'oauth'
urlpatterns = [
    url(r'^qq/login/$', views.OAuthQQLoginView.as_view()),
    url(r'^oauth_callback/$', views.OAuthUserView.as_view()),
]
