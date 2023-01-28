# Generated by Django 4.0.6 on 2023-01-27 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_reciptbillitems_reciptbill_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReciptBill',
            fields=[
                ('reciptBillNo', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='收货单号')),
                ('source', models.CharField(max_length=200, verbose_name='单据来源')),
                ('sourceBillNo', models.CharField(max_length=200, verbose_name='来源单号')),
                ('stauts', models.CharField(max_length=200, verbose_name='状态')),
                ('creator', models.CharField(max_length=100, verbose_name='创建人')),
                ('store', models.ForeignKey(default=15307602, on_delete=django.db.models.deletion.PROTECT, to='core.store', to_field='storeNo', verbose_name='门店')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.supplier', to_field='supplierNo', verbose_name='供商')),
            ],
        ),
        migrations.CreateModel(
            name='ReciptBillItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=100, verbose_name='发货单位')),
                ('sendQty', models.FloatField(default=0, verbose_name='发货量')),
                ('netRecQty', models.FloatField(default=0, verbose_name='净收货量')),
                ('recQty', models.FloatField(default=0, verbose_name='收货量')),
                ('grandTotalRefund', models.FloatField(default=0, verbose_name='累计退货量')),
                ('offset', models.FloatField(default=0, verbose_name='偏差量')),
                ('actPurchasePrice', models.IntegerField(default=0, verbose_name='当前可用采购价（分）')),
                ('purchasePriceByBill', models.IntegerField(default=0, verbose_name='单据记录的采购价（分）')),
                ('purchaseAmount', models.IntegerField(default=0, verbose_name='采购总价')),
                ('netPurchaseAmount', models.IntegerField(default=0, verbose_name='净收货总价')),
                ('receiver', models.CharField(default='收货人为空', max_length=100, verbose_name='收货人')),
                ('receiveTime', models.CharField(blank=True, max_length=100, null=True, verbose_name='收货时间')),
                ('reciptBill', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.reciptbill', verbose_name='收货单')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.goodsspec', to_field='skuId', verbose_name='SKU')),
            ],
        ),
    ]
