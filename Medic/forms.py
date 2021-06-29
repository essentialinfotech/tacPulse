from django import forms
from .models import *


class AmbulanceModelForm(forms.ModelForm):
    class Meta:
        model = AmbulanceModel
        fields = '__all__'
