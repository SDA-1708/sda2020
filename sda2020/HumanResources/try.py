# workers = Worker.objects.all()
import datetime
monday, sunday = datetime.date.today(), datetime.date.today()
one_day = datetime.timedelta(days=1)
while monday.weekday() != 0:
    monday -= one_day
while sunday.weekday() != 6:
    sunday += one_day
# work_info = WorkerArrange.objects.filter(timeatwork__gte=monday, timeatwork__lte=sunday)


time_now=datetime.datetime.now()
print(time_now.time())

for day in range(7):
    day_now = sunday - day * one_day
    print(day_now==time_now.date())
