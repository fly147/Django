"""ReadNews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from DBCtl import views as dbviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/insert',dbviews.article_insert),
    path('article/select/page',dbviews.article_select_page),
    path('article/select/id',dbviews.article_select_id),
    path('article/update/',dbviews.article_update),
    path('article/delete',dbviews.article_delete),
    path('newstype/add',dbviews.newstype_add),
    path('newstype/select',dbviews.newstype_select),
    path('news/add',dbviews.news_add_typeid),
    path('news/select',dbviews.news_select_typeid),
    path('newsdetail/add',dbviews.newsdetail_add_newsid),
    path('newsdetail/select',dbviews.newsdetail_select_newsid),
    path('user/add',dbviews.user_add),
    path('user/login',dbviews.user_login),
    path('user/select',dbviews.user_select),
    path('user/update',dbviews.user_update)
]
