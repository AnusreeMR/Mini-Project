from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    card_id = models.BigIntegerField()
    email = models.CharField(max_length=50)
    card_type = models.CharField(max_length=10)
    card_color = models.CharField(max_length=10)
    head_name = models.CharField(max_length=45)
    annual_income = models.IntegerField()
    occupation = models.CharField(max_length=45)
    age = models.IntegerField()
    no_of_family_member = models.IntegerField()
    no_of_adults = models.IntegerField()
    no_of_family_children = models.IntegerField()
    address = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'user'