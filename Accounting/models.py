from django import dispatch
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.fields import DateTimeField
from Accounts.models import User
from Medic.models import *
from Accounts.models import *
from django.db.models.signals import ModelSignal, post_save
from django.dispatch import receiver

# Create your models here.


class Package(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]

    Declaration = [
        ('Date will be declared', 'Date will be declared'),
        ('Date Declared', 'Date Declared'),
        ('Constant', 'Constant'),
    ]

    p_name = models.CharField(max_length=100)
    p_price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    is_valid = models.CharField(max_length=100, choices=Declaration)
    valid_till = models.DateField(blank=True, null=True)
    package_membership_duration = models.CharField(blank=True, null=True,max_length=50)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.p_name


class PaystubModel(models.Model):
    dispatch = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='paystub/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dispatch.first_name + ' ' + self.dispatch.last_name


class MembershipModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    package = models.ForeignKey(Package,on_delete=SET_NULL,blank=True, null=True)
    token = models.CharField(max_length=500,blank=True, null=True)
    membership_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    membership_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.package)


class MembershipNoti(models.Model):
    membership = models.ForeignKey(MembershipModel, on_delete=models.CASCADE)
    noti_text = models.CharField(max_length=100,default='User purchased membership')
    created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.membership.user.first_name

class MembershipRenewalNoti(models.Model):
    noti_for = models.ForeignKey(MembershipModel,on_delete=models.CASCADE)
    noti_text = models.CharField(max_length=100,default='')
    is_seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.noti_for.membership_end)

@receiver(post_save, sender=MembershipModel)
def create_membership_noti(sender, instance=None, created=False, **kwargs):
    if created:
        MembershipNoti.objects.create(membership=instance)


class StockRequestModel(models.Model):
    receiver = models.CharField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    message_body = models.CharField(max_length=1000, blank=False, null=False)
    attachment = models.FileField(upload_to='attachment', blank=True)
    requested = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class ScheduleModel(models.Model):
    status_type = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
    ]
    trip_type = [
        ('Single', 'Single'),
        ('Round Trip', 'Round Trip'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    contact = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(max_length=250, blank=False, null=False)
    from_loc = models.CharField(max_length=100, blank=False, null=False)
    from_lat = models.CharField(max_length=100, blank=False, null=False)
    from_long = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    latitude = models.CharField(max_length=100, blank=False, null=False)
    longitude = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(
        choices=status_type, max_length=100, blank=True, null=True, default='Pending')
    trip = models.CharField(choices=trip_type, max_length=100,
                            blank=True, null=True, default='Single')
    distance = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=50,blank=True,null=True)
    assigned = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location


class TaskModel(models.Model):
    status_type = [
        ('Assigned', 'Assigned'),
        ('Transferred', 'Transferred'),
        ('Completed', 'Completed'),
    ]
    typeof = [
        ('sch', 'Scheduled Task'),
        ('ambr', 'Ambulance Request'),
        ('pan', 'Panic Request'),
        ('HT', 'Hospital Transfer')
    ]
    task_type = models.CharField(
        choices=typeof, max_length=100, blank=True, null=True)
    dispatch = models.ForeignKey(User, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=100, blank=False, null=False)
    task_desc = models.TextField(max_length=1000, blank=True, null=True)
    scheduled_task = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE, null=True, blank=True)
    ambulance_task = models.ForeignKey(AmbulanceModel, on_delete=models.CASCADE, blank=True, null=True)
    panic_task = models.ForeignKey(
        Panic, on_delete=models.CASCADE, blank=True, null=True)
    hos_tra = models.ForeignKey(HospitalTransferModel, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        choices=status_type, max_length=100, blank=True, null=True, default='Assigned')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dispatch.first_name + ' ' + self.dispatch.last_name


class TaskTransferModel(models.Model):
    dispatch = models.ForeignKey(User, on_delete=models.CASCADE)
    transferred_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by', blank=True, null=True)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, blank=True, null=True)
    transfer_reason = models.TextField(max_length=100, blank=False, null=False)
    transfer_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transferred to { self.transfer_to }"


class InspectionModel(models.Model):
    Type = [
        ('Property', 'Property'),
        ('Dispatch', 'Dispatch')
    ]

    Result = [
        ('Good', 'Good'),
        ('Bad', 'Bad'),
    ]

    inspector = models.ForeignKey(User,on_delete=SET_NULL,blank=True,null=True)
    inspection_for = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='inpected_user')
    inspection_type = models.CharField(max_length=20,blank=True,null=True,choices=Type)
    inspection_output = models.CharField(max_length=20,blank=True,null=True,choices=Result)
    inspection_detail = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inspection_type}"


class Audit(models.Model):
    TRANSACTION_ACTIVITY = [
        ('Stock Issue','Stock Issue'),
        ('Monthly Individual Audit','Monthly Individual Audit'),
        ('Special Audit', 'Special Audit'),
        ('Out-Processing Procedures', 'Out-Processing Procedures'),
    ]

    QUALIFICATION_PRACTITIONER = [
        ('Intermediate Life SUpport','Intermediate Life SUpport'),
        ('Advanced Life Support(CCA/N.Dip)', 'Advanced Life Support(CCA/N.Dip)'),
        ('Emergebcy Care Assistant', 'Emergebcy Care Assistant'),
        ('Emergency Care Technician', 'Emergency Care Technician'),
        ('Emergency Care Practitioner', 'Emergency Care Practitioner'),
        ('Medical Practitioner','Medical Practitioner'),
    ]

    ISSUED_WITH_ALL_NEDICATION = [
        ('Yes','Yes'),
        ('No','No'),
    ]
    name_auditor = models.CharField(max_length=100,blank=True, null=True)
    auditor = models.ForeignKey(User,on_delete = models.CASCADE,blank=True, null=True,related_name='auditor_info')
    practitioner_being_audited_charfield = models.CharField(max_length=100,blank=True, null=True)
    practitioner_being_audited = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='practitioner_info')
    transaction_activity = models.CharField(max_length = 100,blank=True, null=True,choices=TRANSACTION_ACTIVITY)
    date_of_audit = models.DateField(blank=True, null=True)
    email_practitioner = models.EmailField(blank=True, null=True)
    qualification_practitioner = models.CharField(max_length = 100,blank=True, null=True,choices=QUALIFICATION_PRACTITIONER)
    previous_audit = models.DateField(blank=True, null=True)
    special_notes_on_prev_audit_transaction = models.TextField(blank=True, null=True)
    has_the_prac_been_issued_with_all_nedication_in_scope = models.CharField(
        max_length=100,blank=True, null=True,choices=ISSUED_WITH_ALL_NEDICATION
    )
    expired_drugs = models.CharField(max_length=100,blank=True, null=True)
    signature_field = models.CharField(max_length=100,blank=True, null=True)
    created = models.DateTimeField( auto_now_add = True )


class Leaves(models.Model):
    TYPE = [
        ('Sick Leave','Sick Leave'),
        ('Family Responsibility Leave', 'FAmily Responsibility Leave'),
        ('Study Leave','Study Leave'),
        ('Maternity Leave','Maternity Leave'),
        ('Unpaid Leave','Unpaid Leave'),
    ]
    date_of_request = models.DateField(blank=True, null=True)
    time_of_request = models.TimeField(blank=True, null=True)
    employee_name_char = models.CharField(max_length=50,blank=True, null=True)
    employee_name = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    personal_email_address = models.EmailField(blank=True, null=True)
    manager_supervisor_shift_lead = models.CharField(blank=True, null=True,max_length=50)
    employee_clock = models.CharField(max_length=1000,blank=True, null=True)
    request_type = models.CharField(max_length=100,blank=True, null=True,choices=TYPE)
    first_day_of_leave_request = models.DateTimeField(blank=True, null=True)
    last_day_of_leave_request = models.DateTimeField(blank=True, null=True)
    total_num_in_days = models.CharField(blank=True, null=True,max_length=50)
    employee_comments = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=100,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class PayrolDeduction(models.Model):
    MONTHLY_CATEGORY = [
        ('Company Provided Housing', 'Company Provided Housing'),
        ('Cellular Data Allowance', 'Cellular Data Allowance'),
        ('Garnishing Order', 'Garnishing Order'),
        ('Monthly Deduction Agreement-Employee Request', 'Monthly Deduction Agreement-Employee Request'),
        ('other(See Notes)', 'other(See Notes)'),
    ]

    SPECIAL_CATEGORY_DEDUCTIONS = [
        ('Salary Advance','Salary Advance'),
        ('Cellular Data Allowance - Once off','Cellular Data Allowance - Once off'),
        ('Annual HPCSA Renewal','Annual HPCSA Renewal'),
        ('Salary Corrections (Payroll Error)','Salary Corrections (Payroll Error)'),
        ('External Training','External Training'),
        ('Small Loan','Small Loan'),
        ('Employee Request / Agreement(Once off)','Employee Request / Agreement(Once off)'),
        ('Other','Other'),
    ]

    Penalties_Financial_loss_deduction_categories = [
        ('Fines / Penalties','Fines / Penalties'),
        ('Equipment Loss and/or Vehicle Damage','Equipment Loss and/or Vehicle Damage'),
        ('Unauthorized Shift Changes-Overhead Payback','Unauthorized Shift Changes-Overhead Payback'),
        ('Unauthorized Comany Vehivle Use','Unauthorized Comany Vehivle Use'),
        ('Procedure Violence','Procedure Violence'),
        ('Traffic Fines','Traffic Fines'),
    ]

    FREQUENCY = [
        ('Once off','Once off'),
        ('2 Months','2 Months'),
        ('3 Months','3 Months'),
    ]

    AUTHORIZED_BY = [
        ('Leaghnard Coestzee-Pestana(MD)','Leaghnard Coestzee-Pestana(MD)'),
        ('Frankey Pestana-Coetzee','Frankey Pestana-Coetzee'),
    ]

    report_by = models.ForeignKey(User,on_delete=SET_NULL,blank=True, null=True,related_name='report_giver')
    reportedfor = models.ForeignKey(User,on_delete=SET_NULL,blank=True, null=True,related_name='report_taker')
    employe_name = models.CharField(max_length=50,blank=True, null=True)
    employee_number = models.CharField(max_length=50,blank=True, null=True)
    dept = models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_issuance = models.DateField(blank=True, null=True)

    photo_evi1 = models.ImageField(upload_to = 'PayrollDeduction',blank=True, null=True)
    photo_evi2 = models.ImageField(upload_to = 'PayrollDeduction',blank=True, null=True)
    photo_evi3 = models.ImageField(upload_to = 'PayrollDeduction',blank=True, null=True)
    photo_evi4 = models.ImageField(upload_to = 'PayrollDeduction',blank=True, null=True)

    monthly_deductions = models.BooleanField(default=False)
    special_deductions = models.BooleanField(default=False)
    penalties_financial_loss = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    monthly_deduction_category = models.CharField(max_length=50,blank=True, null=True,choices=MONTHLY_CATEGORY)
    special_deduction_category = models.CharField(max_length=50,blank=True, null=True,choices=SPECIAL_CATEGORY_DEDUCTIONS)
    penalties_financial_loss_category = models.CharField(max_length=50,blank=True, null=True,choices=Penalties_Financial_loss_deduction_categories)

    # monthly
    description_deduction_monthly = models.TextField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True, default=0)
    start_date_monthly = models.DateField(blank=True, null=True)
    expiry_date_monthly = models.DateField(blank=True, null=True)

    # special
    description_deduction_special = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=20,blank=True, null=True,choices=FREQUENCY)
    total_amount_r = models.IntegerField(blank=True, null=True, default=0)
    monthly_r = models.IntegerField(blank=True, null=True, default=0)
    start_date_special = models.DateField(blank=True, null=True)
    expiry_date_special = models.DateField(blank=True, null=True)

    # penalty
    description_deduction_penalty = models.TextField(blank=True, null=True)
    employee_percentage_sign = models.IntegerField(blank=True, null=True, default=0)
    total = models.IntegerField(blank=True, null=True)
    employee_rand = models.IntegerField(blank=True, null=True, default=0)
    installments_rand = models.IntegerField(blank=True, null=True, default=0)
    start_date_penaly = models.DateField(blank=True, null=True)
    expiry_date_penalty = models.DateField(blank=True, null=True)

    total_monthly_deduction = models.IntegerField(blank=True, null=True, default=0)
    total_special_deduction = models.IntegerField(blank=True, null=True, default=0)
    total_loss_deduction = models.IntegerField(blank=True, null=True, default=0)
    authorized_by = models.CharField(max_length = 50, blank=True, null=True,choices=AUTHORIZED_BY)
    approver_comments = models.TextField(blank=True, null=True)
    approver_signature = models.CharField(max_length = 200,blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    @property
    def image1URL(self):
        try:
            url = self.photo_evi1.url
        except:
            url = ''
        return url

    @property
    def image2URL(self):
        try:
            url = self.photo_evi2.url
        except:
            url = ''
        return url

    @property
    def image3URL(self):
        try:
            url = self.photo_evi3.url
        except:
            url = ''
        return url

    @property
    def image4URL(self):
        try:
            url = self.photo_evi4.url
        except:
            url = ''
        return url


# Finane
class Electric_Cash_Receipt(models.Model):
    company_or_patient_name = models.CharField(blank=True,null=True,max_length=100)
    customer_email = models.EmailField(blank=False,null=True)
    cus_number = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField()
    time = models.TimeField()
    # reason for payment
    run_id_or_reference = models.CharField(max_length=200,blank=True,null=True,unique=True)

    def __str__(self):
        return str(self.id)

class Invoice_cash_received_by(models.Model):
    receiver_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receiver_name

class Electric_Cash_Receipt_Invoice(models.Model):

    TRANSACTION = [
        ('ALS CALL Out','ALS CALL Out'),
        ('EMS CALL','EMS CALL'),
        ('Equipment Purchase','Equipment Purchase'),
        ('ILS CALL OUT','ILS CALL OUT'),
        ('SPORT STANDBY','SPORT STANDBY'),
        ('TRAINING SERVICES','TRAINING SERVICES'),
        ('OTHER','OTHER'),
    ]

    invo_for = models.ForeignKey(Electric_Cash_Receipt,on_delete=models.CASCADE,blank=True,null=True)
    transaction = models.CharField(max_length=500,blank=True,null=True,choices=TRANSACTION)
    invoice = models.CharField(max_length=200,blank=True,null=True)
    quote_invoice_amount = models.PositiveIntegerField(blank=True,null=True)
    amount_received = models.PositiveIntegerField(blank=True,null=True)
    amount_outstanding = models.PositiveIntegerField(blank=True,null=True)

    cash_received_by = models.ForeignKey(Invoice_cash_received_by,on_delete=SET_NULL,blank=True,null=True)
    receiver_signature = models.FileField(upload_to='InvoiceReceiverSignature',blank=True,null=True)
    customer_signature = models.FileField(upload_to='InvoiceCustomerSignature', blank=True,null=True)
    special_notes = models.TextField()

    def __str__(self):
        return str(self.invo_for.id)


class Expense_Reimbursement_Record(models.Model):
    processing_date = models.DateField()
    name_and_surname = models.CharField(max_length=80,blank=True,null=True)
    dept = models.CharField(max_length=300,blank=True,null=True)
    employment_or_start_date = models.CharField(max_length=80,default='T21')
    personal_email = models.EmailField(default='tloumojela2371@gmail.com')


class ExpenseTransactions(models.Model):
    REASON = [
        ('Pre-Employment Requirements','Pre-Employment Requirements'),
        ('Operational Expense','Operational Expense'),
        ('Staff Food','Staff Food'),
        ('Other','Other'),
    ]

    PAYMENT_METHOD = [
        ('Cash','Cash'),
        ('Cash Voucher','Cash Voucher'),
        ('Company Card','Company Card'),
        ('Director Personal Card','Director Personal Card'),
        ('EFT','EFT'),
    ] 

    table_for = models.ForeignKey(Expense_Reimbursement_Record,on_delete=SET_NULL,blank=True,null=True)
    description_of_expense = models.TextField()
    date_of_expense = models.DateField()
    reason = models.CharField(max_length=80,choices=REASON)
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=80,choices=PAYMENT_METHOD)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.table_for.id)


class PhotoGraphicalEvidence(models.Model):
    photo_for = models.ForeignKey(Expense_Reimbursement_Record, on_delete=models.CASCADE,blank=True,null=True)
    photo = models.FileField(upload_to='Expense_Reimbursement_Record')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.photo_for.id)


class ExpenseRequestSummary(models.Model):

    REIMBURSEMENT_METHOD = [
        ('Petty Cash','Petty Cash'),
        ('Immediate EFT','Immediate EFT'),
        ('Cash Voucher / E-Wallet','Cash Voucher / E-Wallet'),
        ('Include in Next Salary','Include in Next Salary'),
    ]

    summary_for = models.ForeignKey(Expense_Reimbursement_Record, on_delete=SET_NULL,blank=True,null=True)
    total_reimbursement = models.PositiveIntegerField(blank=True,null=True)
    reimbursement_method = models.CharField(max_length=100,choices=REIMBURSEMENT_METHOD)
    comments = models.TextField(blank=True,null=True)
    requester_signature = models.FileField(upload_to='EXPENSEREIMBURSEMENT',blank=True,null=True)

    def __str__(self):
        return str(self.summary_for.id)




class RequestedBy(models.Model):
    requested_by_name = models.CharField(max_length=500,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.requested_by_name

class SupplierOrCompany(models.Model):
    name = models.CharField(max_length=500,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CourierToThisAddress(models.Model):
    address_name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address_name

class PurchaseOrder(models.Model):
    TRANSACTION_CATEGORY = [
        ('Services / Training','Services / Training'),
        ('Products','Products'),
        ('Vehicle Maintenance','Vehicle Maintenance'),
    ]

    SHIPPING_ADDRESS = [
        ('Courier','Courier'),
        ('Collection','Collection'),
        ('Hand Delivery','Hand Delivery'),
    ]

    p_o_req_date = models.DateField()
    req_by = models.ForeignKey(RequestedBy,on_delete=SET_NULL,blank=True,null=True)
    transaction_cat = models.CharField(max_length=100,choices=TRANSACTION_CATEGORY)
    supplier_acc_or_job_card = models.CharField(max_length=200)
    supplier_or_company_name = models.ForeignKey(SupplierOrCompany, on_delete=SET_NULL,blank=True,null=True)
    supplier_contact_person_name = models.CharField(max_length=100,blank=True,null=True)
    supplier_contact_number = models.PositiveIntegerField(blank=True,null=True)
    supplier_email = models.EmailField(blank=True,null=True)
    street_addrs = models.CharField(max_length=100)
    city_province = models.CharField(max_length=100)
    zip_code = models.PositiveIntegerField()

    # shipping
    shipping_method = models.CharField(max_length=200,choices=SHIPPING_ADDRESS)
    # if courier
    courier_to_this_address = models.ForeignKey(CourierToThisAddress,on_delete=SET_NULL,blank=True,null=True)
    # if collection
    person_collecting = models.CharField(max_length=300,blank=True,null=True)


class PackagingForVehicle(models.Model):
    p_name = models.CharField(max_length=500,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.p_name

class VehicleMaintenance(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,blank=True,null=True)
    item_description = models.CharField(max_length=500)
    stock_no = models.CharField(max_length=200,blank=True,null=True)
    packaging = models.ForeignKey(PackagingForVehicle,on_delete=SET_NULL,blank=True,null=True)
    qty = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    total = models.PositiveIntegerField(blank=True,null=True)
    comment = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.order.id)

class VehicleCallAsign(models.Model):
    v_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.v_name

class VehicleMaintenanceTotal(models.Model):
    order_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    vehicle_call_assign = models.ForeignKey(VehicleCallAsign,blank=True,null=True,on_delete=SET_NULL)
    totals = models.IntegerField(blank=True,null=True)
    year = models.CharField(max_length=100,blank=True,null=True)
    make = models.CharField(max_length=100,blank=True,null=True)
    model = models.CharField(max_length=100,blank=True,null=True)
    vin = models.CharField(max_length=1000,blank=True,null=True)

    def __str__(self):
        return str(self.order_for.id)


class Product(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,blank=True,null=True)
    item_description = models.CharField(max_length=500)
    stock_no = models.CharField(max_length=200,blank=True,null=True)
    packaging = models.ForeignKey(PackagingForVehicle,on_delete=SET_NULL,blank=True,null=True)
    qty = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    total = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.order.id)

class Product_totals(models.Model):
    order_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    totals = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.order_for.id)


class Services_Training(models.Model):
    service_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    item_description = models.CharField(max_length=500)
    date_of_service = models.DateField()
    unit_price = models.PositiveIntegerField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.service_for.id)

class Service_Totals(models.Model):
    service_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    totals = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.service_for.id)


class TermsAndConditions(models.Model):

    WAS_A_QUOTATION_OBTAINED_PRIOR_TO_PURCHASE = [
        ('Yes','Yes'),
        ('No','No'),
    ]

    terms_for = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,blank=True,null=True)
    special_comments = models.TextField()
    was_a_quotation_obtained_prior_to_purchase = models.CharField(max_length=10,choices=WAS_A_QUOTATION_OBTAINED_PRIOR_TO_PURCHASE)
    copy_of_quotation_1 = models.FileField(upload_to='Order',blank=True,null=True)
    copy_of_quotation_2 = models.FileField(upload_to='Order',blank=True,null=True)
    copy_of_quotation_3 = models.FileField(upload_to='Order',blank=True,null=True)
    copy_of_quotation_4 = models.FileField(upload_to='Order',blank=True,null=True)
    def __str__(self):
        return str(self.terms_for.id)


class POAPPROVEDBY(models.Model):
    approver_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.approver_name

class PurchaseApproval(models.Model):
    approval_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    quotation_approved = models.CharField(max_length=100,blank=True,null=True)
    p_O_approval_date = models.DateField()
    p_O_approved_by = models.ForeignKey(POAPPROVEDBY,on_delete=SET_NULL,blank=True,null=True)
    approval_signature = models.FileField(upload_to='Order',blank=True,null=True)
    po_items_received = models.BooleanField(default=False)
    quality_assurance_check = models.BooleanField(default=False)


class InitialReceiverOfGoods(models.Model):
    r_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.r_name


class PO_Items_Received(models.Model):
    received_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    date_of_items_received = models.DateField()
    p_i_1 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_2 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_3 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_4 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_5 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_6 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_7 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_8 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_9 = models.FileField(upload_to='Order',blank=True,null=True)
    p_i_10 = models.FileField(upload_to='Order',blank=True,null=True)

    sup_invoice_1 = models.FileField(upload_to='Order',blank=True,null=True)
    sup_invoice_2 = models.FileField(upload_to='Order',blank=True,null=True)
    sup_invoice_3 = models.FileField(upload_to='Order',blank=True,null=True)
    sup_invoice_4 = models.FileField(upload_to='Order',blank=True,null=True)
    sup_invoice_5 = models.FileField(upload_to='Order',blank=True,null=True)
    initial_receiver_of_goods = models.ForeignKey(InitialReceiverOfGoods, on_delete=SET_NULL,blank=True,null=True)
    initial_receiver_signature = models.FileField(upload_to='Order',blank=True,null=True)
    comments = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.received_for.id)

class PurchaseInspectedBy(models.Model):
    inpector_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.inpector_name

class Quality_Control_Inspection(models.Model):

    HAS_ALL_ITEMS_BEEN_RECEIVED = [
        ('Yes','Yes'),
        ('Pending B/O','Pending B/O'),
    ]

    WHAT_WAS_RECEIVED = [
        ('Yes','Yes'),
        ('No','No'),
    ]

    VERIFICATION_EXPIRATION_DATE_RULE = [
        ('Yes','Yes'),
        ('No','No'),
    ]

    quality_for = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True)
    purchase_inspected_by = models.ForeignKey(PurchaseInspectedBy,on_delete=SET_NULL,blank=True,null=True)
    has_all_items_been_received = models.CharField(max_length=200,choices=HAS_ALL_ITEMS_BEEN_RECEIVED)
    was_verification_done_to_ensure_that_what_was_ordered_is_what_was_received = models.CharField(max_length=50,choices=WHAT_WAS_RECEIVED)
    was_verification_done_to_ensure_that_the_expiration_date_rule_was_complied_with = models.CharField(max_length=20,choices=VERIFICATION_EXPIRATION_DATE_RULE)
    quality_control_notes = models.TextField(blank=True,null=True)
    quality_control_signature = models.FileField(upload_to='Order',blank=True,null=True)

    def __str__(self):
        return str(self.quality_for.id)


#quotation emergency operations
class QuotePreparedBy(models.Model):
    prepared_by = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prepared_by

class ProspectiveClient(models.Model):
    doc_version = models.PositiveIntegerField(blank=True,null=True)
    date_of_quote = models.DateField(blank=True,null=True)
    name_poc = models.CharField(max_length=100,blank=True,null=True)
    company_org_name = models.CharField(max_length=100,blank=True,null=True)
    physical_address = models.TextField()
    client_phone_no = models.PositiveIntegerField()
    clinet_email = models.EmailField(blank=True,null=True)
    date_of_expiry = models.DateField()
    quote_prepared_by = models.ForeignKey(QuotePreparedBy, on_delete=SET_NULL,blank=True,null=True)
    

class ServiceRequest(models.Model):
    service_request = models.CharField(max_length=600)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_request

class ServiceDetails(models.Model):
    parent = models.ForeignKey(ProspectiveClient,on_delete=models.CASCADE,blank=True,null=True)
    service_req = models.ForeignKey(ServiceRequest, on_delete=SET_NULL,blank=True,null=True)
    run_id = models.CharField(max_length=1000,blank=True,null=True)
    special_notes = models.BooleanField(default=False)

    def __str__(self):
        return str(self.parent.id)

class Code(models.Model):
    code_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code_name

class EmergencyOperations(models.Model):

    LEVEL_OF_CARE = [
        ('Basic Life Support','Basic Life Support'),
        ('Intermediate Life Support','Intermediate Life Support'),
        ('Advanced Life Support','Advanced Life Support'),
        ('Mobile Intensive Care','Mobile Intensive Care'),
        ('Non-Emergency Transport','Non-Emergency Transport'),
    ]

    parent = models.ForeignKey(ProspectiveClient,on_delete=models.CASCADE,blank=True,null=True)
    level_of_care = models.CharField(max_length=200,choices=LEVEL_OF_CARE)
    code = models.ForeignKey(Code, on_delete=SET_NULL,blank=True,null=True)
    service_description = models.CharField(max_length=1000,blank=True,null=True)
    qty = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    line_total = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.parent.id)


class TotalCallCosting(models.Model):
    parent = models.ForeignKey(ProspectiveClient,on_delete=models.CASCADE,blank=True,null=True)
    total_service_cost = models.PositiveIntegerField(blank=True,null=True)
    discount = models.PositiveIntegerField(blank=True,null=True)
    discount_amount = models.PositiveIntegerField(blank=True,null=True)
    total_quotation_cost = models.PositiveIntegerField(blank=True,null=True)
    special_notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.parent.id)


# Quotation Events and Sport

class EventsProspectiveClient(models.Model):
    doc_version = models.PositiveIntegerField(blank=True,null=True)
    date_of_quote = models.DateField(blank=True,null=True)
    name_poc = models.CharField(max_length=100,blank=True,null=True)
    company_org_name = models.CharField(max_length=100,blank=True,null=True)
    physical_address = models.TextField()
    client_phone_no = models.PositiveIntegerField()
    clinet_email = models.EmailField(blank=True,null=True)
    date_of_expiry = models.DateField()
    quote_prepared_by = models.ForeignKey(QuotePreparedBy, on_delete=SET_NULL,blank=True,null=True)
    

class EventServiceRequest(models.Model):
    service_req = models.CharField(max_length=200,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_req

class EventServiceDetailRiskLevel(models.Model):
    risk_level = models.CharField(max_length=200,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.risk_level

class EventsServiceDetails(models.Model):
    parent = models.ForeignKey(EventsProspectiveClient,on_delete=models.CASCADE,blank=True,null=True)
    service_request = models.ForeignKey(EventServiceRequest,on_delete=SET_NULL,blank=True,null=True)
    risk_lvl = models.ForeignKey(EventServiceDetailRiskLevel, on_delete=SET_NULL,blank=True,null=True)
    evnt_name = models.CharField(max_length=100,blank=True,null=True)
    special_notes = models.BooleanField(default=False)

    def __str__(self):
        return str(self.parent.id)

class EventParticularServiceDescription(models.Model):
    ser_des = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ser_des

class EventSportParticulars(models.Model):
    parent = models.ForeignKey(EventsProspectiveClient,on_delete=models.CASCADE,blank=True,null=True)
    date_of_service = models.DateField()
    service_description = models.ForeignKey(EventParticularServiceDescription,on_delete=SET_NULL,blank=True,null=True)
    loc_address = models.CharField(max_length=500,blank=True,null=True)
    service_start_time = models.TimeField()
    service_end_time = models.TimeField()
    total_service_time = models.CharField(max_length=500,blank=True,null=True)
    price = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.parent.id)








