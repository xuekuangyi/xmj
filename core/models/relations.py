from django.db import models
from django.db.models import SET_NULL, PROTECT, CASCADE
from core.models import Store
from core.models import Goods
from core.models.md import GoodsSpec, Supplier


# 门店商品
class StoreGoods(models.Model):
	# 关联门店对象,一个商品可以在多个门店，同个门店也会有多个商品，多对多
	store = models.ForeignKey(verbose_name='门店', to=Store, to_field='storeNo', on_delete=PROTECT)
	# 关联商品
	sku = models.ForeignKey(verbose_name='sku', to=GoodsSpec, to_field='skuId', on_delete=PROTECT)
	retailPrice = models.IntegerField()  # 零售价格，人民币分
	status = models.SmallIntegerField(default=0)  # 状态，需要研究如何设置枚举
	
	infoCreateTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	infoUpdateTime = models.DateTimeField(verbose_name='创建时间', auto_now=True)
	
	class Meta:
		constraints = [models.UniqueConstraint(fields=["store", "sku"], name='门店+商品不重复')]


# 组合商品
class Bom(models.Model):
	storeGoods = models.ForeignKey(verbose_name='商品', to='StoreGoods', related_name='主商品',
	                               on_delete=models.CASCADE)
	# 组件
	unitGoods = models.ForeignKey(verbose_name='子商品', to='StoreGoods', related_name='子商品',
	                              on_delete=models.CASCADE)
	usage = models.FloatField(verbose_name='组件用量')  # 本组件用量


class PurchaseRelations(models.Model):
	relationNo = models.IntegerField(verbose_name='供化关系编码')
	store = models.ForeignKey(verbose_name='门店', to=Store, to_field='storeNo', on_delete=PROTECT)
	supplier = models.ForeignKey(verbose_name='供商', to=Supplier, to_field='supplierNo', on_delete=models.CASCADE)
	arrivalDays = models.IntegerField(verbose_name='到货天数', null=True)
	sku = models.ForeignKey(verbose_name='SKU', to=GoodsSpec, to_field='skuId', on_delete=PROTECT)
	purUnit = models.CharField(verbose_name='采购单位', max_length=50, null=True)
	isDefault = models.CharField(verbose_name='是否默认', max_length=50, null=True)
	purPrice = models.IntegerField(verbose_name='采购价（分）')
