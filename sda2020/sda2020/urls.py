"""sda2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('welcome/',include(('welcome.urls','welcome'),namespace='welcome')),
    path('repair/', include(('repair.urls', 'repair'), namespace='repair')),
    path('purchase/', include(('purchase.urls', 'purchase'), namespace='purchase')),
    path('storage/', include(('storage.urls', 'storage'), namespace='storage')),
    path('PersonalCenter/',include(('login.urls','login'),namespace='login')),
    path('HumanResources/', include(('HumanResources.urls','HumanResources'),namespace='HumanResources')),
    path('Finance/', include(('Finance.urls','Finance'),namespace='Finance')),
    path('Sale/', include(('Sale.urls','Sale'),namespace='Sale')),
    path('admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    # path('HumanResources/', include('HumanResources.urls')),
    # path('Finance/', include('Finance.urls')),
    # path('Sale/', include('Sale.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
