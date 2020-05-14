from django import forms
#
# class EditForm(forms.Form):
#     inputName=forms.CharField(max_length=20)
#     inputDept = forms.ChoiceField(widget=forms.Select(choices=["销售","维修","仓库","人事","财务"]))
#     inputPosition = forms.ChoiceField(widget=forms.Select(choices=["经理","总管","职员"]))

class AddForm(forms.Form):
    inputNumber=forms.CharField(max_length=20,required=True,widget=forms.TextInput(attrs={'class':"form-control"}))
    inputName=forms.CharField(max_length=20,required=True,widget=forms.TextInput(attrs={'class':"form-control"}))
    inputDept = forms.ChoiceField(choices=[("销售","销售"),("维修","维修"),("仓库","仓库"),("人事","人事"),("财务","财务")],
                                  widget = forms.Select(attrs={'class':"form-control custom-select"}))
    inputPostion = forms.ChoiceField(choices=[("经理","经理"),("总管","总管"),("职员","职员")],widget = forms.Select(attrs={'class':"form-control custom-select"}))

def checkwid(inputNumber):
    l=list(inputNumber)
    if l[0]=='W':
        return True
    else:
        return False
