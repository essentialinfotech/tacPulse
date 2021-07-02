from re import U
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import fields
from .models import *
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','password1','password2',
                    'username','contact','address', 'is_staff','profile_pic','email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),          
        }


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','profile_pic','contact','address','quote','first_name','last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'quote': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssesmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssesmentForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', User)
        self.fields["to_user"].queryset = User.objects.filter(is_staff=True,is_superuser=False)
    class Meta:
        model = Assesment
        fields = '__all__'
        widgets = {
            'to_user': forms.Select(attrs={'class': 'form-control','required': True}),
            'msg': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.Select(attrs={'class': 'form-control'}),
            'warning':DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
        }

