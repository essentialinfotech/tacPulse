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


class PropertyForm(forms.ModelForm):
    class Meta:
        model = PropertyTools
        fields = '__all__'
        widgets = {
            'property_type': forms.Select(attrs={'class': 'form-control','required': True}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'occurrence_type': forms.Select(attrs={'class': 'form-control'}),
            'equipement_name': forms.TextInput(attrs={'class': 'form-control'}),  
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'to_user': forms.TextInput(attrs={'class': 'form-control'}),
            'to_user_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}), 
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})     
        }
        