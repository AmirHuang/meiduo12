"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('users.urls', namespace="user")),
    url(r'^', include('verifications.urls', namespace="verifications")),
    url(r'^', include('contents.urls', namespace="contents")),
    url(r'^', include('oauth.urls', namespace="oauth")),
    url(r'^', include('areas.urls', namespace="areas")),
    url(r'^', include('goods.urls', namespace="goods")),
    url(r'^search/', include('haystack.urls')),
    url(r'^', include('carts.urls', namespace="carts")),
    url(r'^', include('orders.urls')),
]
