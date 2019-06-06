import os
import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect


# Create your views here.
from empapp.models import Employee

def emplist(request):
    number=request.GET.get("number")
    if not number:
        number=1
    emp=Employee.objects.all()
    print(emp.count(),"17行")
    pagtor=Paginator(emp,per_page=3)
    if not request.session.get("num"):
        page = pagtor.page(number)
    else:
        del request.session["num"]
        number = int(emp.count() / 3) + 1
        print(number, "22行")
        page = pagtor.page(number)
    return render(request,"empapp/emplist.html",{"page":page,"number":number})

def addEmp(request):
    number=request.GET.get(("number"))
    return render(request,"empapp/addEmp.html",{"number":number})
def addEmplogic(request):
    try:
        with transaction.atomic():
            number=request.GET.get("number")
            request.session["num"]=number
            name=request.POST.get("name")
            salary=request.POST.get("salary")
            age=request.POST.get("age")
            headpic=request.FILES.get("headpic")
            if name and age and salary and headpic:
                ext = os.path.splitext(headpic.name)[1]  # 后缀名
                headpic.name = str(uuid.uuid4()) + ext
                insert = Employee.objects.create(name=name, salary=salary, age=age, headpic=headpic)
            elif name and age and salary:
                insert = Employee.objects.create(name=name, salary=salary, age=age, headpic="无")
            elif name and age:
                insert = Employee.objects.create(name=name,age=age, salary=0, headpic="无")
            elif name:
                insert = Employee.objects.create(name=name, salary=0, age=0, headpic="无")
            else:
                return HttpResponse("姓名不能为空")
            if insert:
                return redirect("empapp:emplist")
    except:
        return HttpResponse("提交失败")
def deleteEmplogic(request):
    try:
        with transaction.atomic():
            id=request.GET.get("id")
            number=request.GET.get("number")
            e=Employee.objects.all().count()
            if e % 3 == 1 and int(number)>1:
                number =int(number)-1
                print(number, "71行")
            print(e,"62行")
            print(number,"63行")
            emp=Employee.objects.filter(id=id)
            em=emp[0]
            Employee.objects.get(id=em.id).delete()

            return redirect("/empapp/emplist/?number={}".format(number))
    except:
        return HttpResponse("删除失败")
def updateEmp(request):
    id=request.GET.get("id")
    number=request.GET.get("number")
    emp=Employee.objects.filter(id=id)
    em=emp[0]
    return render(request,"empapp/updateEmp.html",{"em":em,"number":number})
def updateEmplogic(request):
    try:
        with transaction.atomic():
            id=request.GET.get("id")
            number=request.GET.get("number")
            name = request.POST.get("name")
            print(name)
            salary = request.POST.get("salary")
            age = request.POST.get("age")
            headpic = request.FILES.get("headpic")
            emp = Employee.objects.filter(id=id)
            em = emp[0]
            print(em.id)
            if headpic:
                ext = os.path.splitext(headpic.name)[1]  # 后缀名
                headpic.name = str(uuid.uuid4()) + ext
                print(headpic.name)
                em.headpic = headpic
            if name:
                em.name=name
            else:
                return HttpResponse("姓名不能为空")
            if salary:
                em.salary=salary
            else:
                em.salary=0
            if age:
                em.age=age
            else:
                em.age=0
            em.save()
            request.session["number"]=number
            print(number,"96行")
            return redirect("/empapp/emplist/?number={}".format(number))
    except:
        return HttpResponse("修改失败")
def index(request):
    return render(request,"empapp/index.html")
def query(request):
    data=request.GET.get("data")
    # pwd=request.GET.get("password")
    print(data,"122行")
    def mydefault(u):
        if isinstance(u,Employee):
            return {"id":u.id,"name":u.name,"salary":str(u.salary),"age":u.age,"headpic":str(u.headpic)}
    if data:
        users=Employee.objects.filter(name__icontains=data)
        print(users,"128行")
    else:
        users=Employee.objects.all()
    return JsonResponse({"users":list(users)},json_dumps_params={"default":mydefault})

