from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
import hashlib
from . import models
import json
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import auth,messages
from .forms import Search,LoginForm,RegisterForm,ResetForm,TouchForm
import datetime
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

# Create your views here.
# 起始页面
def index(request):
    return render(request, 'welcome/index.html')

def about(request):
    return render(request, 'welcome/about.html')

def blog(request):
    carlist = models.CarInfo.objects.all().exclude(ctype='all')
        # paginator = Paginator(carlist, 10)
        # try:
        #     current_page_num = int(request.GET.get('page',1))
        #     current_page = paginator.page(current_page_num)
        # except EmptyPage as e:
        #     current_page = paginator.page(paginator.num_pages)
        # except PageNotAnInteger:
        #     current_page = paginator.page(1)
        # if paginator.num_pages>11:
        #     if current_page_num <6:
        #         page_range = range(1,11)
        #     elif current_page_num+5>paginator.num_pages:
        #         page_range = range(paginator.num_pages-10,paginator.num_pages+1)
        #     else:
        #         page_range = range(current_page_num-5,current_page_num+6)
        # else:
        #     page_range=paginator.page_range
        # return render(request, 'welcome/blog.html',{'current_page':current_page,'page_range':page_range,'current_page_num':current_page_num})
    return render(request, 'welcome/blog.html',{'carlist':carlist,})

def contact(request):
    message=''
    now = datetime.datetime.now()
    end_date = now+ datetime.timedelta(days=7)
    workarrangelist = models.WorkerArrange.objects.filter(timeatwork__gte=now,timeatwork__lte=end_date,appostate='空闲')
    return render(request, 'welcome/contact.html',locals())

def gallery(request):
    return render(request, 'welcome/gallery.html')

def services(request):
    return render(request, 'welcome/services.html')

def details(request, car_id):
    carinfo = models.CarInfo.objects.get(id=car_id)
    return render(request, 'welcome/details.html',{'carinfo':carinfo})
#
# def searchresult(request):
#     if request.method == 'GET' and 'Skey' in request.GET:
#         keyword = request.GET['Skey'].strip()
#         result0 = models.CarInfo.objects.filter(band__icontains=keyword)
#         result1 = models.CarInfo.objects.filter(ctype__icontains=keyword)
#         carlist = set(result1+result0)
#         return render(request, 'welcome/blog.html',{'carlist':carlist})

#搜索框
def search(request):
    if request.method == 'GET' and 's' in request.GET:
        keyword = request.GET['s'].strip()
        if keyword:
            result0 = models.CarInfo.objects.filter(band__icontains=keyword).exclude(ctype='all')
            result1 = models.CarInfo.objects.filter(ctype__icontains=keyword).exclude(ctype='all')
            json_list = []
            for re1 in result0:
                json_list.append(re1.band)
            for re1 in result1:
                json_list.append(re1.ctype)
            json_list = list(set(json_list))
            return HttpResponse(json.dumps(json_list,ensure_ascii=False))

# 登录
def login(request):
    if request.session.get('is_login',None):
        user = request.user
        if user.type == 'customer':
            return redirect(reverse('welcome:index'))
        elif user.type == 'finance':
            return redirect(reverse('Finance:index'))
        elif user.type == 'HR':
            return redirect(reverse('HumanResources:index'))
        elif user.type == 'purchase':
            return redirect(reverse('purchase:index'))
        elif user.type == 'repair':
            return redirect(reverse('repair:welcome'))
        elif user.type == 'sale':
            return redirect(reverse('Sale:index'))
        elif user.type == 'storage':
            return redirect(reverse('storage:welcome'))
        else:
            message = '账号类型错误'
            return render(request,'welcome/confirm.html',{'message':message})
    if request.method == 'GET':
        obj = LoginForm()
        return render(request, 'welcome/login.html',{'login_obj':obj})
    elif request.method == 'POST':
        data = request.POST
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        obj = LoginForm(data)
        message='请检查验证码或用户名长度'
        if obj.is_valid():
            username = obj.cleaned_data.get('username')
            password = obj.cleaned_data.get('password')
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                if not user_obj.has_confirmed:
                    message = '该用户未经过邮件确认！'
                    return render(request, 'welcome/login.html', {'login_obj': obj, 'message': message})
                else:
                    auth.login(request, user_obj)
                    request.session['is_login'] = True
                    user = request.user
                    if user.type == 'customer':
                        return redirect(reverse('welcome:index'))
                    elif user.type == 'finance':
                        return redirect(reverse('Finance:index'))
                    elif user.type == 'HR':
                        return redirect(reverse('HumanResources:index'))
                    elif user.type == 'purchase':
                        return redirect(reverse('purchase:welcome'))
                    elif user.type == 'repair':
                        return redirect(reverse('repair:welcome'))
                    elif user.type == 'sale':
                        return redirect(reverse('Sale:index'))
                    elif user.type == 'storage':
                        return redirect(reverse('storage:welcome'))
                    else:
                        message = '账号类型错误'
                        return render(request, 'welcome/confirm.html', {'message': message})
                    # return redirect(reverse('welcome:index'))
            else:
                message = '用户名或密码不正确'
                # obj.add_error('errorpw','用户名或者密码不正确')
                return render(request,'welcome/login.html',{'login_obj':obj,'message':message})
        else:
            return render(request,'welcome/login.html',{'login_obj':obj,'message':message})

# 注册
def register(request):
    if request.method == 'GET':
        register_obj = RegisterForm()
        return render(request, 'welcome/register.html', {'register_obj': register_obj})
    elif request.method == 'POST':
        data = request.POST
        register_obj = RegisterForm(data)
        if register_obj.is_valid():
            user_obj = register_obj.cleaned_data
            username = user_obj.get('username')
            password = user_obj.get('password')
            r_password = user_obj.get('r_password')
            name = user_obj.get('name')
            email = user_obj.get('email')
            gender = user_obj.get('gender')
            phone = user_obj.get('phone')
            address = user_obj.get('address')
            if password!=r_password:
                message = '两次输入的密码不同！'
                return render(request,'welcome/register.html',{'register_obj':register_obj,'message':message,'status':'0'})
            else:
                if models.Userinfo.objects.filter(username=username).exists():
                    message = '用户名已存在！'
                    return render(request, 'welcome/register.html', {'register_obj': register_obj, 'message': message,'status':'0'})
                if models.Userinfo.objects.filter(email = email).exists():
                    message = '邮箱已被注册！'
                    return render(request, 'welcome/register.html', {'register_obj': register_obj, 'message': message,'status':'0'})
                new_obj = models.Userinfo.objects.create_user(username=username, password=password, email=email, type='customer')
                new_obj.save()
                new_customere = models.Customer.objects.create(cname = name, cgender=gender,tel=phone,email = email,caddress=address)
                new_customere.account = new_obj
                new_customere.save()
                code = make_confirm_string(new_obj)
                send_email(email,code)
                message = '注册成功，请前往邮箱确认！'
                status = '1'
                return render(request, 'welcome/register.html', {'register_obj': register_obj, 'message': message,'status':status})
                # print('新用户{username}注册成功！'.format(username=username))
        else:
            message = '请检查输入数据'
            return render(request, 'welcome/register.html', {'register_obj': register_obj,'message':message,'status':'0'})

# 注册附属函数
def hash_code(s,salt='welcome'):
    h = hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username,now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code

from django.conf import settings
def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自徳旭4S的注册确认邮件'
    text_content = '''感谢注册徳旭4S，我们将竭诚为您服务！\
    如果您看到这条消息，代表您的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>徳旭4S</a>,\
    我们以品质优先，专注于为您提供良好的服务</p>
    <p>请点击站点链接完成注册</p>
    <p>此链接有效期为{}天！</p>'''.format('127.0.0.1:8000/welcome',code,settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()
import pytz
def user_confirm(request):
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效的确认请求！"
        return render(request,'welcome/confirm.html',{'message':message})
    c_time = confirm.c_time
    now = datetime.datetime.now()
    # if now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))>c_time+datetime.timedelta(settings.CONFIRM_DAYS):

    if now>c_time+datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request,'welcome/confirm.html',{'message':message})
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message ='感谢确认,请使用账户登陆！'
        return render(request,'welcome/confirm.html',{'message':message})
# # 登录
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'welcome/login.html')
#     elif request.method == 'POST':
#         # print(request.POST)
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user_obj = auth.authenticate(username=username, password=password)
#         print(user_obj)
#         if user_obj:
#             auth.login(request, user_obj)
#             return JsonResponse({'status': 1, 'url': reverse('index')})
#         else:
#             return JsonResponse({'status': 0, 'url': ''})
#
#
# # 访问认证
# def index(request):
#     if request.user.is_authenticated:
#         print(request.user)
#         if request.method == 'GET':
#             return render(request, 'welcome/index.html')
#     else:
#         return redirect('login')
#
#
# 注销
def logout(request):
    auth.logout(request)
    return redirect('welcome:index')
#
#
# 修改密码
def reset_psd_email(request):
    return render(request,'welcome/reset_psd1.html')

def reset_psd_send(request):
    if request.user.is_authenticated:
        user_obj = request.user
        email = user_obj.email
        code = make_confirm_psd(user_obj)
        send_email_reset(email, code)
        message = '请前往邮箱确认！'
        return JsonResponse({'message':message})
    return JsonResponse({'message':'请先登陆'})

def make_confirm_psd(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username,now)
    models.PsdConfirm.objects.create(code=code, user=user, )
    return code

from django.conf import settings
def send_email_reset(email,code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自徳旭4S的更改密码邮件'
    text_content = '''徳旭4S，用心为您服务！\
    如果您看到这条消息，代表您的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
    <p>感谢访问<a href="http://{}/reset_psd/?code={}" target=blank>徳旭4S</a>,\
    我们以品质优先，专注于为您提供良好的服务</p>
    <p>请点击站点链接完成更改密码</p>
    <p>此链接有效期为{}天！</p>'''.format('127.0.0.1:8000/welcome',code,settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()

from django.contrib.auth.decorators import login_required
@login_required
def reset_psd(request):
    code = request.GET.get('code', None)
    try:
        confirm = models.PsdConfirm.objects.get(code=code)
    except:
        message = '无效请求'
        return render(request, 'welcome/confirm.html', {'message': message})
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.delete()
        message = '您的邮件已经过期！请重新发送！'
        return render(request, 'welcome/confirm.html', {'message': message})
    else:
        reset_obj = ResetForm()
        return render(request, 'welcome/reset_psd.html', {'reset_obj': reset_obj})

def reset_psd_post(request):
    if request.method == 'GET':
        message='GET方法无效'
        return render(request, 'welcome/confirm.html', {'message': message})
    elif request.method == 'POST':
        reset_obj = ResetForm(request.POST)
        message = '请检查输入'
        if reset_obj.is_valid():
            data = reset_obj.cleaned_data
            old_password =data.get('old_password')
            new_password = data.get('new_password')
            r_new_password = data.get('r_new_password')
            # ret=request.user.check_password(old_password)
            # print(ret)
            if request.user.check_password(old_password):
                if new_password == r_new_password:
                    message = '修改成功'
                    request.user.set_password(new_password)
                    request.user.save()
                    return render(request,'welcome/confirm.html',{'message':message,'status':'1'})
                else:
                    message = '两次密码不一致'
                    return render(request,'welcome/reset_psd.html',{'reset_obj':reset_obj,'message':message,'status':'0'})
            else:
                message = '密码不正确'
                return render(request,'welcome/reset_psd.html',{'reset_obj':reset_obj,'message':message,'status':'0'})
        return render(request,'welcome/reset_psd.html',{'reset_obj':reset_obj,'message':message,'status':'0'})

def appo(request):
    if request.method=='POST':
        data = request.POST
        name = data['name']
        email = data['email']
        phone = data['phone']
        content = data['content']
        gender = data['gender']
        choice = data['choice']
        emailvalid = TouchForm({'email':email})
        if name=='Name':
            # message='请填写姓名'
            return HttpResponse('{"status":"fail","msg":"请填写姓名"}', content_type='application/json')
        elif (email=='Email')or(not emailvalid.is_valid()):
            # message='请填写邮件或检查邮件格式'
            return HttpResponse('{"status":"fail","msg":"请填写邮件或检查邮件格式"}', content_type='application/json')
        elif phone=='Phone' or len(str(phone))>20:
            # message='请填写电话或检查长度是否大于20'
            return HttpResponse('{"status":"fail","msg":"请填写电话或检查长度是否大于20"}', content_type='application/json')
        elif choice=='null':
            # message='请选择预约时间'
            return HttpResponse('{"status":"fail","msg":"请选择预约时间"}', content_type='application/json')
        elif content=='Message:维修、购车、试驾...':
            # message='请填写预约内容'
            return HttpResponse('{"status":"fail","msg":"请填写预约内容"}', content_type='application/json')
        else:
            userobj = models.Customer(
                cname = name,
                cgender = gender,
                tel = phone,
                email = email,
            )
            userobj.save()
            arrangeobj = models.WorkerArrange.objects.get(id=choice)
            arrangeobj.appostate='已预约'
            arrangeobj.save()
            appoobj = models.AppoInfo(
                id = arrangeobj,
                cusno = userobj,
                appocontent = content
            )
            appoobj.save()
            # message = '预约成功'
            return  HttpResponse('{"status":"success"}',content_type='application/json')

def home(request):
    pass
    return HttpResponse('个人中心')

#页面下方的提交邮箱
def touch(request):
    if request.method == 'POST':
        touchobj = TouchForm(request.POST)
        if touchobj.is_valid():
            data = touchobj.cleaned_data
            email = data.get('email')
            obj = models.Touch.objects.create(email=email,status='undo')
            obj.save()
            # messages.success(request, '发送成功')
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            # messages.error(request, '请检查邮件格式')
            # print(touchobj.errors)
            return HttpResponse('{"status":"fail"}', content_type='application/json')
    else:
        return HttpResponse('{"status":"1"}', content_type='application/json')

