from django.conf.urls import url
from User import views

urlpatterns=[
    url('mu/',views.mu),
    url('update/(?P<idd>\w+)',views.update,name='upd'),
    url('delete/(?P<idd>\w+)',views.delete,name='del'),
    url('ve/',views.vuser)

]