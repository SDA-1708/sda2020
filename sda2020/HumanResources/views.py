from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .models import Worker
# Create your views here.
from .models import WorkerArrange
from .models import ServiceWorker
from .models import MaintenanceWorker
from .forms import *
import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import time
@login_required()
def index(request):
    if request.user.type != 'HR':
        return render(request,'HumanResources/confirm.html',{'message':'账号无权限'})
    # print(request.user.customer)
    workers_all = Worker.objects.all()
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    work_info = WorkerArrange.objects.filter(timeatwork__gte=monday, timeatwork__lte=sunday)
    time_now = datetime.datetime.now()
    arrangement=[]
    a_m=[]
    a_a=[]
    for day in range(7):
        workers_curr_m = []
        workers_curr_a = []
        day_cur = sunday - day * one_day
        for worker in work_info:
            if worker.timeatwork.date() == day_cur:
                if str(worker.timeatwork.time()) == '09:30:00':
                    workers_curr_m.append(worker)
                else:
                    workers_curr_a.append(worker)
        a_a.append(workers_curr_a)
        a_m.append(workers_curr_m)
    a_m.reverse()
    a_a.reverse()
    arrangement.append(a_m)
    arrangement.append(a_a)
    # print(arrangement)
    # Warrangment=WorkerArrange.objects.filter(appostate="已预约")

    return render(request, 'HumanResources/index.html',
                  {'workers': workers_all, 'arrangement': arrangement, 'today': time_now.date()})
    # pass

@login_required
def add(request):
    if request.user.type != 'HR':
        return render(request,'HumanResources/confirm.html',{'message':'账号无权限'})
    if request.method == "POST":  # 这里POST一定要大写
        # 通常获取请求信息
        # print(request.POST)
        form = AddForm(request.POST)
        if form.is_valid():
            new_number = form.cleaned_data["inputNumber"]
            new_name = form.cleaned_data["inputName"]
            new_dept = form.cleaned_data["inputDept"]
            new_po = form.cleaned_data["inputPostion"]

            # print(new_number)
            Worker.objects.create(wid=new_number, wname=new_name, dept=new_dept, postion=new_po)
            return render(request, 'HumanResources/success.html', {"success_inform": "添加成功", "result": 'success'})
        else:
            return render(request, 'HumanResources/success.html', {"success_inform": "添加失败", "result": 'fail'})
    else:
        newform = AddForm()
    return render(request, 'HumanResources/add.html', {"form": newform})

@login_required
def edit(request, wid):
    if request.user.type != 'HR':
        return render(request,'HumanResources/confirm.html',{'message':'账号无权限'})
    worker_edited = Worker.objects.get(pk=wid)
    if request.method == "POST":  # 这里POST一定要大写
        # 通常获取请求信息
        worker_edited.wname = request.POST.get("inputName", None)
        worker_edited.dept = request.POST.get("inputDept", None)
        worker_edited.postion = request.POST.get("inputpostion", None)
        worker_edited.save()
        return render(request, 'HumanResources/success.html', {"success_inform": "修改成功","result":'success'})
    else:
        return render(request, 'HumanResources/edit.html', {"worker_edited": worker_edited})

@login_required
def arrange(request):
    if request.user.type != 'HR':
        return render(request,'HumanResources/confirm.html',{'message':'账号无权限'})
    if request.method == 'POST':
        workers=ServiceWorker.objects.all().values_list('wid',flat=True)
        wid=request.POST.get('inputNumber','')

        if wid not in workers:
            return render(request,'HumanResources/success.html', {"success_inform": "该员工不存在，或不是销售人员","result":'fail'})
        worker = Worker.objects.get(wid=wid)
        worktime=request.POST.get('worktime','')
        time_ms=request.POST.get('time','')
        # date=datetime.datetime.today()
        # print(type(worktime)) #str
        time_tuple = time.strptime(worktime, "%m/%d/%Y")
        year, month, day = time_tuple[:3]
        if time_ms == "上午":
            a_date = datetime.datetime(year, month, day, 9, 30,0)
        else:
            a_date = datetime.datetime(year, month, day, 14, 30,0)


        #检查是否冲突
        arrangements = WorkerArrange.objects.filter(timeatwork=a_date).values_list('wid',flat=True)
        print(arrangements)
        print(wid)
        if wid in arrangements:
            return render(request,'HumanResources/success.html', {"success_inform": "该员工已经被安排在该时段，不可重复安排","result":'fail'})

        #新建记录
        id_now = WorkerArrange.objects.last()
        id_new=str(int(id_now.id)+1)

        WorkerArrange.objects.create(id=id_new,timeatwork=a_date,appostate='空闲',wid=worker)
        return render(request,'HumanResources/success.html', {"success_inform": "添加成功","result":'success'})

@login_required
def deleteArrange(request):
    if request.user.type != 'HR':
        return render(request, 'HumanResources/confirm.html', {'message': '账号无权限'})

    if request.method == 'POST':
        id = request.POST.get('id', '')
        today=datetime.datetime.today()
        print(request.POST)
        if id != '':
            arrangement=WorkerArrange.objects.get(id=id)

            if arrangement.timeatwork.date() < today.date():
                return HttpResponse('{"status":"late"}', content_type='application/json')
            else:
                arrangement.delete()
                return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"信息为空"}', content_type='application/json')


@login_required
def delete(request, wid):
    if request.user.type != 'HR':
        return render(request,'HumanResources/confirm.html',{'message':'账号无权限'})
    Worker.objects.get(wid=wid).delete()
    return render(request, 'HumanResources/success.html', {"success_inform": "删除成功"})

@login_required
def performance(request):
    if request.user.type != 'HR':
        return render(request,'HumanResources/confirm.html',{'message':'账号无权限'})
    server= ServiceWorker.objects.all()
    repairer=MaintenanceWorker.objects.all()
    return render(request, 'HumanResources/performance.html', {"servers":server,"repairers":repairer})