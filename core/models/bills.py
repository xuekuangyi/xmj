from django.db import models
from django.db.models import PROTECT, DO_NOTHING, UniqueConstraint

from core.models import Store, StoreGoods, Supplier, GoodsSpec, PurchaseRelations


# 预留的超类或抽象类
class Bill(models.Model):
	store = models.ForeignKey(verbose_name='门店', to=Store, to_field='storeNo', on_delete=PROTECT)
	billNo = models.CharField(verbose_name='单据号', max_length=100)
	createTime = models.CharField(verbose_name='单据创建时间', max_length=100)
	status = models.CharField(verbose_name='单据状态', max_length=100)


# 采购单
class PurchasePlan(models.Model):
	store = models.ForeignKey(verbose_name='门店', to=Store, to_field='storeNo', on_delete=PROTECT)
	planNo = models.CharField(verbose_name='销售单号', max_length=50, primary_key=True)


class PurchasePlanItems(models.Model):
	purchasePlan = models.ForeignKey(verbose_name='po单', to=PurchasePlan, to_field='planNo',on_delete=PROTECT)
	sku = models.ForeignKey(verbose_name='sku', to=GoodsSpec, to_field='skuId', on_delete=PROTECT)
	unit = models.CharField(verbose_name='采购单位', max_length=100)
	
	supplier = models.ForeignKey(verbose_name='供商', to=Supplier, to_field='supplierNo', on_delete=models.CASCADE)
	
	purQty = models.FloatField(verbose_name='采购数量')
	purPrice = models.IntegerField(verbose_name='采购单价(分)')
	purAmount = models.IntegerField(verbose_name='采购金额小计（分）')
	
	status = models.SmallIntegerField(verbose_name='采购商品状态')
	
	receiptQty = models.FloatField(verbose_name='实收数量')
	offset = models.FloatField(verbose_name='差异数量')
	
	createTime = models.CharField(verbose_name='订单创建时间',max_length=50)
	
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["purchasePlan", "sku" ], name='采购计划单+商品不重复')]
	


# 收货单抬头
class ReceiptBill(models.Model):
	receiptBillNo = models.CharField(verbose_name='收货单号', max_length=200, primary_key=True)
	store = models.ForeignKey(verbose_name='门店', to='Store', to_field='storeNo', on_delete=PROTECT)
	supplier = models.ForeignKey(verbose_name='供商', to=Supplier, to_field='supplierNo', on_delete=models.CASCADE)
	source = models.CharField(verbose_name='单据来源', max_length=200)
	# 后台要改成对象
	sourceBillNo = models.CharField(verbose_name='来源单号', max_length=200)
	stauts = models.CharField(verbose_name='状态', max_length=200)
	creator = models.CharField(verbose_name='创建人', max_length=100)


# 收货单明细
class ReceiptBillItems(models.Model):
	receiptBill = models.ForeignKey(verbose_name='收货单', to=ReceiptBill, to_field='receiptBillNo', on_delete=PROTECT)
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
		constraints = [
			models.UniqueConstraint(fields=["receiptBill", "sku", "receiveTime", ], name='收货单+商品不重复')]


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
	refReceiptBill = models.ManyToManyField(verbose_name='关联收货单号', to=ReceiptBill)
	payAmount = models.IntegerField(verbose_name='支付金额（分）')
	payChannel = models.IntegerField(verbose_name='支付渠道')
	payTime = models.DateTimeField(verbose_name='支付时间')


# 付款单明细
class poPayBillItems(models.Model):
	# 多对多——合并收货单付款，收货单分次付款
	refReceiptBill = models.ManyToManyField(verbose_name='关联收货单号', to=ReceiptBill)
	payAmount = models.IntegerField(verbose_name='支付金额（分）')
	payChannel = models.IntegerField(verbose_name='支付渠道')
	payTime = models.DateTimeField(verbose_name='支付时间')


# 销售单抬头
class SellOrder(models.Model):
	store = models.ForeignKey(verbose_name='门店', to='Store', to_field='storeNo', on_delete=PROTECT, default=1031328)
	soNo = models.CharField(verbose_name='销售单号', max_length=50, primary_key=True)
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
	deliveryStatus = models.CharField(verbose_name='配送状态', max_length=50)
	
	createTime = models.DateTimeField(verbose_name='下单时间')
	finishTime = models.CharField(verbose_name='完成时间', max_length=50)
	refundTime = models.CharField(verbose_name='订单取消时间', max_length=50)


# 销售单明细
class SoDetails(models.Model):
	refSo = models.ForeignKey(verbose_name='所属销售订单号', to=SellOrder, to_field='soNo', on_delete=PROTECT)
	
	# 商品
	sku = models.ForeignKey(verbose_name='sku', to=GoodsSpec, to_field='skuId', on_delete=PROTECT)
	upc = models.CharField(verbose_name='UPC', max_length=100)
	specName = models.CharField(verbose_name='规格名称', max_length=100)
	unitName = models.CharField(verbose_name='单位名称', max_length=100)
	# 数量
	qty = models.FloatField(verbose_name='销售数量')
	isRefundGoods = models.CharField(verbose_name='是否为退款商品', max_length=100)
	refundQty = models.FloatField(verbose_name='退货数量')
	netQty = models.FloatField(verbose_name='净数量')
	# 价格及成本
	sellGoodsPrice = models.IntegerField(verbose_name='商品原销售单价（分）')
	# refPurRela = models.ForeignKey(verbose_name='关联供货关系', to=PurchaseRelations,on_delete=PROTECT)
	# refGoodsCost = models.IntegerField(verbose_name='关联供货关系价格',default=0)
	# 收入及补贴
	goodsSellAmount = models.IntegerField(verbose_name='原售价销售额小计(分)')
	goodsRealPayAmount = models.IntegerField(verbose_name='商品实付金额（分）')
	goodsRefundAmount = models.IntegerField(verbose_name='退款商品金额（分）')
	goodsPerkTotalAmount = models.IntegerField(verbose_name='商品总补贴金额（分）')
	goodsPerkMerAmount = models.IntegerField(verbose_name='商品商家补贴金额 (分)')
	goodsPerkPlatformAmount = models.IntegerField(verbose_name='商品平台补贴金额 (分)')
	
	refundTime = models.CharField(verbose_name='退款时间', max_length=100)
	
	# 以订单号、sku及数量等来判重
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["refSo", "sku", "qty", "goodsPerkTotalAmount", "refundQty"],
			                        name='订单号+商品+数量不重复')]


# 美团商品对账单（回款）
class checkBillDetails(models.Model):
	sellOrder = models.ForeignKey(verbose_name='销售单', to=SellOrder, to_field='soNo', on_delete=PROTECT)
