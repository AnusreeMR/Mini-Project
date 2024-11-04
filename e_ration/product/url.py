from django.conf.urls import url
from product import views

urlpatterns = [
url('search/', views.product_search, name='product_search'),
url('search-ration-shop/', views.search_ration_shop, name='search_ration_shop'),
url('add_to_cart/(?P<idd>\w+)', views.add_to_cart, name='add_to_cart')
]
