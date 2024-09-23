from django.db import models

# Create your models here.

class RationProduct(models.Model):
    rationproduct_id = models.AutoField(db_column='Rationproduct_id', primary_key=True)  # Field name made lowercase.
    card_type = models.CharField(max_length=12)
    card_color = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ration_product'