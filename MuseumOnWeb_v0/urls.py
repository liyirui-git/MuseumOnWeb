"""MuseumOnWeb_v0 URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from website import views
from django.views.static import serve

urlpatterns = [
    # 后台管理界面
    path('admin/', admin.site.urls),
    # 用户登录界面
    path('', views.register),
    path('register/', views.register),
    # 文物内容页面
    path('index/', views.index_redirect),
    re_path(r'^index/(?P<info>(.*))/', views.index_addition),
    # 解析显示文物图片
    re_path(r'^img/(?P<path>.*)$', serve, {'document_root': '/home/MuseumOnWeb/'}),
]