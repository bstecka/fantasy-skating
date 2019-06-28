"""fantasyskating URL Configuration

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
from django.conf.urls import url, include
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import path
from scoring import views
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('ranking/<int:page>', views.ranking, name='ranking'),
    path('ranking/last/<int:page>', views.ranking_last, name='ranking_last'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.user_page, name='profile'),
    #path('choice/', views.choice_form, name='choice_form_'),
    path('event/<str:event_path>', views.choice_form, name='choice_form'),
    path('', views.choice_form_next, name='choice_form_next'),
    path('index/', views.choice_form_next, name='choice_form_next'),
]
