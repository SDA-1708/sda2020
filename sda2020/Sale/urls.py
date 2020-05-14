from django.urls import path

from . import views

app_name = 'Sale'
urlpatterns = [
    path('', views.index, name='index'),
    path('addCustomer/', views.addCustomer, name='addCustomer'),
    path('carInfo/', views.carInfo, name='carInfo'),
    path('carInfo/details/<str:car_id>', views.details, name='details'),
    path('fault/', views.fault, name='fault'),
    path('fault/repairList', views.repairList, name='repairList'),
    path('order/', views.order, name='order'),
    path('order/detail/<str:oid>', views.orderDetails, name='orderDetails'),
    path('order/newOrder', views.newOrder, name='newOrder'),
    path('order/addOrder', views.addOrder, name='addOrder'),
    path('order/buyCar/<str:car_id>', views.buyCar, name='buyCar'),
    path('checkPick', views.checkPick, name='checkPick'),
    path('checkCusno', views.checkCusno, name='checkCusno'),
    path('cusinfo', views.cusinfo, name='cusinfo')
]
