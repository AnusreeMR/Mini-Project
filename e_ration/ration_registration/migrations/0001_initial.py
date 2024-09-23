# Generated by Django 3.2.25 on 2024-09-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shopkeeper',
            fields=[
                ('shop_id', models.IntegerField(primary_key=True, serialize=False)),
                ('shop_name', models.CharField(max_length=40)),
                ('shopkeeper_name', models.CharField(db_column='Shopkeeper_name', max_length=15)),
                ('address', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=25)),
                ('muncipality', models.CharField(db_column='Muncipality', max_length=25)),
                ('status', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'shopkeeper',
                'managed': False,
            },
        ),
    ]