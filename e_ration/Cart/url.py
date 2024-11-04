from django.conf.urls import url
from Cart import views

urlpatterns = [
url('view_cart/', views.view_cart, name='view_cart'),
url('remove_from_cart/(?P<idd>\w+)',views.remove_from_cart, name='remove_from_cart'),
url('increase_quantity/(?P<idd>\w+)', views.increase_quantity, name='increase_quantity'),
url('decrease_quantity/(?P<idd>\w+)', views.decrease_quantity, name='decrease_quantity'),
url('shopkeeper_cart/', views.shopkeeper_cart, name='shopkeeper_cart'),
url('checkout/', views.checkout, name='checkout'),
]
