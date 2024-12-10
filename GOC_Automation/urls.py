"""GOC_Automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from mainweb.views import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # default page
    path('', main_views.index),

    # include mainweb app urls
    path('main/', include('mainweb.urls')),

    # include monitoringweb app urls
    path('monitoring/', include('monitoringweb.urls')),

    # include operationweb app urls
    path('operation/', include('operationweb.urls')),

    # include pmcweb app urls
    path('pmc/', include('pmcweb.urls')),

    # include userweb app urls
    path('user/', include('userweb.urls')),

    # include apschedulerweb app urls
    path('', include('apschedulerweb.urls')),
]
