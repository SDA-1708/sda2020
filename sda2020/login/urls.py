from django.urls import path

from . import views

app_name = 'personalCenter'
urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.order, name='order'),
    path('order/detail/<str:oid>', views.orderDetails, name='orderDetails'),
    path('carInfo/', views.carInfo, name='carInfo'),
]
