# Generated by Django 3.2.25 on 2024-10-20 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('cart_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('date_added', models.DateField()),
            ],
            options={
                'db_table': 'cart_product',
                'managed': False,
            },
        ),
    ]
