from django.db import models

# Create your models here.
class Shopkeeper(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=40)
    shopkeeper_name = models.CharField(db_column='Shopkeeper_name', max_length=15)  # Field name made lowercase.
    address = models.CharField(max_length=45)
    email = models.CharField(max_length=25)
    muncipality = models.CharField(db_column='Muncipality', max_length=25)  # Field name made lowercase.
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'shopkeeper'