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


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'post': forms.Textarea(attrs={'class': 'form-control'}),
            }


class EmergencyMedDisIncidentReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmergencyMedDisIncidentReportForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance', User)
        self.fields["name_of_dispatcher"].queryset = User.objects.filter(is_superuser=False,is_staff = True)
        
    class Meta:
        model = AmbulanceModel
        fields = '__all__'
        widgets = {
                'run_id': forms.TextInput(attrs={'class': 'form-control'}),
                'chief_complain': forms.Textarea(attrs={'class': 'form-control','required': True}),
                'incident_category': forms.Select(attrs={'class': 'form-control'}),
                'ppe_lvl': forms.Select(attrs={'class': 'form-control'}),
                'pick_up_address': forms.TextInput(attrs={'class': 'form-control'}),
                'billing_type': forms.Select(attrs={'class': 'form-control'}),
                'billing_source': forms.Select(attrs={'class': 'form-control'}),
                'authorization_number': forms.TextInput(attrs={'class': 'form-control'}),
                'caller_name': forms.TextInput(attrs={'class': 'form-control'}),
                'caller_number': forms.TextInput(attrs={'class': 'form-control'}),
                'caller_company': forms.TextInput(attrs={'class': 'form-control'}),
                'call_received_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'time_call_posted_to_crew_on_whatsapp': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'crew_operational_status': forms.Select(attrs={'class': 'form-control'}),
                'how_many_units_dispatched': forms.Select(attrs={'class': 'form-control'}),
                'assigned_unit': forms.Select(attrs={'class': 'form-control'}),
                'vehicle_total': forms.Select(attrs={'class': 'form-control'}),
                'unit_reg': forms.TextInput(attrs={'class': 'form-control'}),
                'senior': forms.Select(attrs={'class': 'form-control'}),
                'assist01': forms.Select(attrs={'class': 'form-control'}),
                'assist02': forms.Select(attrs={'class': 'form-control'}),
                'loc': forms.Select(attrs={'class': 'form-control'}),
                'service_notes': forms.Select(attrs={'class': 'form-control'}),
                'scribe': forms.Select(attrs={'class': 'form-control'}),
                'service_note_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'service_note_description': forms.Textarea(attrs={'class': 'form-control'}),
                'unit': forms.Select(attrs={'class': 'form-control'}),
                'responding_address': forms.TextInput(attrs={'class': 'form-control'}),
                'scene_address': forms.TextInput(attrs={'class': 'form-control'}),
                'facility_address': forms.TextInput(attrs={'class': 'form-control'}),
                'end_address': forms.TextInput(attrs={'class': 'form-control'}),
                'patient': forms.Select(attrs={'class': 'form-control'}),
                'p_priority': forms.Select(attrs={'class': 'form-control'}),
                'p_lvl_of_care': forms.Select(attrs={'class': 'form-control'}),
                'p_name': forms.TextInput(attrs={'class': 'form-control'}),
                'p_medical_aid_plan_option': forms.TextInput(attrs={'class': 'form-control'}),
                'p_medical_aid': forms.TextInput(attrs={'class': 'form-control'}),
                'senior_practitioner_csn': forms.TextInput(attrs={'class': 'form-control'}),
                'name_of_dispatcher': forms.Select(attrs={'class': 'form-control'}),
                'was_the_call_handed_over_to_another_dispatcher': forms.Select(attrs={'class': 'form-control'}),
                'dispatch_special_notes': forms.Textarea(attrs={'class': 'form-control'}),
            }


class SeniorForm(forms.ModelForm):
    class Meta:
        model = Senior
        fields = '__all__'
        widgets = {
                'senior_name': forms.TextInput(attrs={'class': 'form-control'}),
            }

class ScribeForm(forms.ModelForm):
    class Meta:
        model = Scribe
        fields = '__all__'
        widgets = {
                'scribe_name': forms.TextInput(attrs={'class': 'form-control'}),
            }

class Assist01Form(forms.ModelForm):
    class Meta:
        model = Assist01
        fields = '__all__'
        widgets = {
                'a1_name': forms.TextInput(attrs={'class': 'form-control'}),
            }

class Assist02Form(forms.ModelForm):
    class Meta:
        model = Assist02
        fields = '__all__'
        widgets = {
                'a2_name': forms.TextInput(attrs={'class': 'form-control'}),
            }


class VehicleCountForm(forms.ModelForm):
    class Meta:
        model = Vehicles_count_with_info_for_ambulance_request
        fields = '__all__'
        widgets = {
                'vehicle_no': forms.TextInput(attrs={'class': 'form-control'}),
                'responding': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'odo01': forms.NumberInput(attrs={'class': 'form-control'}),
                'on_scene': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'odo2': forms.NumberInput(attrs={'class': 'form-control'}),
                'depart_scene': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'arrive_fac': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'odo3': forms.NumberInput(attrs={'class': 'form-control'}),
                'hand_over': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'depart': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'end_standing_free': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
                'odo04': forms.NumberInput(attrs={'class': 'form-control'}),
            }
                