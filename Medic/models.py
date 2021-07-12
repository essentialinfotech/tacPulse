from typing import Set
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.deletion import SET_NULL
from Accounts.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from Accounts.models import User
# Create your models here.


# emmergency contact template e boshano baki
class Panic(models.Model):
    emergency_contact = models.CharField(max_length=40, blank=True, null=True)
    panic_sender = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, blank=False, null=False)
    place = models.CharField(max_length=2000, blank=True, null=True)
    lat = models.CharField(max_length=200, blank=True, null=True)
    lng = models.CharField(max_length=200, blank=True, null=True)
    assigned = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.panic_sender.first_name


class Rating(models.Model):
    rated_value = models.IntegerField(blank=True, null=True, default=0)
    all_time_rated_value_store = models.IntegerField(
        blank=True, null=True, default=0)
    count = models.IntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0.0)


class Feedback(models.Model):
    author = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    feedback_text = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def name(self):
        user = self.author.first_name
        if user != '':
            return user
        else:
            user = self.author.username
            return user


class Occurrence(models.Model):
    OCCURRENCE_TYPE = [
        ('CORPORATE', 'CORPORATE'),
        ('CUSTOMER', 'CUSTOMER'),
    ]
    occurrence_giver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    related_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True, related_name='for_user')
    occurrence_id = models.CharField(max_length=30000,blank=True, null=True)
    occurrence_type = models.CharField(max_length = 20, choices = OCCURRENCE_TYPE)
    occurrence_detail = models.CharField(max_length=600)
    image = models.ImageField(
        upload_to='media/Occurrence', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def imagesURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return str(self.occurrence_id)


class AmbulanceModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, blank=False, null=False)
    contact = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(
        max_length=100, blank=False, null=False, default="")
    reason = models.TextField(max_length=250, blank=False, null=False)
    location = models.CharField(max_length=250, blank=False, null=False)
    latitude = models.CharField(
        max_length=100, blank=False, null=False, default='')
    longitude = models.CharField(
        max_length=100, blank=False, null=False, default='')
    assigned = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location


class PanicNoti(models.Model):
    panic = models.ForeignKey(
        Panic, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=100, default='has sent a panic request')
    created = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return self.panic.panic_sender.first_name


class PropertyTools(models.Model):
    CONDITION = [
        ('NEW', 'NEW'),
        ('USED', 'USED'),
    ]
    STATUS = [
        ('PAID', 'PAID'),
        ('DUE', 'DUE'),
    ]
    TYPE = [
        ('FURNITURE', 'FURNITURE'),
        ('HARDWARE', 'HARDWARE'),
        ('ELECTRICAL', 'ELECTRICAL'),
        ('SOFTWARE', 'SOFTWARE'),
        ('AMBULANCE', 'AMBULANCE'),
        ('OXYGEN CYLINDER', 'OXYGEN CYLINDER'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    to_user = models.CharField(max_length=80, blank=True, null=True)
    to_user_mobile = models.CharField(max_length=80, blank=True, null=True)
    property_type = models.CharField(
        max_length=30, blank=True, null=True, choices=TYPE)
    equipement_name = models.CharField(max_length=40, blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=300, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    condition = models.CharField(
        max_length=30, blank=True, null=True, choices=CONDITION)
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=STATUS)
    invoice_id = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    vat = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.invoice_id


class FAQ(models.Model):
    author = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    img = models.ImageField(upload_to='FAQ', blank=True, null=True)
    ques = models.CharField(max_length=500, blank=True, null=True)
    ans = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ques


class CaseNote(models.Model):
    creator = models.ForeignKey(User,on_delete=SET_NULL,blank=True, null=True)
    case_panic = models.ForeignKey(Panic,on_delete=models.CASCADE,blank=True, null=True)
    case_no = models.TextField(blank=True, null=True)
    case_note = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.case_no)


@receiver(post_save, sender=Panic)
def create_panic_noti(sender, instance=None, created=False, **kwargs):
    if created:
        PanicNoti.objects.create(panic=instance)


class HospitalTransferModel(models.Model):
    transfer_type = [
        ('Emergency', 'Emergency'),
        ('Normally', 'Normally')
    ]

    priority_type = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transfer_speed = models.CharField(max_length=100, choices=transfer_type, blank=False, null=False, default='Emergency')
    reason = models.CharField(max_length=100, blank=False, null=False)
    priority = models.CharField(max_length=100, choices=priority_type, blank=True, null=True, default='Low')
    current_hos = models.CharField(max_length=200, blank=False, null=False)
    current_add = models.CharField(max_length=200, blank=False, null=False)
    target_hos = models.CharField(max_length=200, blank=False, null=False)
    target_add = models.CharField(max_length=200, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    assigned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.target_hos
