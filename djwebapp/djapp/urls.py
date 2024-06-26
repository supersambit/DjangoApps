"""
URL configuration for djwebapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('add_user', views.add_user, name='add_user'),
    path('add_record', views.add_record, name='add_record'),
    path('records', views.records, name='records'),
    path('check_out', views.check_out, name='check_out'),
    path('bill_out', views.bill_out, name='bill_out'),
    path('change_password', views.change_password, name='change_password'),
]
