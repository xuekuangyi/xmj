from django.db import models
from django.db.models import PROTECT, DO_NOTHING, UniqueConstraint

from core.models import Store, StoreGoods, Supplier, GoodsSpec


# 采购单
class PurchaseOrder(models.Model):
	store = models.ForeignKey(verbose_name='门店', to=Store, to_field='storeNo', on_delete=PROTECT)
	poNo = models.CharField(verbose_name='销售单号', max_length=50, unique=True)
	purPrice = models.BigIntegerField(verbose_name='本次采购价')
	
	realMerTotal = models.IntegerField(verbose_name='商家实收金额')


# 收货单抬头
class ReciptBill(models.Model):
	reciptBillNo = models.CharField(verbose_name='收货单号', max_length=200, primary_key=True)
	store = models.ForeignKey(verbose_name='门店', to='Store', to_field='storeNo', on_delete=PROTECT, default=15307602)
	supplier = models.ForeignKey(verbose_name='供商', to=Supplier, to_field='supplierNo', on_delete=models.CASCADE)
	source = models.CharField(verbose_name='单据来源', max_length=200)
	# 后台要改成对象
	sourceBillNo = models.CharField(verbose_name='来源单号', max_length=200)
	stauts = models.CharField(verbose_name='状态', max_length=200)
	creator = models.CharField(verbose_name='创建人', max_length=100)


# 收货单明细

class ReciptBillItems(models.Model):
	reciptBill = models.ForeignKey(verbose_name='收货单', to=ReciptBill, to_field='reciptBillNo', on_delete=PROTECT)
	sku = models.ForeignKey(verbose_name='SKU', to=GoodsSpec, to_field='skuId', on_delete=PROTECT)
	unit = models.CharField(verbose_name='发货单位', max_length=100)
	
	sendQty = models.FloatField(verbose_name='发货量', default=0)
	netRecQty = models.FloatField(verbose_name='净收货量', default=0)
	recQty = models.FloatField(verbose_name='收货量', default=0)
	grandTotalRefund = models.FloatField(verbose_name='累计退货量', default=0)
	offset = models.FloatField(verbose_name='偏差量', default=0)
	
	# 通过采购关系查找
	actPurchasePrice = models.IntegerField(verbose_name='当前可用采购价（分）', default=0)
	
	purchasePriceByBill = models.IntegerField(verbose_name='单据记录的采购价（分）', default=0)
	purchaseAmount = models.IntegerField(verbose_name='采购总价', default=0)
	netPurchaseAmount = models.IntegerField(verbose_name='净收货总价', default=0)
	receiver = models.CharField(verbose_name='收货人', max_length=100, default='收货人为空')
	# receiveTime = models.DateTimeField(verbose_name='收货时间', null=True, blank=True)
	receiveTime = models.CharField(verbose_name='收货时间', max_length=100, null=True, blank=True)
	
	# 针对可能存在多次导入的场景，所以必须增加联合主键
	class Meta:
		constraints = [models.UniqueConstraint(fields=["reciptBill", "sku", "receiveTime", ], name='收货单+商品不重复')]


# 供商销售单
class supplierSoBill(models.Model):
	billNo = models.CharField(verbose_name='单据号', max_length=100)
	supplier = models.ForeignKey(verbose_name='供商', to=Supplier, to_field='supplierNo', on_delete=PROTECT)
	
	status = models.IntegerField(verbose_name='状态编码')
	billTotalAmount = models.IntegerField(verbose_name='单据总价')
	bizDate = models.DateField(verbose_name='单据日期')


# 	采购付款单
class poPayBill(models.Model):
	# 多对多——合并收货单付款，收货单分次付款
	refReciptBill = models.ManyToManyField(verbose_name='关联收货单号', to=ReciptBill)
	payAmount = models.IntegerField(verbose_name='支付金额（分）')
	payChannel = models.IntegerField(verbose_name='支付渠道')
	payTime = models.DateTimeField(verbose_name='支付时间')


# 付款单明细
class poPayBillItems(models.Model):
	# 多对多——合并收货单付款，收货单分次付款
	refReciptBill = models.ManyToManyField(verbose_name='关联收货单号', to=ReciptBill)
	payAmount = models.IntegerField(verbose_name='支付金额（分）')
	payChannel = models.IntegerField(verbose_name='支付渠道')
	payTime = models.DateTimeField(verbose_name='支付时间')


# 销售单抬头
class SellOrder(models.Model):
	# 销售单号
	soNo = models.CharField(verbose_name='销售单号', max_length=50, unique=True)
	soSn = models.IntegerField(verbose_name='订单序号')
	
	totalAmount = models.IntegerField(verbose_name='订单总金额（分）')
	totalGoodsAmount = models.IntegerField(verbose_name='商品原总价')
	realPayTotal = models.IntegerField(verbose_name='订单实收金额（分）')
	realMerTotal = models.IntegerField(verbose_name='商家实收金额（分）')
	deliveryFee = models.IntegerField(verbose_name='配送费（分）')
	lunchboxFee = models.IntegerField(verbose_name='餐盒费（分）')
	
	platformServiceFee = models.IntegerField(verbose_name='平台服务费（分）')
	merActFee = models.IntegerField(verbose_name='商家活动支出（分）')
	platformActFee = models.IntegerField(verbose_name='平台活动支出（分）')
	
	status = models.CharField(verbose_name='订单状态', max_length=50)
	deliveryStatus = models.CharField(verbose_name='配送状态',max_length=50)
	
	createTime = models.DateTimeField(verbose_name='下单时间')
	finishTime = models.CharField(verbose_name='完成时间', max_length=50)
	refundTime = models.CharField(verbose_name='订单取消时间',max_length=50)

# 销售单明细
class SoDetails(models.Model):
	refSo = models.ForeignKey(verbose_name='所属销售订单号', to=SellOrder, to_field='soNo', on_delete=PROTECT)
	soType = models.CharField(verbose_name='订单类型',max_length=50)
	
	# 需要指向联合主键
	sku = models.ForeignKey(verbose_name='sku', to=StoreGoods, on_delete=PROTECT)
	qty = models.FloatField(verbose_name='销售数量')
	refundQty = models.FloatField(verbose_name='退货数量')
	netQty = models.FloatField(verbose_name='净数量')
	sellPrice = models.FloatField(verbose_name='原售价')
	cost = models.FloatField(verbose_name='成本价')
	purPrice = models.FloatField(verbose_name='下单时采购价')
	
	# 以订单号、sku及数量等来判重
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["refSo", "sku", "qty", "refundQty"], name='订单号+商品+数量不重复')]

# 美团商品对账单（回款）


class checkBillDetails(models.Model):
	sellOrder = models.ForeignKey(verbose_name='销售单', to=SellOrder, to_field='soNo', on_delete=PROTECT)
