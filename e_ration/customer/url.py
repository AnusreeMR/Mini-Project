from django.conf.urls import url
from customer import views

urlpatterns = [

    url('custregister/',views.custreg),
    
]
