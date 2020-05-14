from django.shortcuts import render
from .models import Pickuplist
from .models import Orders
from .models import Worksheet
from .models import Purchase,Worker
import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
@login_required
def index(request):
    if request.user.type != 'finance':
        return render(request,'Finance/confirm.html',{'message':'账号无权限'})
    workername = Worker.objects.get(wid=request.user.username)
    orders = Orders.objects.all().order_by('-oid') #按时间降序排列
    purchases=Purchase.objects.all().order_by('ptime')
    cnames = {}
    licenses = {}
    for o in orders:
        worksheets = Worksheet.objects.filter(oid=o.oid)[0]
        pickid = Pickuplist.objects.get(pickid=worksheets.pickid.pickid)
        cnames[o.oid] = pickid.cusno.cname
        licenses[o.oid] = pickid.license
    #绘图数据
    td=datetime.date.today()
    one_day = datetime.timedelta(days=1)
    start=td-one_day*29
    sin=[] #收入
    cos=[] #支出
    date=[]
    os= Orders.objects.filter(ostime__gte=start, ostime__lte=td)
    ps= Purchase.objects.filter(ptime__gte=start, ptime__lte=td)
    for d in range(30):
        day_curr = start + d * one_day
        date.append(str(day_curr)[5:])
        day_sum1=0
        day_sum2=0
        for o in os:
            if o.ostime.date() == day_curr:
                day_sum1 += int(o.sumprice)
        for p in ps:
            if p.ptime.date() == day_curr:
                day_sum2 += int(p.psumprice)/100
        sin.append(day_sum1)
        cos.append(day_sum2)
    sin_=','.join([str(i) for i in sin])
    cos_=','.join([str(i) for i in cos])
    date_=','.join([str(i) for i in date])
    return render(request, 'Finance/index.html',
                  { "orders": orders, "purchase":purchases,"cnames": cnames, "licenses": licenses,
                    "sin":sin_,"cos":cos_,'date':date_,'workername':workername.wname})