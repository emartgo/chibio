# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getSysdata/', views.getSysdata, name='getSysdata'),
]
