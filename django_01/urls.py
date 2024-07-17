"""
URL configuration for django_01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import reverse
from django.shortcuts import HttpResponse
from django.urls import include

import home.views
from book import views


def index(request):
    # print(reverse("book_detail"))
    # print(reverse("book_str",kwargs={"book_id":1}))
    print(reverse("movie:movie_list"))
    return HttpResponse('欢迎欢迎')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book', views.book_detail_query_string, name='book_detail'),
    path('book/<int:book_id>', views.book_detail_path),
    path('book/str/<path:book_id>', views.book_detail_str, name="book_str"),
    # path('', index,name='index'),

    path('', home.views.index),
    path('baidu', home.views.baidu),
    path('info', home.views.info, name='info'),
    path('if', home.views.if_view, name='if_view'),
    path('with', home.views.with_view, name='with'),
    path('url', home.views.url_view, name='url'),
    path('book/<book_id>', home.views.book_detail, name='book_detail'),
    path('filter', home.views.filter_view, name='filter'),

    path('movie/', include("movie.urls"))
]
