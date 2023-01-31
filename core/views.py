from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse
from django.template.context_processors import request

from core.upload import *

def mainOp(request):
	return render(request,'mainOp.html')
def upload(request):
	command = inputCommand()
	
	if command == 'y':
		inputCommand()
	elif command == 'n':
		pass
	else:
		print('异常')
		
		
	

def createPoPayBill(request):
	rangeOfPo = input('请输入单据时间范围，为空则不限制')
	
def showReciptBillItems(request):
	# 获取全部行项目数据
	recList = ReceiptBillItems.objects.all()
	return render(request,'reciptBillItems.html',{"recList":recList})




# 渲染登录页
def login_views(request):
	return render(request,'login.html')
# 处理登录
def manage_login(request):
	user_name = request.GET.get('user_name','')
	pwd = request.GET.get('pwd','')
	
	if user_name == 'xky' and pwd == 'pwd':
		return render(request,'reciptBillItems.html')
	return HttpResponse("用户名或密码错误")
	
	