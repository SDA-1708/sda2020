from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# 登陆信息维护
class Userinfo(AbstractUser):
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
    type = models.CharField(max_length=20,choices=(
        ('customer','顾客'),
        ('finance','财务'),
        ('HR','人事'),
        ('purchase','采购'),
        ('repair','维修'),
        ('sale','销售'),
        ('storage','仓库'),
    ))

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-c_time"]

# 客户信息
class Customer(models.Model):
    cusno = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=20)
    cgender = models.CharField(max_length=10,null=True,blank=True,choices=(
        ('male','男'),
        ('female','女'),
    ))
    tel = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    caddress = models.CharField(max_length=60, blank=True, null=True)
    account = models.OneToOneField(Userinfo,blank=True,null=True,on_delete=models.SET_NULL)

    class Meta:
        db_table = 'customer'

class MaintenanceWorker(models.Model):
    wid = models.OneToOneField('Worker', models.DO_NOTHING, db_column='wid', primary_key=True)
    wname = models.CharField(max_length=10)
    dept = models.CharField(max_length=20)
    postion = models.CharField(max_length=20)
    workload = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    class Meta:
        db_table = 'maintenance_worker'

class ServiceWorker(models.Model):
    wid = models.OneToOneField('Worker', models.DO_NOTHING, db_column='wid', primary_key=True)
    wname = models.CharField(max_length=10)
    dept = models.CharField(max_length=20)
    postion = models.CharField(max_length=20)
    order_finish = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'service_worker'

class Worker(models.Model):
    wid = models.CharField(primary_key=True, max_length=20)
    wname = models.CharField(max_length=10)
    dept = models.CharField(max_length=20)
    postion = models.CharField(max_length=20)
    account = models.OneToOneField(Userinfo, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        managed=False
        db_table = 'worker'

# 预约
class AppoInfo(models.Model):
    appoid = models.AutoField(primary_key=True)
    id = models.ForeignKey('WorkerArrange', models.DO_NOTHING,
                           db_column='id', related_name='App_id', null=True, blank=True)
    cusno = models.ForeignKey('Customer', models.DO_NOTHING, db_column='cusno', null=True, blank=True)
    appocontent = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'appo_info'

#排班
class WorkerArrange(models.Model):
    id = models.AutoField(primary_key=True)
    wid = models.ForeignKey(Worker, models.DO_NOTHING, db_column='wid',  null=True, blank=True)
    timeatwork = models.DateTimeField()
    appostate = models.CharField(max_length=20, blank=True, null=True)


    def profile1(self):
        if str(self.timeatwork.time())=='09:30:00':
            return '上午'
        else:
            return '下午'
    profile1.allow_tags = True

    class Meta:
        db_table = 'worker_arrange'
        unique_together = (('wid', 'timeatwork'),)

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('Userinfo',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': '+self.code

    class Meta:
        ordering = ["-c_time"]

class PsdConfirm(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('Userinfo', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.code

    class Meta:
        ordering = ["-c_time"]

#汽车信息，查询用
class CarInfo(models.Model):
    band = models.CharField(max_length=20)
    ctype = models.CharField(max_length=20)
    inventory = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    describe = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='carimage/', null=True,blank=True,verbose_name='配图')

    class Meta:
        db_table = 'car_info'
        unique_together = (('band', 'ctype'),)

class Touch(models.Model):
    email = models.EmailField(max_length=30)
    status = models.CharField(max_length=5, null=True, blank=True, choices=(
        ('done','已联系'),
        ('undo','未联系'),
    ))
    time = models.DateTimeField(auto_now_add=True)


# 开始
# Batch
# class Batch(models.Model):
#     id = models.AutoField(primary_key=True)
#     coid = models.ForeignKey('Components', models.DO_NOTHING, db_column='coid', null=True, blank=True)
#     purchaseid = models.ForeignKey('CoPurchase', models.DO_NOTHING, db_column='purchaseid', null=True, blank=True)
#     remainnum = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'batch'
#         unique_together = (('coid', 'purchaseid'),)

# Car
# class Car(models.Model):
#     cid = models.CharField(primary_key=True, max_length=20)
#     id = models.ForeignKey('CarInfo', models.DO_NOTHING, related_name='Car_id', db_column='id', blank=True, null=True)
#     real_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#
#     class Meta:
#         db_table = 'car'
#
# # carpurchase
# class CarPurchase(models.Model):
#     purchaseid = models.OneToOneField('Purchase', models.DO_NOTHING, db_column='purchaseid', primary_key=True)
#     id = models.ForeignKey(CarInfo, models.DO_NOTHING, related_name='Pur_id', db_column='id', blank=True, null=True)
#     purchasenum = models.IntegerField(blank=True, null=True)
#     purchasestate = models.CharField(max_length=20, blank=True, null=True)
#     psumprice = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     ptime = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'car_purchase'
#
# class CarShortage(models.Model):
#     car_shortage_id = models.CharField(db_column='Car_shortage_id', primary_key=True, max_length=20)
#     cusno = models.ForeignKey('Customer', models.DO_NOTHING, db_column='cusno', null=True, blank=True)
#     id = models.ForeignKey(CarInfo, models.DO_NOTHING, related_name='Shor_id', db_column='id', blank=True, null=True)
#     ct_date = models.DateTimeField(blank=True, null=True)
#     appo_price= models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     csstate = models.CharField(max_length=20, blank=True, null=True)
#
#     class Meta:
#         db_table = 'car_shortage'
#
# class Components(models.Model):
#     coid = models.CharField(primary_key=True, max_length=20)
#     coname = models.CharField(max_length=30, blank=True, null=True)
#     cotype = models.CharField(max_length=20, blank=True, null=True)
#     conumber = models.IntegerField(blank=True, null=True)
#     coprice = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#
#     class Meta:
#         db_table = 'components'
#
# class CoPurchase(models.Model):
#     purchaseid = models.OneToOneField('Purchase', models.DO_NOTHING, db_column='purchaseid', primary_key=True)
#     purchasenum = models.IntegerField(blank=True, null=True)
#     purchasestate = models.CharField(max_length=20, blank=True, null=True)
#     warehouse_time = models.DateTimeField(blank=True, null=True)
#     psumprice = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     ptime = models.DateTimeField(blank=True, null=True)
#     coid = models.ForeignKey('Components', models.DO_NOTHING, db_column='pur_coid', null=True, blank=True)
#
#     class Meta:
#         db_table = 'co_purchase'
#
# class CompoUseInfo(models.Model):
#     wsid = models.OneToOneField('Worksheet', models.DO_NOTHING, db_column='wsid', primary_key=True)
#     compo_use_state = models.CharField(max_length=20, blank=True, null=True)
#
#     class Meta:
#         db_table = 'compo_use_info'
#
# class FaultInfo(models.Model):
#     faultinfoid = models.CharField(primary_key=True, max_length=20)
#     coid = models.ForeignKey(Components, models.DO_NOTHING, db_column='coid', null=True, blank=True)
#     faultid = models.ForeignKey('FaultList', models.DO_NOTHING, db_column='faultid', null=True, blank=True)
#     renum = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'fault_info'
#
# class FaultList(models.Model):
#     faultid = models.CharField(primary_key=True, max_length=20)
#     faultname = models.CharField(max_length=30)
#     Fa_id = models.CharField(max_length=30, null=True)
#     eload = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
#
#     class Meta:
#         db_table = 'fault_list'
#
# class Orders(models.Model):
#     oid = models.CharField(primary_key=True, max_length=20)
#     ostate = models.CharField(max_length=20, blank=True, null=True)
#     sumprice = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     ostime = models.DateTimeField(blank=True, null=True)
#     oftime = models.DateTimeField(blank=True, null=True)
#     return_info = models.TextField(blank=True, null=True)
#     wid = models.ForeignKey('ServiceWorker', models.DO_NOTHING, db_column='wid', blank=True, null=True)
#
#     class Meta:
#         db_table = 'orders'
#
# class Pickuplist(models.Model):
#     pickid = models.CharField(primary_key=True, max_length=20)
#     cusno = models.ForeignKey(Customer, models.DO_NOTHING, db_column='cusno', null=True, blank=True)
#     cid = models.ForeignKey(Car, models.DO_NOTHING, db_column='cid', blank=True, null=True)
#     license = models.CharField(max_length=20, blank=True, null=True)
#     pickstate = models.CharField(max_length=10)
#
#     class Meta:
#         db_table = 'pickuplist'
#
# class Purchase(models.Model):
#     purchaseid = models.CharField(primary_key=True, max_length=20)
#     purchasenum = models.IntegerField(blank=True, null=True)
#     purchasestate = models.CharField(max_length=20, blank=True, null=True)
#     warehouse_time = models.DateTimeField(blank=True, null=True)
#     psumprice = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     ptime = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'purchase'
#
# class Worksheet(models.Model):
#     wsid = models.CharField(primary_key=True, max_length=20)
#     oid = models.ForeignKey(Orders, models.DO_NOTHING, db_column='oid', null=True, blank=True)
#     pickid = models.ForeignKey(Pickuplist, models.DO_NOTHING, db_column='pickid', null=True, blank=True)
#     wid = models.ForeignKey(MaintenanceWorker, models.DO_NOTHING, db_column='wid', null=True, blank=True)
#     wsstate = models.CharField(max_length=20, blank=True, null=True)
#     repeatnum = models.IntegerField(blank=True, null=True)
#     wsftime = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'worksheet'
#
# class WorksheetCompoInfo(models.Model):
#     id = models.AutoField(primary_key=True)
#     wsid = models.ForeignKey(Worksheet, models.DO_NOTHING, db_column='wsid', null=True, blank=True)
#     faultinfoid = models.ForeignKey(FaultInfo, models.DO_NOTHING, db_column='faultinfoid', null=True, blank=True)
#
#     class Meta:
#         db_table = 'worksheet_compo_info'
#         unique_together = (('wsid', 'faultinfoid'),)
#
#
