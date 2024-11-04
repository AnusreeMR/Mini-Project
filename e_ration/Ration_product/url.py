from django.conf.urls import url
from Ration_product import views

urlpatterns=[
    url('Ration_product/',views.Ration_product),
    url('update/(?P<rationproduct_id>\w+)',views.update),
    url('delete/(?P<rationproduct_id>\w+)',views.delete,name='bb'),
    url('mrp/',views.mrp),
    url('vcard/',views.vcard, name='vcard')
]