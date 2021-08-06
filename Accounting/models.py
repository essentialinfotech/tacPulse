from django import dispatch
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.expressions import F
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
    attachment = models.FileField('attachment/', blank=True)
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
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
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
    amount = models.CharField(max_length=100, blank=True, null=True, default=0)
    duration = models.CharField(max_length=100, blank=True, null=True)
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








