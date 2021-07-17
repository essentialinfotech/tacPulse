from django import dispatch
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from Accounts.models import User
from Medic.models import *
from Accounts.models import *

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
    pass


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
