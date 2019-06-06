import random
import string

from django.db import transaction
from django.shortcuts import render,HttpResponse,redirect
from userapp.captcha.image import ImageCaptcha
from userapp.models import User


def login(request):
    username=request.COOKIES.get("username")
    if username:
        username=username.encode("latin-1").decode("utf-8")
    pwd=request.COOKIES.get("pwd")
    result=User.objects.filter(username=username,pwd=pwd)
    if result:
        request.session["login"]="ok"
        return redirect("empapp:emplist")
    return render(request,"userapp/login.html")
def loginlogic(request):
    username=request.POST.get("name")
    pwd=request.POST.get("pwd")
    rem=request.POST.get("rember")
    result=User.objects.filter(username=username,pwd=pwd)
    if result:
        res=redirect("empapp:emplist")
        request.session["login"]="ok"
        if rem:
            res.set_cookie("username",username.encode("utf-8").decode("latin-1"), max_age=7 * 24 * 3600)
            res.set_cookie("pwd",pwd,max_age=7*24*3600)
        return res
    return HttpResponse("登录失败")
def regist(request):
    return render(request,"userapp/regist.html")
def getcaptcha(request):
    #构造一个图片验证码的对象
    image=ImageCaptcha()
    rand_code=random.sample(string.ascii_letters+string.digits,5)
    rand_code="".join(rand_code)
    request.session["code"]=rand_code
    print(rand_code,'23行')
    data=image.generate(rand_code)
    return HttpResponse(data,"image/png")
def registlogic(request):
    try:
        with transaction.atomic():
            captcha=request.POST.get("number")
            code=request.session.get("code")
            username=request.POST.get("username")
            name=request.POST.get("name")
            pwd=request.POST.get("pwd")
            pwd1=request.POST.get("pwd1")
            gender=request.POST.get("sex")
            gender=bool(gender)
            if pwd==pwd1:
                if username and captcha and name and pwd and gender:
                    result=User.objects.filter(username=username,pwd=pwd)
                else:
                    return HttpResponse("账号，姓名或密码不能为空")
                if result:
                    return HttpResponse("账号已经存在")
                if captcha.upper() == code.upper():
                    # return HttpResponse("验证码正确")
                    insert=User.objects.create(username=username,name=name,pwd=pwd,gender=gender)
                    if insert:
                        return redirect("userapp:login")
            return HttpResponse("注册失败")
    except:
        return HttpResponse("注册失败")
#onblur时被调用----chenName(){url?username=location.href}
def checkname(request):
    username=request.GET.get("username")
    print(username)
    result = User.objects.filter(username=username)
    if result:
        return HttpResponse("用户名已经存在")
    elif not username:
        return HttpResponse("用户名不能为空")
    else:
        return HttpResponse("用户名合法")
def checkImg(request):
    img=request.GET.get("cig")
    code = request.session.get("code")
    if img.upper() == code.upper():
        return HttpResponse("验证码正确")
    else:
        return HttpResponse("验证码错误")
