from django.conf.urls import url
from Supplyco_product import views

urlpatterns = [
    url('supplyco_product/', views.Supplyco_product, name='supplyco_product'),  
    url('mscop/', views.mscop, name='mscop'), 
    url('update/(?P<idd>\w+)', views.update),
    url('delete/(?P<idd>\w+)', views.delete, name='ff'),
]
