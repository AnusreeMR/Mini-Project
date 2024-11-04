from django.db import models
from Supplyco_product.models import SupplycoProduct
from ration_registration.models import Shopkeeper
from customer.models import CustomerRegistration
from Cart.models import Cart

# Create your models here.

class CartProduct(models.Model):
    cart_product_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart,to_field='cart_id',on_delete=models.CASCADE)
    supplycoproduct = models.ForeignKey(SupplycoProduct,to_field='supplycoproduct_id',on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shop = models.ForeignKey(Shopkeeper,to_field='shop_id',on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerRegistration,to_field='customer_id',on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'cart_product'