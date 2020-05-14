import math

from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import Customer
# Create your views here.
from .models import FaultList, CoPurchase, Purchase
from .models import FaultInfo
from .models import Components
from .models import Pickuplist
from .models import Orders
from .models import Worksheet
from .models import WorksheetCompoInfo
from .models import MaintenanceWorker ,ServiceWorker
from .models import Batch
from .models import CarInfo,CarShortage,Car
from .models import CompoUseInfo
from .models import AppoInfo,WorkerArrange,Worker
from django.db.models import Q
from .forms import *
import datetime
import json
import re
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
@login_required
def index(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    sale_worker=request.user.username
    date=datetime.datetime.today()
    #找到所有，该员工被预约，且是今天级以后的记录，按时间排序
    appos=WorkerArrange.objects.filter(wid=sale_worker,appostate='已预约',timeatwork__gte=date).order_by('-timeatwork')
    appoment=[]

    for appo in appos:
        a=AppoInfo.objects.get(id=appo.id)
        appoment.append(a)

    #找到自己负责的，未回访的内容
    orders=Orders.objects.filter(ostate='已完成',return_info__isnull=True,wid=sale_worker)
    return render(request, 'Sale/index.html',{"appoment":appoment,"orders":orders})

@login_required
def appo(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    return render(request, 'Sale/appointment.html')

@login_required
def cusinfo(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    if request.method =="POST":
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            cusno = form.cleaned_data["inputNumber"]
            cus=Customer.objects.get(cusno=cusno)
            cars = Pickuplist.objects.filter(cusno=cusno)
            repairs = {}
            pick={}
            for c in cars:
                pick[c.pickid]=Pickuplist.objects.get(cid=c.cid,cusno=cus.cusno).pickid
                worksheets_c = Worksheet.objects.filter(pickid=c.pickid)
                repairs[c.pickid] = 0
                repairs[c.pickid] = 0
                for ws in worksheets_c:
                    repairs[c.pickid] += 1
            return render(request, 'Sale/cusinfo.html', {"cus": cus, "form": form,"cars":cars, "repairs": repairs,"pick":pick})
    form=CustomerInfoForm()
    cus = Customer.objects.get(cusno=int(1))
    cars = Pickuplist.objects.filter(cusno=cus.cusno)
    repairs = {}
    pick={}
    for c in cars:
        pick[c.pickid] = Pickuplist.objects.get(cid=c.cid, cusno=cus.cusno).pickid
        worksheets_c = Worksheet.objects.filter(pickid=c.pickid)
        repairs[c.pickid] = 0
        repairs[c.pickid] = 0
        for ws in worksheets_c:
            repairs[c.pickid] += 1
    return render(request, 'Sale/cusinfo.html',{"cus":cus,"form":form,"cars":cars, "repairs": repairs,"pick":pick})

@login_required
def addCustomer(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    cus_curr = Customer.objects.last()
    number_curr = int(cus_curr.cusno)
    number_curr += 1
    new_cusno =str(number_curr)
    if request.method == "POST":  # 这里POST一定要大写
        # 通常获取请求信息
        print(request.POST)
        form = AddCustomerForm(request.POST)
        # print(form)
        if form.is_valid():
            # new_number = form.cleaned_data["inputNumber"]
            new_name = form.cleaned_data["inputName"]
            new_gender = form.cleaned_data["inputGender"]
            new_tel = form.cleaned_data["inputTel"]
            new_address = form.cleaned_data["inputAddress"]
            new_email = form.cleaned_data["inputEmail"]

            Customer.objects.create( cname=new_name, cgender=new_gender,
                                    tel=new_tel, email=new_email, caddress=new_address)
            return render(request, 'Sale/success.html', {"success_inform": "添加成功", "result": 'success'})
        else:
            return render(request, 'Sale/success.html', {"success_inform": "添加失败", "result": 'fail'})
    else:
        newform = AddCustomerForm()
    return render(request, 'Sale/addCustomer.html', {"form": newform, "cusno": new_cusno})

@login_required
def carInfo(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    carlist = CarInfo.objects.all().exclude(ctype='all')
    return render(request, 'Sale/carInfo.html', {"carlist": carlist})

@login_required
def details(request, car_id):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    carinfo = CarInfo.objects.get(id=car_id)
    return render(request, 'Sale/details.html', {'carinfo': carinfo})

@login_required
def buyCar(request ,car_id):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    if request.method == 'POST':
        carinfo = CarInfo.objects.get(id=car_id)
        print(request.POST.get("inputNumber"))
        cusno = int(request.POST.get("inputNumber",None))
        aprice = request.POST.get("Realprice", 0)
        if carinfo.inventory == 0:  # 售罄,生成整车缺货单
            id_curr=CarShortage.objects.last()
            id_last= int(id_curr.car_shortage_id[2:])
            id="NC"+str(id_last+1)
            date=datetime.datetime.today()
            CarShortage.objects.create(Car_Shortage_id=id,ct_date=date,cusno=Customer.objects.get(cusno=cusno),id=car_id,appo_price=aprice,csstate='未完成')
            return render(request, 'Sale/success.html', {"success_inform": "交易成功！请耐心等待您的爱车到货","result":'success'})
        else: #生成提车单
            id_curr=Pickuplist.objects.last()
            pid_last = int(id_curr.pickid[1:])
            pid_last += 1
            if pid_last // 1000 == 0:
                # print(number_curr)
                new_pid = "P0" + str(pid_last)
            else:
                new_pid = "P" + str(pid_last)
            cars_buyable = Car.objects.filter(id=car_id, real_price__isnull=True)[0]  # 未出售的该种汽车
            cars_buyable.real_price=aprice
            Pickuplist.objects.create(pickid=new_pid,pickstate='未提车',cid=cars_buyable,cusno=Customer.objects.get(cusno=cusno))
            cars_buyable.save()
            return render(request, 'Sale/success.html', {"success_inform": "交易成功！请提车","result":'success'})


@login_required
def fault(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    if request.method =="POST":
        pid = request.POST.get("inputNumber", None)
        request.session["pickid"] = pid
        car = Pickuplist.objects.get(pickid=pid)
        band = car.cid.id.band
        faults = FaultList.objects.filter(Q(Fa_id="all")|Q(Fa_id=CarInfo.objects.filter(band=band).get(ctype='all').id))
        return render(request, 'Sale/fault.html', {"faults": faults})
    else:
        pid =request.session.get("pickid")
        request.session["pickid"] = pid
        car = Pickuplist.objects.get(pickid=pid)
        band = car.cid.id.band
        faults = FaultList.objects.filter(
            Q(Fa_id="all") | Q(Fa_id=CarInfo.objects.filter(band=band).get(ctype='all').id))
        return render(request, 'Sale/fault.html', {"faults": faults})

@login_required
def repairList(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    faultlist = {}
    repeat = {}
    if request.method == "POST":  # 这里POST一定要大写
        # 通常获取请求信息
        for i in request.POST:
            if re.match("checkboxPrimary_", i):
                fid = i[16:]
                request.session["repeat_" + fid] = int(request.POST.get("repeat_" + fid, 0))
                # faults.append(fid)
                # faultnames=FaultList.objects.get(pk=fid).faultname
                fault = FaultList.objects.get(pk=fid)
                repairlist = FaultInfo.objects.filter(faultid=fid)
                compo = set()

                for f in repairlist:
                    compo.add(f.coid.cotype)
                ctype = list(range(len(compo)))
                faultlist[fid] = (fault, repairlist, ctype)
            if re.match("repeat_", i):
                fid = i[7:]
                repeat[fid] = int(request.POST.get(i, 0))
        # print(repeat)
        # print(faultlist)
        if len(faultlist) == 0:
            return render(request, 'Sale/success.html', {"success_inform": "未选择故障！", "result": "fail"})
        return render(request, 'Sale/repairList.html',
                      {"faultlist": faultlist, "repeat": repeat})

@login_required
def newOrder(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    if request.method == "POST":  # 这里POST一定要大写
        # 通常获取请求信息
        pid=request.session.get("pickid")
        # pickup = Pickuplist.objects.all().values_list('pickid', flat=True)
        # if pid == None or pid not in pickup:
        #     return render(request, 'Sale/success.html', {"success_inform": "无该客户，请检查"})
        car = Pickuplist.objects.get(pickid=pid)
        cus = car.cusno
        fs = []
        for k, v in request.POST.items():
            if re.match("r_", k):
                fs.append(v)
        if len(fs)==0:
            return render(request, 'Sale/success.html', {"success_inform": "未选择维修！", "result": "fail"})
        repairlist = FaultInfo.objects.filter(faultinfoid__in=fs)
        faultlist = {}
        repeat = {}
        request.session["repair"] = fs
        subtotal_0, subtotal_1 = 0, 0
        for f in repairlist:
            repeat_f = request.session.get("repeat_" + f.faultid.faultid, 0)
            if f.faultid.faultid not in faultlist:
                faultlist[f.faultid.faultid] = (f.faultid, repeat_f)
                subtotal_0 += float(f.faultid.eload) * repeat_f
            repeat[f.faultinfoid] = repeat_f * f.renum
            subtotal_1 += float(f.renum * f.coid.coprice) * repeat_f
        tax = 0.093 * float(subtotal_0 * 125 + subtotal_1)
        sumall = tax + float(subtotal_0 * 125 + subtotal_1)
        # print(tax, sumall)
        request.session["sumprice"] = sumall
        return render(request, 'Sale/newOrder.html',
                      {"cus": cus, "car": car, "repairlist": repairlist, "faultlist": faultlist,
                       "subtotal": (subtotal_0, subtotal_1), "repeat": repeat,
                       "tax": tax, "sumall": sumall})

@login_required
def addOrder(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    # 添加顾客订单
    date = datetime.datetime.today()
    today = str(date.date())[2:].replace('-', '')
    oid_date = "O" + today
    oid_last = Orders.objects.last()

    if re.match(oid_date, str(oid_last.oid)):
        number = int(oid_last.oid[1:]) + 1
        oids = "O" + str(number)
    else:
        oids = oid_date + "001"

    pickid = request.session.get('pickid', None)
    repair = request.session.get('repair', None)
    sumprice = request.session.get('sumprice', None)
    sale_wid= request.user.username  #负责服务员工

    wid = ServiceWorker.objects.get(wid=sale_wid)

    Orders.objects.create(oid=oids,ostate='未完成',sumprice=sumprice,ostime=date,wid=wid)

    # 添加派工单
    repairlist = FaultInfo.objects.filter(faultinfoid__in=repair)

    wsid_init = int(oids[1:] + "00")
    ws_num = 1

    oid = Orders.objects.get(oid=oids)
    print(repairlist)
    for f in repairlist:
        coid = f.coid.coid
        book(coid)
        wsid = "O" + str(wsid_init + ws_num)
        ws_num += 1
        status = "未完成"
        if f.coid.conumber < f.renum:
            status = "缺货"
        repeatnum = request.session.get("repeat_" + f.faultid.faultid, 0)
        # 找到合适的维修员工，修改其负荷工时

        repair_worker = MaintenanceWorker.objects.all().order_by('workload')
        reworker = repair_worker[0]

        reworker.workload += f.faultid.eload * repeatnum
        reworker.save()

        Worksheet.objects.create(wsid=wsid, wsstate=status, repeatnum=repeatnum,oid=oid,
                                 pickid= Pickuplist.objects.get(pickid=pickid),wid=reworker)

        # 修改零件库存数量,同时减少零件批次表中的剩余数量
        compo = f.coid
        compo.conumber -= f.renum * repeatnum
        compo_batch = Batch.objects.filter(coid=compo.coid).order_by('id')
        for cb in compo_batch:
            if cb.remainnum >= f.renum * repeatnum:
                cb.remainnum -= f.renum * repeatnum
                cb.save()
                break


        # 记录 派工单所用零件信息表
        WorksheetCompoInfo.objects.create(wsid=Worksheet.objects.get(wsid=wsid),faultinfoid=f)

        # 生成零件使用单
        # 若不缺货，生成零件使用单
        if status !='缺货':
            CompoUseInfo.objects.create(wsid=Worksheet.objects.get(wsid=wsid), compo_use_state='未领取')
    return render(request, 'Sale/success.html', {"success_inform": "订单提交成功！", "result": 'success'})


def co_eoq(id):
    com = Components.objects.get(coid=id)
    com_price = float(com.coprice)
    use = 0
    cur_date = datetime.datetime.now()
    month = cur_date - datetime.timedelta(weeks=4)
    worksheet_out = Worksheet.objects.filter(oid__ostime__gt=month, oid__ostime__lt=cur_date)
    fault_info_co = FaultInfo.objects.filter(coid=com)
    for i in worksheet_out:
        worksheet_info = WorksheetCompoInfo.objects.filter(wsid=i)
        repeatnum = i.repeatnum
        for j in worksheet_info:
            if j.faultinfoid in fault_info_co:
                com_use = int(j.faultinfoid.renum) * int(repeatnum)
                use += com_use
    best_q = int(math.sqrt(2*use*100*100/com_price))
    print('best_q=', best_q)
    return  best_q


def co_r(id):
    com = Components.objects.get(coid=id)
    com_price = float(com.coprice)
    use = 0
    cur_date = datetime.datetime.now()
    month = cur_date - datetime.timedelta(weeks=4)
    worksheet_out = Worksheet.objects.filter(oid__ostime__gt=month, oid__ostime__lt=cur_date)
    fault_info_co = FaultInfo.objects.filter(coid=com)
    for i in worksheet_out:
        worksheet_info = WorksheetCompoInfo.objects.filter(wsid=i)
        repeatnum = i.repeatnum
        for j in worksheet_info:
            if j.faultinfoid in fault_info_co:
                com_use = int(j.faultinfoid.renum) * int(repeatnum)
                use += com_use
    best_r = 0.25*use + 1.65*0.2*use*math.sqrt(0.25)
    print('best_r=', best_r)
    return best_r


def book(id):
    best_q = co_eoq(id)
    best_r = co_r(id)
    com = Components.objects.get(coid=id)
    copurchase = CoPurchase.objects.filter(coid=com).filter(purchasestate='已采购未入库')
    purchase_num = 0
    for i in copurchase:
        purchasenum = i.purchasenum
        purchase_num += purchasenum
    conumber = com.conumber
    tot = purchase_num + conumber
    if tot > best_r :
        print('tot=',tot)
        return
    else:
        purchase_now = CoPurchase.objects.filter(coid=com).filter(purchasestate='未采购').count()
        print('purchase_now=', purchase_now)
        if purchase_now == 0:
            date = datetime.datetime.today()
            today = str(date.date())[2:7].replace('-', '')
            pur_id = 'CG02' + today
            sum = Purchase.objects.filter(purchaseid__contains=pur_id).count()
            pur_id = pur_id + '000'
            p_id = 'CG0' + str(int(pur_id[3:]) + sum + 1)
            purchasenum = best_q
            coid = id
            comp = Components.objects.get(coid=coid)
            coprice = comp.coprice
            sum_money = float(coprice) * float(purchasenum)
            purchase = Purchase(purchaseid=p_id, purchasenum=purchasenum, purchasestate='未采购', psumprice=sum_money,
                                ptime=date)
            purchase.save()
            purchase_m = Purchase.objects.get(purchaseid=p_id)
            print(purchase_m)
            copurchase = CoPurchase(purchaseid=purchase_m, purchasenum=purchasenum, purchasestate='未采购',
                                    psumprice=sum_money, ptime=date, coid=comp)
            copurchase.save()
            return
        else:
            copurchase = CoPurchase.objects.filter(coid=com).filter(purchasestate='未采购').first()
            copurchase.purchasenum = best_q
            copurchase.save()
            purchase = copurchase.purchaseid
            purchase.purchasenum = best_q
            purchase.save()
            print(copurchase, purchase)
            return


@login_required
def order(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    sale_wid = request.user.username  # 负责服务员工
    # 服务顾问只能看到自己负责的订单

    orders = Orders.objects.filter(wid=sale_wid)
    # print(orders)
    cnames = {}
    licenses = {}

    for o in orders:
        # print(o.oid)
        # print(Worksheet.objects.filter(oid=o.oid))
        worksheets = Worksheet.objects.filter(oid=o.oid)[0]
        pickid = Pickuplist.objects.get(pickid=worksheets.pickid.pickid)
        cnames[o.oid] = pickid.cusno.cname
        licenses[o.oid] = pickid.license

    if request.method == 'POST':
        message=request.POST.get('message','')
        oid_curr=request.POST.get('oid','')
        print(request.POST)
        if message !='':
            order = Orders.objects.get(oid=oid_curr)
            order.return_info = message
            order.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"信息为空"}', content_type='application/json')
    return render(request, 'Sale/orders.html',
                  {"wid":"W1901001","orders": orders, "cnames": cnames, "licenses": licenses})

@login_required
def orderDetails(request, oid):
    # if request.user.type != 'sale':
    #     return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    worksheets = Worksheet.objects.filter(oid=oid)
    car=worksheets[0].pickid
    cus=car.cusno
    faultlist={}
    repairlist=[]
    repeat={}
    subtotal_0, subtotal_1 = 0, 0
    for ws in worksheets:
        wcs = WorksheetCompoInfo.objects.filter(wsid=ws.wsid)
        repair=[]
        for wc in wcs:
            repair.append(wc.faultinfoid)
        repairlist.extend(repair)
        repeat_f =ws.repeatnum
        for f in repair:
            if f.faultid.faultid not in faultlist:
                faultlist[f.faultid.faultid] = (f.faultid, repeat_f)
                subtotal_0 += float(f.faultid.eload) * repeat_f
            subtotal_1 += float(f.renum * f.coid.coprice) * repeat_f
            repeat[f.faultinfoid] = repeat_f * f.renum

    tax = 0.093 * float(subtotal_0 * 125 + subtotal_1)
    sumall = tax + float(subtotal_0 * 125 + subtotal_1)
    return render(request, 'Sale/orderDetails.html',
                  {"oid": oid, "cus": cus, "car": car, "repairlist": repairlist, "faultlist": faultlist,
                   "subtotal": (subtotal_0, subtotal_1),"repeat":repeat,
                   "tax": tax, "sumall": sumall})


@login_required
def checkPick(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    if request.method == 'POST':
        pickid = request.POST.get('pickid','')
        pickup = Pickuplist.objects.all().values_list('pickid', flat=True)

        if pickid in pickup:
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"提车单号错误，请核对后填写"}', content_type='application/json')


@login_required
def checkCusno(request):
    if request.user.type != 'sale':
        return render(request,'Sale/confirm.html',{'message':'账号无权限'})
    if request.method == 'POST':
        cusno = int(request.POST.get('cusno', ''))
        cusnolist = Customer.objects.all().values_list('cusno', flat=True)

        if cusno in cusnolist:
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"顾客编号错误，请核对后填写"}', content_type='application/json')
