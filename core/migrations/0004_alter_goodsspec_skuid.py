# Generated by Django 4.0.6 on 2023-01-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_supplier_suppliername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsspec',
            name='skuId',
            field=models.CharField(max_length=100, unique=True, verbose_name='商品SKU编码'),
        ),
    ]
