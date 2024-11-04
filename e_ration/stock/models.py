from django.db import models
from Ration_product.models import RationProduct
from ration_registration.models import Shopkeeper

# Create your models here.

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shopkeeper, to_field='shop_id', on_delete=models.CASCADE)
    rationproduct = models.ForeignKey(RationProduct,to_field='rationproduct_id',on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock'