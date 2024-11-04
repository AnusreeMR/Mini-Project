from django.db import models
from stock.models import Stock
from ration_registration.models import Shopkeeper
from Supplyco_product.models import SupplycoProduct
from Ration_product.models import RationProduct

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock,to_field='stock_id',on_delete=models.CASCADE)
    shop = models.ForeignKey(Shopkeeper,to_field='shop_id',on_delete=models.CASCADE)
    supplycoproduct = models.ForeignKey(SupplycoProduct,to_field='supplycoproduct_id',on_delete=models.CASCADE)
    rationproduct = models.ForeignKey(RationProduct, to_field='rationproduct_id', on_delete=models.CASCADE)  # Add this line

    class Meta:
        managed = False
        db_table = 'product'
