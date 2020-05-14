# -*- coding:utf-8 -*-
from django.urls import path

from purchase import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('co_purchase/', views.co_purchase, name='co_purchase'),
    path('co_purchase/confirmed', views.co_confirmed, name='co_confirmed'),
    path('co_purchase/unconfirmed', views.co_unconfirmed, name='co_unconfirmed'),
    path('car_purchase/', views.car_purchase, name='car_purchase'),
    path('car_purchase/confirmed', views.car_confirmed, name='car_confirmed'),
    path('car_purchase/unconfirmed', views.car_unconfirmed, name='car_unconfirmed'),
    path('co_purchase/confirm/<str:purchaseid>', views.co_confirm, name='co_confirm'),
    path('co_purchase/delete/<str:purchaseid>', views.co_delete, name='co_delete'),
    path('co_purchase/modify_page/<str:purchaseid>/', views.co_modify_page, name='co_modify'),
    path('co_purchase/modify/<str:purchaseid>', views.co_modify, name='co_change'),
    path('co_purchase/co_add_page/', views.co_add_page , name='co_add_page'),
    path('co_purchase/co_add/', views.co_add , name='co_add'),
    path('car_purchase/confirm/<str:purchaseid>', views.car_confirm, name='car_confirm'),
    path('car_purchase/delete/<str:purchaseid>', views.car_delete, name='car_delete'),
    path('car_purchase/modify_page/<str:purchaseid>/', views.car_modify_page, name='car_modify'),
    path('car_purchase/modify/<str:purchaseid>/', views.car_modify, name='car_change'),
    path('car_purchase/car_add_page/', views.car_add_page, name='car_add_page'),
    path('car_purchase/car_add/', views.car_add, name='car_add'),
    path('component/', views.component, name='component'),
    path('car/', views.car, name='car'),
    path('car_out/', views.car_out, name='car_out'),

]