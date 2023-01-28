import os

import openpyxl
from django.db import IntegrityError
from openpyxl import load_workbook

from core.models import *
import datetime


# 文件导入功能

# `models.GoodsCost.objects.filter(soNo=800290872520005250).values('soNo')[1]['soNo']`

# 获取成本的方法
def getCost(sku, timeRegion):
	pass


# 读取excel方法读取调用时指定文件及sheet号，返回sheet_obj对象——一个可迭代的对象
def readExcel(path, sheetNo):
	# 获取文件对象
	file_path = os.path.join(path)  # 只能用绝对路径，如何解决？
	# Workbook就是一个excel文档对象
	wb_obj = load_workbook(file_path)
	print("文件读取成功")
	# 获取sheet对象
	sheet_obj = wb_obj.worksheets[int(sheetNo)]  # 再定位到某个sheet，并实例化一个sheet对象
	return sheet_obj


def createExcelFile(sheetName):
	wb_obj = openpyxl.Workbook()
	sheet = wb_obj.active
	sheet.title = f"{sheetName}"
	


def importData(bizType, path, sheetNo):

	# 获取到要被上传的sheet对象
	sheet_obj = readExcel(path, sheetNo)
	print(sheet_obj)
	# 对该对象进行逐行循环遍历，赋值给对应的数据库表；
	for row in sheet_obj.iter_rows(min_row=2):

		# 判断业务类型为1，则为导入供商数据
		if bizType == '1':
			Supplier.objects.create(
				supplierNo=row[0].value,
				supplierName=row[1].value,
				deliveryDays=row[5].value
			)
			
		# 判断业务类型为2时，导入
		elif bizType == '2':
			pass
		

		# 判断业务类型为3时，导入门店商品数据，门店商品数据会向Goods和GoodsSpec对象中拆分
		elif bizType == '3':
			# print("正常进入类型3")
			# 将数据导入到商品表
			
				try:
					Goods.objects.create(
						spuId=row[2].value,
						goodsName=row[4].value
					)
					
					# 注意区分querySet和实例
					# print(Goods.objects.filter(spuId=row[2].value).first())
				except IntegrityError as error:
					pass
					# print(f'重复SPU{row[2]}')
			
				GoodsSpec.objects.create(
					goods=Goods.objects.filter(spuId=row[2].value).first(),
					skuId=row[3].value,
					upc=row[20].value,
					specName=row[7].value
				)
				try:
					StoreGoods.objects.create(
						store=Store.objects.filter(storeNo=1031328).first(),
						# 只负责第一次处理
						sku=GoodsSpec.objects.filter(skuId=row[3].value).first(),
						retailPrice=int(float(row[14].value) * 1000),
						status=0,
						infoCreateTime=0,
						infoUpdateTime=0
					
					)
				except ValueError as error:
					if row[14].value == '':
						print(f'{row[14]}售价未配置')
						StoreGoods.objects.create(
							store=Store.objects.filter(storeNo=1031328).first(),
							# 只负责第一次处理
							sku=GoodsSpec.objects.filter(skuId=row[3].value).first(),
							retailPrice=0,
							status=0,
							infoCreateTime=0,
							infoUpdateTime=0
						
						)
		
		# 判断业务类型为4时，组合商品导入
		elif bizType == '4':
			try:
				Bom.objects.create(
				storeGoods=StoreGoods.objects.filter(sku=row[3].value).first(),
				unitGoods=StoreGoods.objects.filter(sku=row[9].value).first(),
				usage=float(row[14].value)

				)
			
			except IntegrityError as error:
				pass
				# print(row[3].value)
				# print(row[9].value)
			
		# 判断业务类型为5时，导入商品供货关系；
		elif bizType == '5':
			PurchaseRelations.objects.create(
				relationNo=int(row[0].value),
				store=Store.objects.filter(storeNo=row[1].value).first(),
				supplier=Supplier.objects.filter(supplierNo=row[3].value).first(),
				arrivalDays=row[5].value,
				sku=GoodsSpec.objects.filter(skuId=row[8].value).first(),
				purUnit=row[10].value,
				isDefault=row[14].value,
				purPrice=int(float(row[15].value)*100)
			)
		
		# 采购单
		elif bizType == '10':
			pass
		
		
		# 收货单抬头
		elif bizType == '12':
			try:
				ReciptBill.objects.create(
					reciptBillNo=row[0].value,
					store = Store.objects.filter(storeName=row[1].value).first(),
					supplier = Supplier.objects.filter(supplierName=row[2].value).first(),
					source = row[3].value,
					sourceBillNo = row[4].value,
					stauts=row[5].value,
					creator=row[10].value
				)
			except IntegrityError as error:
				print(f'找不到供商或“发货方”不为供商:{row[2].value}')
		
		# 收货单明细
		elif bizType == '13':
			# 只导入收货单状态为“已完成”的收货单的明细
			try:
				if ReciptBill.objects.filter(reciptBillNo=row[0].value).exists() and ReciptBill.objects.filter(reciptBillNo=row[0].value).first().stauts == '已完成':
				# if row[3].value == '采购单':
					ReciptBillItems.objects.create(
						reciptBill=ReciptBill.objects.filter(reciptBillNo=row[0].value).first(),
						sku=GoodsSpec.objects.filter(skuId=row[4].value).first(),
						unit=row[8].value,
						sendQty=row[9].value,
						netRecQty=row[11].value,
						recQty=row[12].value,
						grandTotalRefund=row[13].value,
						offset=row[14].value,
						actPurchasePrice=PurchaseRelations.objects.filter(sku=GoodsSpec.objects.filter(skuId=row[4].value).first()).first().purPrice,
						purchasePriceByBill=int(float(row[15].value)*100),
						purchaseAmount=int(float(row[16].value)*100),
						netPurchaseAmount=int(float(row[18].value)*100),
						receiver=row[20].value,
						receiveTime=row[21].value
					)
				else:
					print(f'{row[0].value}未完成或未开始收货')
			except ValueError as error01:
				print(f'数据异常ValueError【{error01}】,单据号:{row[0].value},发货方:{row[2].value}，单据类型{row[3].value}')
			except IntegrityError as error02:
				# print(f'数据异常IntegrityError,【{error02}】|单据号:{row[0].value}|,发货方:{row[2].value}|，单据类型{row[3].value}|,净收货量{row[11].value}')
				print(f'{row[0].value}已关单且本行商品{row[5].value}无净收货|,发货方:{row[2].value}|，单据类型{row[3].value}|,净收货量{row[11].value}')
			except AttributeError as error03:
				print(f'数据异常AttributeError,【{error03}】|单据号:{row[0].value},发货方{row[2].value}|，单据类型{row[3].value}|,净收货量{row[11].value}')

		
		
		
		# 判断业务类型，如果为15，则为导入销售订单抬头
		elif bizType == '15':
			# 转义订单状态
			if row[21] == "已完成":
				transfer = 3
			# 导入销售单抬头：
			SellOrder.objects.create(
				soNo=row[0].value,
				status=transfer,
				createTime=datetime.datetime.strptime(row[25], "%Y-%m-%d %H-%M-%S"),
				finishTime=datetime.datetime.strptime(row[27], "%Y-%m-%d %H-%M-%S"),
				totalAmount=row[8].value,
				realPayTotal=row[10].value,
				realMerTotal=row[11].value,
				deliveryFee=row[12].value,
				lunchboxFee=row[13].value,
				mtServiceFee=row[14].value,
				merActFee=row[15].value,
				mtActFee=row[16].value
			)


		# 判断业务类型如果为16，则为导入销售订单明细
		elif bizType == '16':
			# 导入销售商品明细
		
			SoDetails.objects.create(
				refSo=row[2].value,
				sku=row[18].value,
				qty=row[25].value,
				refundQty=row[33].value,
				netQty=row[25].value - row[33].value,
				sellPrice=row[26].value,
				cost=getCost(row[18], SellOrder.objects.filter(soNo=row[2].value).createTime),
				purPrice=row[26].value  # 百川此处有bug，未能正确记录下单时商品售价，其实是需要去主数据中查询下单时刻的售价

			)
			
		
			
			
