from django import forms
from django.forms import ModelForm, fields
from .models import *

class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = Occurrence
        fields = ['occurrence_giver','related_user','occurrence_id', \
                 'occurrence_type','occurrence_detail','image']
        widgets = {
            'related_user': forms.Select(attrs={'class': 'form-control'}),
            'occurrence_type': forms.Select(attrs={'class': 'form-control'}),
            'occurrence_detail': forms.TextInput(attrs={'class': 'form-control'}),        
        }

class AmbulanceModelForm(forms.ModelForm):
    class Meta:
        model = AmbulanceModel
        fields = '__all__'
