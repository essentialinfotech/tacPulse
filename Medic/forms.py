from Accounting.models import Audit
from django import forms
from django.forms import ModelForm, fields
from .models import *


class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = Occurrence
        fields = '__all__'
        widgets = {
            'reason_for_report': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control','required': True}),
            'occurrence_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'incident_report': forms.Textarea(attrs={'placeholder': '(Provide ad much information as possible and be as comprehensive as possible)', 'class': 'form-control'}),   
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
            'price': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'status': forms.Select(attrs={'class': 'form-control'}), 
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})     
        }
        

class FAQFORM(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'ques': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'ans': forms.Textarea(attrs={'class': 'form-control','required': True}),
        }

    
class CaseForm(forms.ModelForm):
    class Meta:
        model = CaseNote
        fields = '__all__'
        widgets = {
            'case_panic': forms.Select(attrs={'class': 'form-control'}),
            'case_ambulance': forms.Select(attrs={'class': 'form-control'}),
            'case_note': forms.Textarea(attrs={'class': 'form-control','required': True}),
        }


class HospitalTransferForm(forms.ModelForm):
    class Meta:
        model = HospitalTransferModel
        fields = '__all__'
        widgets = {
                    'transfer_speed': forms.Select(attrs={'class': 'form-control'}),
                }
                