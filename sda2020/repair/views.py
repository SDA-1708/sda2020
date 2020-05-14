import datetime
import math

from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
# Create your views here.

from repair.models import Worksheet, Worker, Orders, WorksheetCompoInfo, CompoUseInfo, FaultInfo, WorksheetCompoInfo, \
    FaultList, MaintenanceWorker, Pickuplist, Customer, Car, CarInfo, Components, CoPurchase, Purchase, Components, \
    WorksheetCompoInfo, FaultInfo, Worksheet, Batch
from welcome.models import Userinfo
# from storage.models import Batch
# from Sale.models import CoPurchase, Purchase, Components, WorksheetCompoInfo, FaultInfo, Worksheet
from django.contrib.auth.decorators import login_required


from django.conf import settings
def send_email(workid,email,faultid,oid,faultnum):
    from django.core.mail import EmailMultiAlternatives
    subject = '新故障提醒————徳旭4S'
    text_content = '''感谢光临徳旭4S，我们将竭诚为您服务！\
    如果您看到这条消息，代表您的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
    <p>亲爱的服务顾问{}</p >
    <p>您负责的的订单{}有新故障，故障编号为{},故障数量为{},请及时与顾客联系</p >
    '''.format(workid,oid,faultid,faultnum)
    msg = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()


@login_required
def un_wroksheet(request):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    wor = Worksheet.objects.filter(wid=w_id).filter(wsstate='未完成')
    worker = []
    for i in wor:
        m = {}
        m['wsid'] = i.wsid
        m['state'] = i.wsstate
        m['comuse'] = CompoUseInfo.objects.filter(wsid=i.wsid).first().compo_use_state
        faid = FaultInfo.objects.filter(worksheetcompoinfo__wsid=i.wsid).first()
        fid = faid.faultid.faultid
        m['faultname'] = FaultList.objects.filter(faultid=fid).first().faultname
        worker.append(m)
    context = {
        'w_name': w_name,
        'w_worker': worker
    }
    return render(request, 'repair_un_finish.html', context)
    # 未完成的派工单查看页面

@login_required
def ed_wroksheet(request):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    wor = Worksheet.objects.filter(wid=w_id).filter(wsstate='已完成')
    worker = []
    for i in wor:
        m = {}
        m['wsid'] = i.wsid
        m['state'] = i.wsstate
        m['comuse'] = CompoUseInfo.objects.filter(wsid=i.wsid).first().compo_use_state
        faid = FaultInfo.objects.filter(worksheetcompoinfo__wsid=i.wsid).first()
        fid = faid.faultid.faultid
        m['faultname'] = FaultList.objects.filter(faultid=fid).first().faultname
        worker.append(m)
    context = {
        'w_name': w_name,
        'w_worker': worker
    }
    return render(request, 'repair_ed_finish.html', context)

@login_required
def out_wroksheet(request):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    wor = Worksheet.objects.filter(wid=w_id).filter(wsstate='缺货')
    worker = []
    for i in wor:
        m = {}
        m['wsid'] = i.wsid
        m['state'] = i.wsstate
        faid = FaultInfo.objects.filter(worksheetcompoinfo__wsid=i.wsid).first()
        fid = faid.faultid.faultid
        m['faultname'] = FaultList.objects.filter(faultid=fid).first().faultname
        worker.append(m)
    context = {
        'w_name': w_name,
        'w_worker': worker
    }
    return render(request, 'repair_out_finish.html', context)

@login_required
def welcome(request):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = 'W2002011'
    request.session["w_id"] = w_id
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    wor = Worksheet.objects.filter(compouseinfo__compo_use_state='未领取').filter(wid=w_id).filter(wsstate='未完成')
    worker = []
    for i in wor:
        m = {}
        m['wsid'] = i.wsid; m['state'] = i.wsstate
        m['comuse'] = CompoUseInfo.objects.filter(wsid=i.wsid).first().compo_use_state
        faid = FaultInfo.objects.filter(worksheetcompoinfo__wsid=i.wsid).first()
        fid = faid.faultid.faultid
        m['faultname'] = FaultList.objects.filter(faultid=fid).first().faultname
        pick_id = Worksheet.objects.filter(wsid=i.wsid).first().pickid.pickid
        car_id = Pickuplist.objects.filter(pickid=pick_id).first().cid.cid
        m['cid'] = car_id
        worker.append(m)
    context={
        'w_name' : w_name,
        'w_worker' : worker
    }
    return render(request,'repair_welcome.html',context)

@login_required
def userinfo(request):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    w_info = MaintenanceWorker.objects.filter(wid=w_id).first()
    w_dept = w_info.dept
    w_post = w_info.postion
    w_time = w_info.workload
    context = {
        'w_name': w_name,
        'w_id' : w_id,
        'w_dept' : w_dept,
        'w_post': w_post,
        'w_time' : w_time,
    }
    return render(request,'repair_userinfo.html',context)

@login_required
def worksheetinfo(request, ws_id):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    m={}
    m['wsid'] = ws_id
    pickinfo = Worksheet.objects.filter(wsid=ws_id).first().pickid.pickid
    pick = Pickuplist.objects.filter(pickid=pickinfo).first()
    pickid = pick.pickid
    cusid = pick.cusno.cusno
    m['cusid'] = cusid
    c_id = pick.cid.cid
    m['cid'] = c_id
    id = Car.objects.filter(cid=c_id).first().id.id
    carinfo = CarInfo.objects.filter(id=id).first()
    c_band = carinfo.band
    ctype = carinfo.ctype
    faid = FaultInfo.objects.filter(worksheetcompoinfo__wsid=ws_id).first()
    fid = faid.faultid.faultid
    m['faultname'] = FaultList.objects.filter(faultid=fid).first().faultname
    m['cband'] = c_band
    m['ctype'] = ctype
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
    context = {
        'w_name': w_name,
        'works': m,
    }
    return render(request,'repair_back.html',context)

@login_required
def new_fault(request, ws_id):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    worksheet = Worksheet.objects.get(wsid=ws_id)
    oid = worksheet.oid.oid
    pickid = worksheet.pickid.pickid
    wid = worksheet.wid.wid.wid
    request.session['oid'] = oid
    orders = Orders.objects.get(oid=oid)
    service = orders.wid
    print(service.wid.wid,type(service.wid.wid))
    request.session['service_id'] = str(service.wid.wid)
    request.session['email'] = Userinfo.objects.get(username=str(service.wid.wid)).email
    caid = Pickuplist.objects.get(pickid=pickid).cid.cid
    i_d = Car.objects.get(cid=caid).id.id
    band = CarInfo.objects.filter(id=i_d).first().band
    ctype = CarInfo.objects.filter(id=i_d).first().ctype
    idinfo = CarInfo.objects.filter(band=band).filter(Q(ctype=ctype) | Q(ctype='all'))
    ids = []
    faltlists = []
    for i in idinfo:
        ids.append(i.id)
    for j in range(0,len(ids)):
        falt = FaultList.objects.filter(Fa_id=ids[j])
        if len(falt) != 0:
            faltlists.append(falt)
    faltlist = FaultList.objects.filter(Fa_id='all')
    faltlists.append(faltlist)
    work = {}
    work['wsid'] = ws_id
    work['oid'] = oid
    work['pickid'] = pickid
    work['wid'] = wid
    work['faultlist'] = faltlists
    context = {
        'w_name': w_name,
        'work' : work,
    }
    return render(request,'repair_add.html',context)

@login_required
def worksheetadd(request, ws_id):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    num = request.POST.get('num')
    faultid = request.POST.get('fault')
    service = request.session.get('service_id')
    email = request.session.get('email')
    oid = request.session.get('oid')
    send_email(service, email, faultid, oid, num)
    url = reverse('repair:un_worksheet')
    return redirect(url)
    # faultname = FaultList.objects.get(faultid=faultid).faultname
    # faults = FaultInfo.objects.filter(faultid=faultid)
    # work = {}
    # work['faultname'] = faultname
    # work['faultid'] = faultid
    # work['num'] = num
    # work['wsid'] = ws_id
    # fault = []
    # for i in faults:
    #     m={}
    #     co_id = i.coid.coid
    #     co_name = Components.objects.get(coid=co_id).coname
    #     m['faultinfoid'] = i.faultinfoid
    #     m['coname'] = co_name
    #     m['conum'] = i.renum
    #     m['coid'] = co_id
    #     fault.append(m)
    # context = {
    #     'w_name': w_name,
    #     'work': work,
    #     'fault' : fault
    # }
    # return render(request, 'repair_add_co.html', context)

@login_required
def new_fault_confirm(request, ws_id, num):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    workerinfos = Worker.objects.filter(wid=w_id)
    workerinfo = workerinfos.first()
    w_name = workerinfo.wname
    fault_info_id = request.POST.getlist('com')
    if len(fault_info_id) == 0:
        url = reverse('repair:un_worksheet')
        return redirect(url)
    worksheet = Worksheet.objects.get(wsid=ws_id)
    oid = worksheet.oid
    pickid = worksheet.pickid
    wid = MaintenanceWorker.objects.get(wid=w_id)
    repeatnum = num
    lastwsid = Worksheet.objects.filter(oid=oid.oid).order_by('wsid').last().wsid
    last = str(int(lastwsid[1:])+1)
    new_wsid = 'O'+last
    if check_new_worksheet(fault_info_id, repeatnum):
        wsstate = '未完成'
    else:
        wsstate = '缺货'
    new_worksheet_create(wsid=new_wsid, oid=oid, pickid=pickid, wid=wid, wsstate=wsstate, repeatnum=repeatnum, fault_info_id=fault_info_id )
    url = reverse('repair:un_worksheet')
    return redirect(url)

# check_new_worksheet传入两个参数,fault_info_id故障信息id列表, num重复次数，能做返回True，不能返回None
def check_new_worksheet(fault_info_id, num):
    state = True
    for i in fault_info_id:
        faultinfo = FaultInfo.objects.get(faultinfoid=i)
        co_id = faultinfo.coid.coid
        renum = faultinfo.renum
        total = int(renum) * int(num)
        left = Components.objects.get(coid=co_id).conumber
        if total > left:
            return False
    return True

def new_worksheet_create(wsid, oid, pickid, wid, wsstate, repeatnum, fault_info_id):
    worksheet = Worksheet(wsid=wsid, oid=oid, pickid=pickid, wid=wid, wsstate=wsstate, repeatnum=repeatnum)
    worksheet.save()
    for i in fault_info_id:
        work_sheet = Worksheet.objects.get(wsid=wsid)
        fault_info = FaultInfo.objects.get(faultinfoid=i)
        worksheetcompoinfo = WorksheetCompoInfo(wsid=work_sheet, faultinfoid=fault_info)
        worksheetcompoinfo.save()
        co_id = fault_info.coid.coid
        book(co_id)
    if wsstate =='未完成':
        work_sheet = Worksheet.objects.get(wsid=wsid)
        compoUseInfo = CompoUseInfo(wsid=work_sheet, compo_use_state='未领取')
        compoUseInfo.save()
        for i in fault_info_id:
            faultinfo = FaultInfo.objects.get(faultinfoid=i)
            co_id = faultinfo.coid.coid
            renum = faultinfo.renum
            total = int(renum) * int(repeatnum)
            left = Components.objects.get(coid=co_id).conumber
            left_co = left - total
            Components.objects.filter(coid=co_id).update(conumber=left_co)
            batches = Batch.objects.filter(coid=co_id).order_by('id').exclude(remainnum=0)
            for j in batches:
                if total <= 0:
                    break
                else:
                    if j.remainnum < total:
                        total -= total - j.remainnum
                        id = j.id
                        Batch.objects.filter(id=id).update(remainnum=0)
                    else:
                        batch_left = j.remainnum - total
                        total = 0
                        id = j.id
                        Batch.objects.filter(id=id).update(remainnum=batch_left)
    total_price = total_money(fault_info_id, repeatnum)
    Orders.objects.filter(oid=oid).update(sumprice=total_price)
    print(wsid)
    return True

def total_money(fault_info_id, repeatnum):
    faultid = FaultInfo.objects.filter(faultinfoid=fault_info_id[0]).first().faultid.faultid
    fault_load = FaultList.objects.get(faultid=faultid).eload
    co_money = 0
    for i in fault_info_id:
        faultinfo = FaultInfo.objects.get(faultinfoid=i)
        co_id = faultinfo.coid.coid
        renum = faultinfo.renum
        total_num = int(renum) * int(repeatnum)
        price = Components.objects.get(coid=co_id).coprice
        co_money += total_num*price
    total_price = co_money + fault_load*5
    return  total_price

# 改成return True的函数
def orderconfirm(or_id):
    undo = Worksheet.objects.filter(oid=or_id).filter(wsstate='未完成').count()        # 查看未完成的派工单数量
    if undo == 0:
        order = Orders.objects.filter(oid=or_id).update(ostate='已完成')               # 不存在未完成派工单立刻更新订单
    return True

@login_required
def worksheetconfirm(request, ws_id):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    pick_state = CompoUseInfo.objects.filter(wsid=ws_id).first().compo_use_state
    if (pick_state == '已领取'):
        worksheet = Worksheet.objects.filter(wsid=ws_id).update(wsstate='已完成')  # 根据派工单号更改派工单状态
        faid = FaultInfo.objects.filter(worksheetcompoinfo__wsid=ws_id).first()
        fid = faid.faultid.faultid
        ftime = FaultList.objects.filter(faultid=fid).first().eload
        load = MaintenanceWorker.objects.filter(wid=w_id).first().workload + ftime
        MaintenanceWorker.objects.filter(wid=w_id).update(workload=load)
        or_id = Worksheet.objects.filter(wsid=ws_id).first().oid  # 查找订单编号
        orderconfirm(or_id)  # 查看调用订单确认函数，看是否能够确认订单
        url = reverse('repair:ed_worksheet')
        return redirect(url)
    else:
        url = reverse('repair:un_worksheet')
        return redirect(url)
# 派工单从未完成变成已完成

@login_required
def back(request, ws_id):
    if request.user.type != 'repair':
        return render(request,'confirm.html',{'message':'账号无权限'})
    w_id = request.session.get('w_id')
    wor = Worksheet.objects.filter(wsid=ws_id).first()
    wstate =  wor.wsstate
    if wstate == '未完成':
        url = reverse('repair:un_worksheet')
        return redirect(url)
    elif wstate == '缺货':
        url = reverse('repair:out_worksheet')
        return redirect(url)
    else:
        url = reverse('repair:ed_worksheet')
        return redirect(url)


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
        purchase_now = CoPurchase.objects.filter(coid=com).filter(purchasestate='未确认').count()
        print(purchase_now)
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
            CoPurchase.objects.filter(coid=com).filter(purchasestate='未确认').first().update(purchasenum=best_q)
            return

