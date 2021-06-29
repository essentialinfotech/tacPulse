from django import forms
from django.db.models import fields
from .models import *


class ScheduleModelForm(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = '__all__'
