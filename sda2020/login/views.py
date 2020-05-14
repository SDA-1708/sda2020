from django.shortcuts import render
from .models import Worker,Orders,Worksheet,Pickuplist,Customer,WorksheetCompoInfo
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def index(request):
    if request.user.type != 'customer':
        return render(request,'login/confirm.html',{'message':'账号无权限'})
    cus = Customer.objects.get(cusno = int(request.user.customer.cusno))
    print(cus)
    return render(request,'login/index.html',{"cus": cus})

@login_required
def order(request):
    if request.user.type != 'customer':
        return render(request, 'login/confirm.html', {'message': '账号无权限'})
    cusno = int(request.user.customer.cusno)
    cus =Customer.objects.get(cusno=cusno)
    cars = Pickuplist.objects.filter(cusno=cus.cusno)
    orders=set()
    license={}
    for c in cars:
        worksheets_c = Worksheet.objects.filter(pickid=c.pickid)
        for ws in worksheets_c:
            orders.add(ws.oid)
            license[ws.oid.oid] = c.license

    return render(request, 'login/orders.html',
                  {"orders": orders, "cus": cus, "cars": cars,"license":license})
@login_required
def orderDetails(request, oid):
    if request.user.type != 'customer':
        return render(request, 'login/confirm.html', {'message': '账号无权限'})
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
    return render(request, 'login/orderDetails.html',
                  {"oid": oid, "cus": cus, "car": car, "repairlist": repairlist, "faultlist": faultlist,
                   "subtotal": (subtotal_0, subtotal_1),"repeat":repeat,
                   "tax": tax, "sumall": sumall})
@login_required
def carInfo(request):
    if request.user.type != 'customer':
        return render(request, 'login/confirm.html', {'message': '账号无权限'})
    cusno = int(request.user.customer.cusno)
    cus = Customer.objects.get(cusno=cusno)
    cars = Pickuplist.objects.filter(cusno=cus.cusno)
    repairs = {}
    for c in cars:
        worksheets_c = Worksheet.objects.filter(pickid=c.pickid)
        repairs[c.pickid] = 0
        repairs[c.pickid] = 0
        for ws in worksheets_c:
            repairs[c.pickid] += 1
    return render(request, 'login/carInfo.html', {"cars": cars, "repairs": repairs})