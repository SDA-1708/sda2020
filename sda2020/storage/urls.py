# -*- coding:utf-8 -*-
from django.urls import path

from storage import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('pickup/', views.pickup, name='pickup'),
    path('couse/', views.co_use, name='co_use'),
    path('co_purchase/', views.copurchase, name='co_purchase'),
    path('car_purchase/', views.carpurchase, name='car_purchase'),
    path('component/', views.component, name='component'),
    path('batch/', views.batch, name='batch'),
    path('car/', views.car, name='car'),
    path('co_confirm/<str:ws_id>', views.co_confirm, name='co_confirm'),
    path('co_unconfirm', views.co_unconfirm),
    path('car_confirm/<str:pick_id>', views.car_confirm, name='car_confirm'),
    path('car_unconfirm', views.car_unconfirm),
    path('co_in/<str:pid>',views.co_in, name='co_in'),
    # url(r'confirm/', views.confirm, name='confirm'),
    path('car_in/<str:pid>',views.car_in, name='car_in'),
]