from django.db import models
from django.db.models import SET_NULL, PROTECT


# ============================主数据部分=======================
# 商品
class Goods(models.Model):
	spuId = models.BigIntegerField(verbose_name='商品SPU编码', primary_key=True)  # 商品SPU编码
	goodsName = models.CharField(max_length=255)  # 商品名称

	def __str__(self):
		return u'<Goods:%s>' % self.goodsName


# sku
class GoodsSpec(models.Model):
	
	skuId = models.CharField(verbose_name='商品SKU编码', max_length=100,primary_key=True)  # 商品SKU编码
	goods = models.ForeignKey(verbose_name='商品', to=Goods, to_field='spuId', on_delete=PROTECT)

	upc = models.CharField(verbose_name='国条', max_length=50)
	specName = models.CharField(verbose_name='规格名称',max_length=255)


# 门店
class Store(models.Model):
	# 门店类型，分为自营门店/对标门店等，枚举类型，研究下枚举类型怎么实现
	storeNo = models.IntegerField(verbose_name='门店号',primary_key=True)  # 门店编码
	storeName = models.CharField(max_length=20)  # 门店名称

	storeAddress = models.CharField(verbose_name='门店地址', max_length=255, default='', null=True, blank=True)


# 供商
class Supplier(models.Model):
	supplierNo = models.IntegerField(verbose_name='供商编码',primary_key=True)  # 供商编码
	supplierName = models.CharField(verbose_name='供商名称',max_length=100)  # 供商名称
	deliveryDays = models.IntegerField(verbose_name='到货时间',default=100)  # 送货时间
	paymentByDays = models.IntegerField(verbose_name='账期天数',null=True)  # 账期天数

class Dictionary(models.Model):
	bizType = models.IntegerField(verbose_name='业务类型')
	subNo = models.IntegerField(verbose_name='子编码')
	dictName = models.CharField(verbose_name='枚举值',max_length=100)
	remarks = models.CharField(verbose_name='备注', max_length=255)