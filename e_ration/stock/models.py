from django.db import models
from Ration_product.models import RationProduct

# Create your models here.

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    #rationproduct_id = models.IntegerField()
    rationproduct = models.ForeignKey(RationProduct,to_field='rationproduct_id',on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    stock_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock'