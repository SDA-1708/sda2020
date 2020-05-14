from django.urls import path

from . import views

app_name = 'HumanResources'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<str:wid>', views.edit, name='edition'),
    path('arrange/', views.arrange, name='arrange'),
    path('delete/<str:wid>', views.delete, name='delete'),
    path('deleteArrange/', views.deleteArrange, name='deleteArrange'),
    path('performance', views.performance, name='performance'),
]
