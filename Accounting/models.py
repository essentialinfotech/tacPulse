from django import dispatch
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from Accounts.models import User
from Medic.models import AmbulanceModel

# Create your models here.


class PaystubModel(models.Model):
    dispatch = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, blank=False, null=False)
    file = models.FileField(upload_to='paystub/')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dispatch.first_name + ' ' + self.dispatch.last_name


class MembershipModel(models.Model):
    pass


class TaskModel(models.Model):
    dispatch = models.ForeignKey(User, on_delete=models.CASCADE)
    task_description = models.CharField(
        max_length=100, blank=False, null=False, default='')
    ambulance_req = models.ForeignKey(AmbulanceModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return self.dispatch.first_name + ' ' + self.dispatch.last_name


class StockRequestModel(models.Model):
    receiver = models.CharField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    message_body = models.CharField(max_length=1000, blank=False, null=False)
    attachment = models.FileField('attachment/', blank=True)

    def __str__(self):
        return self.subject


class ScheduleModel(models.Model):
    status_type = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
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
        choices=status_type, max_length=100, default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)



