"""e_ration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url,include
from django.urls import path
from Temp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('login/',include('login.url')),
    url('Temp/',include('Temp.url')),
    url('Ration_product/',include('Ration_product.url')),
    url('Supplyco_product/',include('Supplyco_product.url')),
    url('ration/',include('ration_registration.url')),
    url('User/',include('User.url')),
    url('Cart/',include('Cart.url')),
    url('customer/',include('customer.url')),
    url('stock/',include('stock.url')),
    url('product/',include('product.url')),
    url('$',views.home),
    
]
