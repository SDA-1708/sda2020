#_author:'Palau'
#date:2020/4/23
from django import forms
import re
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from . import models
from captcha.fields import CaptchaField

def name_valid(value):
    name_re = re.compile(r'^[\d]+')
    ret = name_re.match(value)
    if ret:
        raise ValidationError('用户名不能以数字开头！')

class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='用户名：',
        min_length=5,
        max_length=32,
        help_text='只能有字母数字下划线组成，且不能以数字开头，长度6到32位！',
        # initial='admin123_',
        error_messages={
            'required': '用户名不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', '用户名只能包含字母数字下划线！'), name_valid],
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "用户名（必填）", 'autocomplete': "off"})
    )
    password = forms.CharField(
        required=True,
        label='密码：',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True,attrs={'class': "form-control", 'placeholder': "密码（必填）", 'autocomplete': "off"}),
    )
    r_password = forms.CharField(
        required=True,
        label='确认密码：',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True,attrs={'class': "form-control", 'placeholder': "确认密码（必填）", 'autocomplete': "off"}),
    )

    name = forms.CharField(
        required=True,
        label='姓名',
        max_length=32,
        error_messages={
            'required':'姓名不能为空!',
            'max_length': '长度不能超过32位!',
        },
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "姓名（必填）", 'autocomplete': "off"})
    )

    email = forms.EmailField(
        required=True,
        label='邮箱',
        error_messages={
            'required': '邮箱不能为空！',
        },
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "邮箱（必填）", 'autocomplete': "off"})
    )

    gender = forms.CharField(
        initial=1,
        required=False,
        label='性别',
        widget=forms.Select(choices=(('male', '男'), ('female', '女'),),attrs={'class': "form-control"}),
    )

    phone = forms.CharField(
        required=False,
        label='电话',
        max_length=16,
        min_length=3,
        error_messages={
            'min_length':'长度不能少于3位',
            'max_length':'长度不能大于16位',
        },
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "电话", 'autocomplete': "off"})
    )

    address = forms.CharField(
        required=False,
        label='地址',
        max_length=60,
        error_messages={
            'max_length':'长度不能大于60位',
        },
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "地址", 'autocomplete': "off"})
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        pass
        return self.cleaned_data.get('name')

    def clean_password(self):
        pass
        return self.cleaned_data.get('password')

    def clean_r_password(self):
        pass
        return self.cleaned_data.get('r_password')

    def clean_email(self):
        pass
        return self.cleaned_data.get('email')

    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')
        if password != r_password:
            self.add_error('r_password', '两次密码不一致！')
            raise ValidationError('两次密码不一致！')
        else:
            return self.cleaned_data


class Search(forms.Form):
    text = forms.CharField(max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='用户名',
        max_length=30,
        min_length=5,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'长度不能低于5位',
            'max_length':'长度不能大于30位',
        },
        widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"用户名",'autocomplete':"off"})
    )

    password = forms.CharField(
        required=True,
        label='密码',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True,attrs={'class':"form-control",'placeholder':"密码",'autocomplete':"off"}),
    )

    captcha = CaptchaField(label='验证码')

class ResetForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        label='旧密码',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True,attrs={'class':"form-control",'placeholder':"旧密码",'autocomplete':"off"}),
    )

    new_password = forms.CharField(
        required=True,
        label='新密码',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True,attrs={'class':"form-control",'placeholder':"新密码",'autocomplete':"off"}),
    )

    r_new_password = forms.CharField(
        required=True,
        label='确认新密码',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True,attrs={'class':"form-control",'placeholder':"确认新密码",'autocomplete':"off"}),
    )


# class AppoForm(forms.Form):
#     name = forms.CharField(
#         required=True,
#         label='姓名',
#         max_length=32,
#         error_messages={
#             'required':'姓名不能为空!',
#             'max_length': '长度不能超过32位!',
#         }
#     )
#
#     email = forms.EmailField(
#         required=True,
#         label='邮箱',
#         error_messages={
#             'required': '邮箱不能为空！',
#         }
#     )
#
#     gender = forms.ChoiceField(
#         choices=(('male', '男'), ('female', '女'),),
#         initial=1,
#         required=False,
#         label='性别',
#         widget=widgets.RadioSelect(),
#     )
#
#     phone = forms.CharField(
#         required=False,
#         label='电话',
#         max_length=16,
#         min_length=3,
#         error_messages={
#             'min_length':'长度不能少于3位',
#             'max_length':'长度不能大于16位',
#         }
#     )
#
#     choice = forms.CharField(
#         required=False,
#         label='地址',
#         max_length=60,
#         error_messages={
#             'max_length':'长度不能大于60位',
#         }
#     )

class TouchForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='邮箱',
        error_messages={
            'required': '邮箱不能为空！',
            'valid':'邮箱格式错误',
        }
    )