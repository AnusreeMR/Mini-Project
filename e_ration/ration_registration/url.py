from django.conf.urls import url
from ration_registration import views

urlpatterns = [

    url('rationregister/',views.rreg),
    url('approve/(?P<idd>\w+)', views.accept, name='approve'),
    #url('reject/(?P<idd>\w+)', views.reject_leave_request, name='reject'),
  #  url('approve/(?p<idd>\w+)',views.approve,name='approve'),
  #  url('view_rationshop')
]