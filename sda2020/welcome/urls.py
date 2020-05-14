#_author:'Palau'
#date:2020/4/2

from django.urls import path
from . import views
from django.conf.urls import url
from django.urls import include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

app_name='welcome'
urlpatterns = [
    url(r'index/', views.index, name='index'),
    url(r'about/', views.about, name='about'),
    url(r'blog/', views.blog, name='blog'),
    url(r'contact/', views.contact, name='contact'),
    url(r'gallery/', views.gallery, name='gallery'),
    url(r'services/', views.services, name='services'),
    url(r'search/',views.search, name='search'),
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'captcha',include('captcha.urls')),
    # url(r'^index/', views.index, name='index'),
    url(r'logout/', views.logout, name='logout'),
    url(r'reset_psd/', views.reset_psd, name='reset_psd'),
    url(r'reset_psd_email/', views.reset_psd_email, name='reset_psd_email'),
    url(r'reset_psd_send/', views.reset_psd_send, name='reset_psd_send'),
    url(r'reset_psd_post/', views.reset_psd_post, name='reset_psd_post'),
    url(r'home/', views.home, name='home'),
    url(r'confirm/', views.user_confirm, name='user_confirm'),
    path("carinfo/details/<int:car_id>", views.details, name='details'),
    url(r'appo/',views.appo,name='appo'),
    url(r'gettouch',views.touch,name='touch')
    #url(r'^searchresult/', views.searchresult, name='searchresult'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
