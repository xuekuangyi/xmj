# Generated by Django 4.0.6 on 2023-01-27 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_reciptbill_reciptbillitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bizType', models.IntegerField(verbose_name='业务类型')),
                ('subNo', models.IntegerField(verbose_name='子编码')),
                ('dictName', models.CharField(max_length=100, verbose_name='枚举值')),
                ('remarks', models.CharField(max_length=255, verbose_name='备注')),
            ],
        ),
        migrations.RenameField(
            model_name='reciptbillitems',
            old_name='shop',
            new_name='store',
        ),
        migrations.CreateModel(
            name='ReciptBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciptBillNo', models.CharField(max_length=200, verbose_name='收货单号')),
                ('source', models.CharField(max_length=200, verbose_name='单据来源')),
                ('sourceBillNo', models.CharField(max_length=200, verbose_name='来源单号')),
                ('stauts', models.CharField(max_length=200, verbose_name='状态')),
                ('creator', models.CharField(max_length=100, verbose_name='创建人')),
                ('store', models.ForeignKey(default=15307602, on_delete=django.db.models.deletion.PROTECT, to='core.store', to_field='storeNo', verbose_name='门店')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.supplier', to_field='supplierNo', verbose_name='供商')),
            ],
        ),
    ]
