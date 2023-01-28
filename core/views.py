from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse
from django.template.context_processors import request

from core.upload import *

def mainOp(request):
	return render(request,'mainOp.html')
def upload(request):
	bizType = input("请选择导入数据类型：")
	path = input("请输入导入文件的路径")
	sheetNo = input("请输入要导入的sheet")
	importData(bizType, path, sheetNo)
	return HttpResponse("上传数据成功")

def createPoPayBill(request):
	rangeOfPo = input('请输入单据时间范围，为空则不限制')
	
def showReciptBillItems(request):
	# 获取全部行项目数据
	recList = ReciptBillItems.objects.all()
	return render(request,'reciptBillItems.html',{"recList":recList})
