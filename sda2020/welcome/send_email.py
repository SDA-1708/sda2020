#_author:'Palau'
#date:2020/4/28
import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'sda2020.settings'

if __name__ == '__main__':
    send_mail(
        '1',
        '2',
        'bw_yin@163.com',
        ['2200645266@qq.com'],
    )