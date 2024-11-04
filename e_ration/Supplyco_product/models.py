from django.db import models
from ration_registration.models import Shopkeeper

# Create your models here.

class SupplycoProduct(models.Model):
    supplycoproduct_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shopkeeper, to_field='shop_id', on_delete=models.CASCADE)
    supplycoproduct_name = models.CharField(max_length=100,unique=True)
    expiry_date = models.DateField(db_column='expiry date')  # Field renamed to remove unsuitable characters.
    manufacture_date = models.DateField()
    supplyco_quantity = models.IntegerField()
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'supplyco_product'

