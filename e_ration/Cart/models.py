from django.db import models
from customer.models import CustomerRegistration

# Create your models here.

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerRegistration,to_field='customer_id',on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'cart'