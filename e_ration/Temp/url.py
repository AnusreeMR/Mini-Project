from django.conf.urls import url
from Temp import views

urlpatterns=[
    url('home/',views.home),
    url('admin/',views.admin),
    url('reg/',views.register),
    url('user/',views.customer),
    url('shopkeeper/',views.shopkeeper)
]