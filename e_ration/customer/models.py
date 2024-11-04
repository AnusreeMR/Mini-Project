from django.db import models

# Create your models here.

class CustomerRegistration(models.Model):
    customer_id = models.AutoField(primary_key=True)
    card_no = models.BigIntegerField()
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    age = models.CharField(max_length=45)
    contact = models.CharField(max_length=45)
    email = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'customer_registration'