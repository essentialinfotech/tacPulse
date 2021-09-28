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


class ElectricCashForm(forms.ModelForm):
    class Meta:
        model = Electric_Cash_Receipt
        fields = '__all__'
        widgets = {
            'company_or_patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control','type': 'email'}),
            'cus_number': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'run_id_or_reference': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Run ID / Reference'}),
        }

class ElectricCashInvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = Electric_Cash_Receipt_Invoice
        fields = '__all__'
        widgets = {
            'transaction': forms.Select(attrs={'class': 'form-control'}),
            'invoice': forms.TextInput(attrs={'class': 'form-control'}),
            'quote_invoice_amount': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'amount_received': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'amount_outstanding': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'cash_received_by': forms.Select(attrs={'class': 'form-control'}),
            'run_id_or_reference': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Run ID / Reference'}),
            'special_notes': forms.Textarea(attrs={'class': 'form-control','placeholder': 'No Note to record'}),
        }


class Expense_Reimbursement_Record_Form(forms.ModelForm):
    class Meta:
        model = Expense_Reimbursement_Record
        fields = '__all__'
        widgets = {
            'processing_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'name_and_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_or_start_date': forms.TextInput(attrs={'class': 'form-control'}),
            'personal_email': forms.EmailInput(attrs={'class': 'form-control','type': 'email'}),
        }


class ExpenseTransactionsForm(forms.ModelForm):
    class Meta:
        model = ExpenseTransactions
        fields = '__all__'
        widgets = {
            'date_of_expense': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'description_of_expense': forms.Textarea(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


class ExpenseRequestSummaryForm(forms.ModelForm):
    class Meta:
        model = ExpenseRequestSummary
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'total_reimbursement': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'reimbursement_method': forms.Select(attrs={'class': 'form-control'}),
        }

    
class Order_Cus_Info(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        widgets = {
            'p_o_req_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'transaction_cat': forms.Select(attrs={'class': 'form-control'}),
            'req_by': forms.Select(attrs={'class': 'form-control'}),
            'supplier_acc_or_job_card': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_or_company_name': forms.Select(attrs={'class': 'form-control'}),
            'supplier_contact_person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_contact_number': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'supplier_email': forms.EmailInput(attrs={'class': 'form-control','type': 'email'}),
            'street_addrs': forms.TextInput(attrs={'class': 'form-control'}),
            'city_province': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'shipping_method': forms.Select(attrs={'class': 'form-control'}),
            'courier_to_this_address': forms.Select(attrs={'class': 'form-control'}),
            'person_collecting': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VehicleMaintenanceForm(forms.ModelForm):
    class Meta:
        model = VehicleMaintenance
        fields = '__all__'
        widgets = {
            'item_description': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_no': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging': forms.Select(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'total': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class VehicleMaintenanceTotalsForm(forms.ModelForm):
    class Meta:
        model = VehicleMaintenanceTotal
        fields = '__all__'
        widgets = {
            'vehicle_call_assign': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TermsAndConditionsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions
        fields = '__all__'
        widgets = {
            'was_a_quotation_obtained_prior_to_purchase': forms.Select(attrs={'class': 'form-control'}),
        }


class PurchaseApprovalForm(forms.ModelForm):
    class Meta:
        model = PurchaseApproval
        fields = '__all__'
        widgets = {
            'quotation_approved': forms.TextInput(attrs={'class': 'form-control'}),
            'p_O_approval_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'p_O_approved_by': forms.Select(attrs={'class': 'form-control'}),
        }


class PO_Items_ReceivedForm(forms.ModelForm):
    class Meta:
        model = PO_Items_Received
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'date_of_items_received': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'initial_receiver_of_goods': forms.Select(attrs={'class': 'form-control'}),
        }


class Quality_Control_InspectionForm(forms.ModelForm):
    class Meta:
        model = Quality_Control_Inspection
        fields = '__all__'
        widgets = {
            'has_all_items_been_received': forms.Select(attrs={'class': 'form-control'}),
            'was_verification_done_to_ensure_that_what_was_ordered_is_what_was_received': forms.Select(attrs={'class': 'form-control'}),
            'purchase_inspected_by': forms.Select(attrs={'class': 'form-control'}),
            'was_verification_done_to_ensure_that_the_expiration_date_rule_was_complied_with': forms.Select(attrs={'class': 'form-control'}),
            'quality_control_notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'item_description': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_no': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging': forms.Select(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'total': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
        }


class Services_TrainingForm(forms.ModelForm):
    class Meta:
        model = Services_Training
        fields = '__all__'
        widgets = {
            'item_description': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_service': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
        }


class ProspectiveClientForm(forms.ModelForm):
    class Meta:
        model = ProspectiveClient
        fields = '__all__'
        widgets = {
            'doc_version': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'date_of_quote': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'name_poc': forms.TextInput(attrs={'class': 'form-control'}),
            'company_org_name': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control'}),
            'client_phone_no': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'clinet_email': forms.EmailInput(attrs={'class': 'form-control','type': 'email'}),
            'date_of_expiry': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'quote_prepared_by': forms.Select(attrs={'class': 'form-control'}),
        }


class ServiceDetailsForm(forms.ModelForm):
    class Meta:
        model = ServiceDetails
        fields = '__all__'
        widgets = {
            'service_req': forms.Select(attrs={'class': 'form-control'}),
            'run_id': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmergencyOperationsForm(forms.ModelForm):
    class Meta:
        model = EmergencyOperations
        fields = '__all__'
        widgets = {
            'level_of_care': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.Select(attrs={'class': 'form-control'}),
            'service_description': forms.TextInput(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'line_total': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
        }


class TotalCallCostingForm(forms.ModelForm):
    class Meta:
        model = TotalCallCosting
        fields = '__all__'
        widgets = {
            'special_notes': forms.Textarea(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'total_quotation_cost': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
        }


class EventsProspectiveClientForm(forms.ModelForm):
    class Meta:
        model = EventsProspectiveClient
        fields = '__all__'
        widgets = {
            'doc_version': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'date_of_quote': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'name_poc': forms.TextInput(attrs={'class': 'form-control'}),
            'company_org_name': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control'}),
            'client_phone_no': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
            'clinet_email': forms.EmailInput(attrs={'class': 'form-control','type': 'email'}),
            'date_of_expiry': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'quote_prepared_by': forms.Select(attrs={'class': 'form-control'}),
        }

class EventsServiceDetailsForm(forms.ModelForm):
    class Meta:
        model = EventsServiceDetails
        fields = '__all__'
        widgets = {
            'service_request': forms.Select(attrs={'class': 'form-control'}),
            'risk_lvl': forms.Select(attrs={'class': 'form-control'}),
            'evnt_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EventSportParticularsForm(forms.ModelForm):
    class Meta:
        model = EventSportParticulars
        fields = '__all__'
        widgets = {
            'date_of_service': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'service_description': forms.Select(attrs={'class': 'form-control'}),
            'loc_address': forms.TextInput(attrs={'class': 'form-control'}),
            'service_start_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'service_end_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'total_service_time': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
        }