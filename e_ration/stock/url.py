from django.conf.urls import url
from stock import views

urlpatterns=[
url('add_rp/',views.Rskp),
url('mrp/',views.mrskp),
#url('update_stock/', views.update_stock, name='update_stock'),
url('update/(?P<idd>\w+)', views.update_stock, name='kk'),
url('delete/(?P<idd>\w+)',views.delete,name='cc'),
]