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
            'package_membership_duration': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
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

class AuditForm(forms.ModelForm):
    class Meta:
        model = Audit
        fields = '__all__'
        widgets = {
            'name_auditor': forms.TextInput(attrs={'class': 'form-control'}),
            'practitioner_being_audited_charfield': forms.TextInput(attrs={'class': 'form-control'}),
            'practitioner_being_audited': forms.Select(attrs={'class': 'form-control'}),
            'transaction_activity': forms.Select(attrs={'class': 'form-control'}),
            'date_of_audit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  
            'email_practitioner': forms.EmailInput(attrs={'class': 'form-control'}),
            'qualification_practitioner': forms.Select(attrs={'class': 'form-control'}),
            'previous_audit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'special_notes_on_prev_audit_transaction': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'has_the_prac_been_issued_with_all_nedication_in_scope': forms.Select(attrs={'class': 'form-control'}),
            'expired_drugs': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = '__all__'
        widgets = {
            'date_of_request': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'first_day_of_leave_request': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'last_day_of_leave_request': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'employee_comments': forms.Textarea(attrs={'class': 'form-control'}),  
            'time_of_request': forms.TimeInput(attrs={'type': 'time','class': 'form-control'}),
            'employee_name_char': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_name': forms.Select(attrs={'class': 'form-control'}),
            'personal_email_address': forms.EmailInput(attrs={'type': 'email','class': 'form-control'}),
            'manager_supervisor_shift_lead': forms.TextInput(attrs={'class': 'form-control'}),  
            'employee_clock': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'request_type': forms.Select(attrs={'class': 'form-control'}),
        }


class PayrolDeductionForm(forms.ModelForm):
    class Meta:
        model = PayrolDeduction
        fields = '__all__'
        widgets = {
            'monthly_deduction_category': forms.Select(attrs={'class': 'form-control'}),
            'special_deduction_category': forms.Select(attrs={'class': 'form-control'}),
            'penalties_financial_loss_category': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'authorized_by': forms.Select(attrs={'class': 'form-control'}),
            'approver_comments': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PayrolDeductionFormView(forms.ModelForm):
    class Meta:
        model = PayrolDeduction
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'total_loss_deduction': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'total_special_deduction': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'total_monthly_deduction': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'expiry_date_penalty': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'start_date_penaly': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'installments_rand': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'employee_rand': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'employee_percentage_sign': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'description_deduction_penalty': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'total': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'monthly_r': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'total_amount_r': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'employe_name': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'employee_number': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'dept': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'email': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'description_deduction_monthly': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'description_deduction_special': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'amount': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'start_date_monthly': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'start_date_special': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'expiry_date_special': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'expiry_date_monthly': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'email': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'date_of_issuance': forms.DateInput(attrs={'class': 'form-control','type': 'date','readonly': True}),
            'monthly_deduction_category': forms.Select(attrs={'class': 'form-control','readonly': True}),
            'special_deduction_category': forms.Select(attrs={'class': 'form-control','readonly': True}),
            'penalties_financial_loss_category': forms.Select(attrs={'class': 'form-control','readonly': True}),
            'frequency': forms.Select(attrs={'class': 'form-control','readonly': True}),
            'authorized_by': forms.Select(attrs={'class': 'form-control','readonly': True}),
            'approver_comments': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
        }


class ScheduleStatus(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ScheduleAmount(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }