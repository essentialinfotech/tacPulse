from django import forms
from django.db.models import fields
from django.forms.widgets import DateInput
from .models import *


class ScheduleModelForm(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = '__all__'

        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'trip': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = '__all__'

        widgets = {
            'dispatch': forms.Select(attrs={'class': 'form-control'}),
            'task_title': forms.TextInput(attrs={'class': 'form-control'}),
            'task_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'scheduled_task': forms.Select(attrs={'class': 'form-control', 'onchange': "myFunction()"}),
            'ambulance_task': forms.Select(attrs={'class': 'form-control'}),
            'panic_task': forms.Select(attrs={'class': 'form-control'}),
        }


class TransferTaskForm(forms.ModelForm):
    class Meta:
        model = TaskTransferModel
        fields = '__all__'


class StockRequestForm(forms.ModelForm):
    class Meta:
        model = StockRequestModel
        fields = '__all__'


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'
        widgets = {
            'p_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'p_price': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'is_valid': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'valid_till': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PaystubForm(forms.ModelForm):
    class Meta:
        model = PaystubModel
        fields = '__all__'



class InspectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InspectionForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', User)
        if self.instance:
            self.fields["inspection_for"].queryset = User.objects.filter(is_staff=True,
                                                                         is_superuser=False,
                                                                         is_active = True)
    class Meta:
        model = InspectionModel
        fields = '__all__'
        widgets = {
            'inspection_for': forms.Select(attrs={'class': 'form-control'}),
            'inspection_type': forms.Select(attrs={'class': 'form-control'}),
            'inspection_output': forms.Select(attrs={'class': 'form-control'}),
            'inspection_detail': forms.TextInput(attrs={'class': 'form-control'}),
        }

