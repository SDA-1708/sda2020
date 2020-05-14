from django import forms

class AddCustomerForm(forms.Form):
    # inputNumber=forms.CharField(max_length=20,required=True,
    #                             widget=forms.TextInput(attrs={'class':"form-control"}))
    inputName=forms.CharField(max_length=20,required=True,
                              widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Enter name"}))
    inputGender = forms.ChoiceField(choices=[("male", "男"), ("female", "女")],
                                  widget=forms.Select(attrs={'class': "form-control custom-select"}))
    # inputGender = forms.CheckboxInput(attrs={'class': "form-control custom-select"})
    inputTel=forms.CharField(max_length=20,required=False,
                             widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Enter phone number"}))
    inputEmail=forms.CharField(max_length=30,required=False,
                               widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Enter email"}))
    inputAddress=forms.CharField(max_length=50,required=False,
                                 widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Enter address"}))


class CustomerInfoForm(forms.Form):
    inputNumber=forms.CharField(max_length=20,required=True,
                                widget=forms.TextInput(attrs={'class':"form-control"}))
