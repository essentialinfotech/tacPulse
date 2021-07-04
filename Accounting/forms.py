from django import forms
from django.db.models import fields
from django.forms.widgets import DateInput
from .models import *


class ScheduleModelForm(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = '__all__'


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'
        widgets = {
            'p_name': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control','required': True}),
            'p_price': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'status': forms.Select(attrs={'class': 'form-control','required': True}),
            'is_valid': forms.Select(attrs={'class': 'form-control','required': True}),
            'valid_till': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        }
        
