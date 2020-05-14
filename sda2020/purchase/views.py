import datetime
import math
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from purchase.models import Worker, CarPurchase, Batch, CarInfo, CoPurchase, Purchase, Components, WorksheetCompoInfo, \
    FaultInfo, Worksheet, CarShortage
from django.contrib.auth.decorators import login_required

@login_required()
def welcome(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = 'W2003001'
    request.session["w_id"] = w_id
    workerinfo = Worker.objects.filter(wid=w_id).first()
    w_name = workerinfo.wname
    w_dept = workerinfo.dept
    w_post = workerinfo.postion
    context = {
        'w_name' : w_name,
        'w_id' : w_id,
        'w_dept' : w_dept,
        'w_post' : w_post,
    }
    # 主页面设置两个跳转，一个是查看整车采购单，一个查看零件采购单。
    return render(request,'purchase_welcome.html' ,context)

@login_required
def co_purchase(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    com = CoPurchase.objects.filter(purchasestate='已采购未入库')
    works = []
    for i in com:
        m = {}
        m['pid'] = i.purchaseid.purchaseid
        m['pnum'] = i.purchasenum
        m['ptime'] = i.ptime
        m['pstate'] = i.purchasestate
        id = i.purchaseid.purchaseid
        co_names = CoPurchase.objects.filter(purchaseid=id).first()
        co_name = Components.objects.filter(coid=co_names.coid.coid).first()
        m['coname'] = co_name.coname
        works.append(m)
    context = {
        'works': works,
        'w_name': w_name,
    }
    return render(request, 'purchase_co_unco.html', context)
# 已采购未入库
@login_required
def co_confirmed(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    com = CoPurchase.objects.filter(purchasestate='已入库')
    works = []
    for i in com:
        m = {}
        m['pid'] = i.purchaseid.purchaseid
        m['pnum'] = i.purchasenum
        m['ptime'] = i.ptime
        m['pstate'] = i.purchasestate
        id = i.purchaseid.purchaseid
        co_name = i.coid.coname
        m['coname'] = co_name
        works.append(m)
    context = {
        'works': works,
        'w_name': w_name,
    }
    return render(request, 'purchase_co_ed.html', context)
# 已入库
@login_required
def co_unconfirmed(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    com = CoPurchase.objects.filter(purchasestate='未采购')
    works = []
    for i in com:
        m = {}
        m['pid'] = i.purchaseid.purchaseid
        m['pnum'] = i.purchasenum
        m['ptime'] = i.ptime
        m['pstate'] = i.purchasestate
        id = i.purchaseid.purchaseid
        co_names = CoPurchase.objects.filter(purchaseid=id).first()
        co_name = Components.objects.filter(coid=co_names.coid.coid).first()
        m['coname'] = co_name.coname
        works.append(m)
    context = {
        'works':works,
        'w_name': w_name,
    }
    return render(request, 'purchase_co_un.html', context)
# 未采购
@login_required
def car_purchase(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    unpurchase = CarPurchase.objects.filter(purchasestate='已采购未入库')
    works = []
    for i in unpurchase:
        m = {}
        m['pid'] = i.purchaseid.purchaseid
        car_id = i.id.id
        m['car_band'] = CarInfo.objects.filter(id=car_id).first().band
        m['car_type'] = CarInfo.objects.filter(id=car_id).first().ctype
        m['pnum'] = i.purchasenum
        m['ptime'] = i.ptime
        m['pstate'] = i.purchasestate
        works.append(m)
    context = {
        'works': works,
        'w_name': w_name,
    }
    # 零件首页设置为未采购，可跳转到未确认和已确认界面
    return render(request, 'purchase_car_unco.html', context)

@login_required
def car_confirmed(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    unpurchase = CarPurchase.objects.filter(purchasestate='已入库')
    works = []
    for i in unpurchase:
        m = {}
        m['pid'] = i.purchaseid.purchaseid
        car_id = i.id.id
        m['car_band'] = CarInfo.objects.filter(id=car_id).first().band
        m['car_type'] = CarInfo.objects.filter(id=car_id).first().ctype
        m['pnum'] = i.purchasenum
        m['ptime'] = i.ptime
        m['pstate'] = i.purchasestate
        works.append(m)
    context = {
        'works': works,
        'w_name': w_name,
    }
    # 零件首页设置为未采购，可跳转到未确认和已确认界面
    return render(request, 'purchase_car_ed.html', context)

@login_required
def car_unconfirmed(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    unpurchase = CarPurchase.objects.filter(purchasestate='未采购')
    works = []
    for i in unpurchase:
        m = {}
        m['pid'] = i.purchaseid.purchaseid
        car_id = i.id.id
        m['car_band'] = CarInfo.objects.filter(id=car_id).first().band
        m['car_type'] = CarInfo.objects.filter(id=car_id).first().ctype
        m['pnum'] = i.purchasenum
        m['ptime'] = i.ptime
        m['pstate'] = i.purchasestate
        works.append(m)
    context = {
        'works': works,
        'w_name': w_name,
    }
    # 零件首页设置为未采购，可跳转到未确认和已确认界面
    return render(request, 'purchase_car_un.html', context)

@login_required
def co_confirm(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    confirm = CoPurchase.objects.filter(purchaseid=purchaseid).update(purchasestate='已采购未入库')
    Purchase.objects.filter(purchaseid=purchaseid).update(purchasestate='已采购未入库')
    url = reverse('purchase:co_unconfirmed')
    return redirect(url)

@login_required
def co_delete(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    delete = CoPurchase.objects.filter(purchaseid=purchaseid).delete()
    Purchase.objects.filter(purchaseid=purchaseid).delete()
    url = reverse('purchase:co_unconfirmed')
    return redirect(url)

@login_required
def co_modify_page(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    co_purchase = CoPurchase.objects.filter(purchaseid=purchaseid).first()
    work = {}
    co_id = co_purchase.coid.coid
    coinfo = Components.objects.filter(coid=co_id).first()
    work['coname'] = coinfo.coname
    work['pid'] = co_purchase.purchaseid.purchaseid
    work['pnum'] = co_purchase.purchasenum
    work['ptime'] = co_purchase.ptime
    work['pstate'] = co_purchase.purchasestate
    context = {
        'w_name' : w_name,
        'works' : work
    }

    return render(request,'purchase_co_modify.html',context)

@login_required
def co_modify(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    num = request.POST.get('num')
    Purchase.objects.filter(purchaseid=purchaseid).update(purchasenum=int(num))
    CoPurchase.objects.filter(purchaseid=purchaseid).update(purchasenum=int(num))
    url = reverse('purchase:co_unconfirmed')
    return redirect(url)

@login_required
def co_add_page(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    com = Components.objects.all()
    context = {
        'w_name': w_name,
        'com':com
    }
    return render(request,'purchase_co_add.html',context)

@login_required
def co_add(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    date = datetime.datetime.today()
    today = str(date.date())[2:7].replace('-', '')
    pur_id = 'CG02' + today
    sum = Purchase.objects.filter(purchaseid__contains=pur_id).count()
    pur_id = pur_id + '000'
    p_id = 'CG0'+str(int(pur_id[3:])+sum+1)
    purchasenum = request.POST.get('num')
    coid = request.POST.get('co_id')
    comp = Components.objects.get(coid=coid)
    coprice = comp.coprice
    sum_money = float(coprice) * float(purchasenum)
    purchase = Purchase(purchaseid=p_id,purchasenum=purchasenum,purchasestate='未采购',psumprice=sum_money, ptime=date)
    purchase.save()
    purchase_m = Purchase.objects.get(purchaseid=p_id)
    print(purchase_m)
    copurchase = CoPurchase(purchaseid=purchase_m,purchasenum=purchasenum,purchasestate='未采购',psumprice=sum_money, ptime=date,coid=comp)
    copurchase.save()
    url = reverse('purchase:co_unconfirmed')
    print(p_id)
    return redirect(url)

@login_required
def car_confirm(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    confirm = CarPurchase.objects.filter(purchaseid=purchaseid).update(purchasestate='已采购未入库')
    Purchase.objects.filter(purchaseid=purchaseid).update(purchasestate='已采购未入库')
    url = reverse('purchase:car_unconfirmed')
    return redirect(url)

@login_required
def car_delete(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    delete = CarPurchase.objects.filter(purchaseid=purchaseid).delete()
    Purchase.objects.filter(purchaseid=purchaseid).delete()
    url = reverse('purchase:car_unconfirmed')
    return redirect(url)

@login_required
def car_modify_page(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    car_purchase = CarPurchase.objects.filter(purchaseid=purchaseid).first()
    work = {}
    id = car_purchase.id.id
    carinfo = CarInfo.objects.filter(id=id).first()
    work['band'] = carinfo.band
    work['ctype'] = carinfo.ctype
    work['pid'] = car_purchase.purchaseid.purchaseid
    work['pnum'] = car_purchase.purchasenum
    work['ptime'] = car_purchase.ptime
    work['pstate'] = car_purchase.purchasestate
    context = {
        'w_name': w_name,
        'works': work
    }
    return render(request, 'purchase_car_modify.html', context)

@login_required
def car_modify(request, purchaseid):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    num = request.POST.get('num')
    Purchase.objects.filter(purchaseid=purchaseid).update(purchasenum=int(num))
    CarPurchase.objects.filter(purchaseid=purchaseid).update(purchasenum=int(num))
    url = reverse('purchase:car_unconfirmed')
    return redirect(url)

@login_required
def car_add_page(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    car = CarInfo.objects.exclude(ctype='all').all()
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    context = {
        'w_name': w_name,
        'car': car
    }
    return render(request, 'purchase_car_add.html', context)



# 后面还需要一些系统自动的检查函数，就是在一定库存水平下系统会自动检测零件的库存水平并且进行采购单的生成。
# 整车的采购部分则由服务顾问生成。
@login_required
def car_add(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    date = datetime.datetime.today()
    today = str(date.date())[2:7].replace('-', '')
    pur_id = 'CG01' + today
    sum = Purchase.objects.filter(purchaseid__contains=pur_id).count()
    pur_id = pur_id + '000'
    p_id = 'CG0' + str(int(pur_id[3:]) + sum + 1)
    purchasenum = request.POST.get('num')
    cid = request.POST.get('c_id')
    carinfo = CarInfo.objects.get(id=cid)
    price = carinfo.price
    sum_money = float(price) * float(purchasenum)
    purchase = Purchase(purchaseid=p_id, purchasenum=purchasenum, purchasestate='未采购', psumprice=sum_money, ptime=date)
    purchase.save()
    purchase_m = Purchase.objects.get(purchaseid='CG022005001')
    cainfo = CarInfo.objects.get(id=cid)
    print(purchase_m)
    carpurchase = CarPurchase(purchaseid=purchase_m, purchasenum=purchasenum, purchasestate='未采购', psumprice=sum_money, ptime=date, id=cainfo)
    carpurchase.save()
    url = reverse('purchase:car_unconfirmed')
    print(p_id)
    return redirect(url)


@login_required
def component(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    works = Components.objects.all()
    context = {
        'works': works,
        'w_name': w_name,
    }
    return render(request, 'purchase_component.html', context)



@login_required
def car(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    works = CarInfo.objects.all().exclude(ctype='all')
    context = {
        'works': works,
        'w_name': w_name,
    }
    return render(request, 'purchase_car.html', context)

@login_required
def car_out(request):
    if request.user.type != 'purchase':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    works = CarShortage.objects.filter(csstate='未完成')
    context = {
        'works': works,
        'w_name': w_name,
    }
    return render(request, 'purchase_car_out.html', context)