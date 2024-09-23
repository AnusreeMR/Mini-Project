from django.conf.urls import url
from Ration_product import views

urlpatterns=[
    url('Ration_product/',views.Ration_product),
   # url('ms/',views.ms),
   # url('update/(?P<idd>\w+)',views.update,name='upd'),
   # url('delete/(?P<idd>\w+)',views.delete,name='del'),
   # url('ve/',views.vstud)

]