# -*- coding:utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path('un_worksheet/', views.un_wroksheet, name='un_worksheet'),
    path('ed_worksheet/', views.ed_wroksheet, name='ed_worksheet'),
    path('out_worksheet/', views.out_wroksheet, name='out_worksheet'),
    path('welcome/', views.welcome, name='welcome'),
    path('welcome/user/', views.userinfo, name='user'),
    path('worksheet/info/<str:ws_id>', views.worksheetinfo, name='worksheet_info'),
    path('worksheet/new_fault/<str:ws_id>', views.new_fault, name='new_fault'),
    path('worksheet/new_fault/add/<str:ws_id>', views.worksheetadd, name='new_fault_add'),
    path('worksheet/new_fault/confirm/<str:ws_id>/<int:num>', views.new_fault_confirm, name='new_fault_confirm'),
    path('worksheet/confirm/<str:ws_id>', views.worksheetconfirm, name='confirm'),
    path('worksheet/back/<str:ws_id>', views.back, name='back'),
]