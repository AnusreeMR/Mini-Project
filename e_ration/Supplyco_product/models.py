from django.db import models

# Create your models here.

class SupplycoProduct(models.Model):
    supplycoproduct_id = models.AutoField(primary_key=True)
    supplycoproduct_name = models.CharField(max_length=100)
    expiry_date = models.DateField(db_column='expiry date')  # Field renamed to remove unsuitable characters.
    manufacture_date = models.DateField()
    quantity = models.IntegerField()
    actual_price = models.IntegerField()
    available_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supplyco_product'