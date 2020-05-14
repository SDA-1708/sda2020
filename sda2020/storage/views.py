import math
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from storage.models import Car, Components, Worker, Pickuplist, CompoUseInfo, Purchase, CarPurchase, CoPurchase, \
    CarInfo, WorksheetCompoInfo, FaultInfo, Worksheet, Batch, CarShortage


@login_required
def welcome(request):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})

    w_id = 'W2004001'
    request.session["w_id"] = w_id
    workerinfo = Worker.objects.filter(wid=w_id).first()
    w_name = workerinfo.wname
    w_dept = workerinfo.dept
    w_post = workerinfo.postion
    context = {
        'w_name': w_name,
        'w_id': w_id,
        'w_dept': w_dept,
        'w_post': w_post,
    }
    return render(request, 'storage_welcome.html', context)

@login_required
def pickup(request):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfo = Worker.objects.filter(wid=w_id).first()
    w_name = workerinfo.wname
    pickuplist = Pickuplist.objects.filter(pickstate='未提车')
    works = []
    for i in pickuplist:
        m={}
        m['pickid'] = i.pickid
        m['pickstate'] = i.pickstate
        m['cusno'] = i.cusno.cusno
        c_id = i.cid.cid
        m['cid'] = c_id
        cin_id = Car.objects.filter(cid=c_id).first().id.id
        c_info = CarInfo.objects.filter(id=cin_id).first()
        m['cband'] = c_info.band
        m['ctype'] = c_info.ctype
        works.append(m)
    context = {
        'w_name': w_name,
        'works' : works,
    }
    return render(request, 'storage_pickup.html', context)

@login_required
def co_use(request):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfo = Worker.objects.filter(wid=w_id).first()
    w_name = workerinfo.wname
    co_use = CompoUseInfo.objects.filter(compo_use_state='未领取')
    workers = []
    for i in co_use:
        m={}
        m['wsid'] = i.wsid.wsid
        m['compo_use_state'] = i.compo_use_state
        ws_id = i.wsid.wsid
        fault = WorksheetCompoInfo.objects.filter(wsid=ws_id)
        faults = []
        for j in fault:
            component = {}
            repeat = Worksheet.objects.filter(wsid=ws_id).first().repeatnum
            fainfo_id = j.faultinfoid.faultinfoid
            fainfo = FaultInfo.objects.filter(faultinfoid=fainfo_id).first()
            co_id = fainfo.coid.coid
            co = Components.objects.filter(coid=co_id).first()
            co_name = co.coname
            co_num = fainfo.renum * repeat
            component['coname'] = co_name
            component['conum'] = co_num
            faults.append(component)
        m['com'] = faults
        workers.append(m)
    context = {
        'w_name': w_name,
        'works': workers,
    }
    return render(request, 'storage_couse.html', context)

@login_required
def copurchase(request):
    if request.user.type != 'storage':
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
    return render(request, 'storage_co_unco.html', context)

@login_required
def carpurchase(request):
    if request.user.type != 'storage':
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
    return render(request, 'storage_car_unco.html', context)

@login_required
def component(request):
    if request.user.type != 'storage':
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
    return render(request, 'storage_component.html', context)

@login_required
def batch(request):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    batch_info = Batch.objects.filter(remainnum__gt=0)
    works = []
    for i in batch_info:
        m = {}
        m['id'] = i.id
        m['remainnum'] = i.remainnum
        co_id = i.coid.coid
        purid = i.purchaseid.purchaseid
        m['purid'] = purid.purchaseid
        coname = Components.objects.filter(coid=co_id).first().coname
        ptime = CoPurchase.objects.filter(purchaseid=purid).first().warehouse_time
        m['coname'] = coname
        m['ptime'] = ptime
        works.append(m)
    context = {
        'works': works,
        'w_name': w_name,
    }
    return render(request, 'storage_batch.html', context)

@login_required
def car(request):
    if request.user.type != 'storage':
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
    return render(request, 'storage_car.html', context)

@login_required
def co_confirm(request, ws_id):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    com = CompoUseInfo.objects.filter(wsid=ws_id).update(compo_use_state='已领取')
    url = reverse('storage:co_use')
    return redirect(url)

@login_required
def co_unconfirm(request):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    com = Components.objects.all()
    return HttpResponse('未确认零件')

@login_required
def car_confirm(request, pick_id):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    car = Pickuplist.objects.filter(pickid=pick_id).update(pickstate='已提车')
    url = reverse('storage:pickup')
    return redirect(url)

@login_required
def car_unconfirm(request):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    car = Car.objects.all()
    return None

@login_required
def co_in(request, pid):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    time = timezone.now()
    Purchase.objects.filter(purchaseid=pid).update(purchasestate='已入库', warehouse_time=time)
    CoPurchase.objects.filter(purchaseid=pid).update(purchasestate='已入库', warehouse_time=time)
    purchase = CoPurchase.objects.get(purchaseid=pid)
    purchasenum = purchase.purchasenum
    coid = purchase.coid
    tot_num = coid.conumber + purchasenum
    co_id = coid.coid
    Components.objects.filter(coid=co_id).update(conumber=tot_num)
    copurchase = CoPurchase.objects.get(purchaseid=pid)
    batch = Batch(coid=coid,purchaseid=copurchase,remainnum=purchasenum)
    batch.save()
    worksheet = worksheet_co_serach(coid)
    check_worksheet(worksheet)
    url = reverse('storage:co_purchase')
    return redirect(url)

# 输入一个零件查询，根据这个零件查询返回一个需要这个零件的派工单查询列表
def worksheet_co_serach(coid):
    worksheet_out = Worksheet.objects.filter(wsstate='缺货')
    fault_info_co = FaultInfo.objects.filter(coid=coid)
    worksheet = []
    for i in worksheet_out:
        worksheet_info = WorksheetCompoInfo.objects.filter(wsid=i)
        for j in worksheet_info:
            if j.faultinfoid in fault_info_co:
                worksheet.append(i)
    return worksheet

# 传入派工单列表，将能维修的派工单维修，不能维修的不变。返回已经更改状态的派工单列表。
def check_worksheet(worksheet):
    if len(worksheet) == 0:
        return []
    else:
        has_change = []
        for i in worksheet:
            com_use = WorksheetCompoInfo.objects.filter(wsid=i)
            num = i.repeatnum
            state = True
            for j in com_use:
                faultinfo = j.faultinfoid
                co_id = faultinfo.coid.coid
                renum = faultinfo.renum
                total = int(renum) * int(num)
                left = Components.objects.get(coid=co_id).conumber
                if total > left:
                    state = False
                    break
            if state:
                ws_id = i.wsid
                Worksheet.objects.filter(wsid=ws_id).update(wsstate='未完成')
                has_change.append(i)
                work_sheet = Worksheet.objects.get(wsid=ws_id)
                compoUseInfo = CompoUseInfo(wsid=work_sheet, compo_use_state='未领取')
                compoUseInfo.save()
            for k in com_use:
                faultinfo = k.faultinfoid
                co_id = faultinfo.coid.coid
                renum = faultinfo.renum
                total = int(renum) * int(num)
                left = Components.objects.get(coid=co_id).conumber
                left_co = left - total
                Components.objects.filter(coid=co_id).update(conumber=left_co)
                batches = Batch.objects.filter(coid=co_id).order_by('id').exclude(remainnum=0)
                for m in batches:
                    if total <= 0:
                        break
                    else:
                        if m.remainnum < total:
                            total -= total - m.remainnum
                            id = m.id
                            Batch.objects.filter(id=id).update(remainnum=0)
                        else:
                            batch_left = m.remainnum - total
                            total = 0
                            id = m.id
                            Batch.objects.filter(id=id).update(remainnum=batch_left)
        print(has_change)
        return has_change

@login_required
def car_in(request, pid):
    if request.user.type != 'storage':
        return render(request,'confirm.html',{'message':'账号无权限'})
    time = timezone.now()
    Purchase.objects.filter(purchaseid=pid).update(purchasestate='已入库', warehouse_time=time)
    CarPurchase.objects.filter(purchaseid=pid).update(purchasestate='已入库')
    purchase = CarPurchase.objects.get(purchaseid=pid)
    purchasenum = purchase.purchasenum
    car_info = purchase.id
    tot_num = car_info.inventory + purchasenum
    id = car_info.id
    CarInfo.objects.filter(id=id).update(inventory=tot_num)
    tot = Car.objects.all().count()
    for i in range(0,purchasenum):
        cid = 'C' + '0'*(4-len(str(tot)))+ str(tot)
        i_d = CarInfo.objects.get(id=id)
        car = Car(cid=cid, id=i_d)
        car.save()
        tot += 1
    change = check_car(id)
    url = reverse('storage:car')
    return redirect(url)


def check_car(id):
    carinfo = CarInfo.objects.get(id=id)
    inventory = int(carinfo.inventory)
    shortage = CarShortage.objects.filter(id=carinfo)
    change = []
    for i in shortage:
        carinfo = CarInfo.objects.get(id=id)
        if inventory <= 0 :
            break
        else:
            CarInfo.objects.filter(id=id).update(inventory=inventory-1)
            cusno = i.cusno
            car_shortage_id = i.car_shortage_id
            i_d = carinfo
            realprice = i.appo_price
            CarShortage.objects.filter(car_shortage_id=car_shortage_id).update(csstate='已完成')
            car = Car.objects.filter(id=i_d).filter(real_price__isnull=True).first()
            cid = car.cid
            Car.objects.filter(cid=cid).update(real_price=realprice)
            pnum = str(Pickuplist.objects.all().count())
            pickid ='P' + '0'*(4-len(pnum)) + pnum
            picklist = Pickuplist(pickid=pickid, cusno=cusno, cid=car, pickstate='未提车')
            picklist.save()
            change.append(picklist)
    return change






