# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from blueking.component.shortcuts import get_client_by_request
from .decotators.decorator import *
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
# def home(request):
#     """
#     首页
#     """
#     return render(request, 'home_application/index_home.html')
# def dev_guide(request):
#     """
#     开发指引
#     """
#     return render(request, 'home_application/dev_guide.html')
# def contact(request):
#     """
#     联系页
#     """
#     return render(request, 'home_application/contact.html')

def index(request):
    """
    首页
    """
    return render(request,'home_application/index.html')

@auto_session
def result(request):
    """
    详情
    """
    return render(request,'home_application/result.html')

def login_verify(request):
    """
    用户登录验证
    """
    #获取用户登录信息
    username = request.POST.get("username")
    password = request.POST.get('password')
    print(username, password)
    #数据库信息
    user = User.objects.filter(username=username).first()
    #校验
    if user:
        if username != user.username:
            return JsonResponse({"msg": "用户名不存在", "flag": 1})
        if password != user.password:
            return JsonResponse({"msg": "密码错误", "flag": 2})
        request.session["loginflag"] = {"username": user.username, "userid": user.id}

        return JsonResponse({"msg": "登陆成功", "flag": 3})
    return JsonResponse({"msg": "用户名不存在", "flag": 1})

@auto_session
def server_verify(request):
    """
    服务器验证
    """
    #获取服务器信息
    serverip = request.POST.get("serverip")
    servername = request.POST.get("servername")
    serverpassword = request.POST.get('serverpassword')
    flag = request.POST.get('flag')
    print(serverip, servername, serverpassword)

    #验证
    server = ServerInfo.objects.filter(serverip=serverip).first()
    if server:
        if serverip != server.serverip:
            return JsonResponse({"flag": 1})
        if servername != server.servername:
            return JsonResponse({"flag": 2})
        if serverpassword != server.serverpassword:
            return JsonResponse({"flag": 3})
        request.session["loginflag2"] = {"serverip": server.serverip, "serverid": server.id,"servername":servername,"serverpassword":serverpassword,"flag":1}

        return JsonResponse({})
    return JsonResponse({"flag": 1})

def get_cpu(request):
    serveriofo = request.session.get("loginflag2")
    bk_token = request.COOKIES.get("bk_token")
    print(bk_token,serveriofo)
    # api连接
    client = get_client_by_request(request)
    app_code = client.app_code  # 用户ID
    app_secret = client.app_secret  # 用户密钥
    # 请求参数
    kwargs = {
        "bk_app_code": app_code,
        "bk_app_secret": app_secret,
        "bk_token": bk_token,
        "ip": {
            "data": [serveriofo["serverip"]],
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_name"
        },
        "pattern": ""
    }
    # 响应结果
    data = client.cc.search_host(**kwargs)
    info = data["data"]["info"][0]["host"]
    print(info)
    return JsonResponse(info)