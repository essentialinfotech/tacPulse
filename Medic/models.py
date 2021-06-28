from django.db import models
from django.db.models.aggregates import Count
from Accounts.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Panic(models.Model):
    panic_sender = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, blank=False, null=False)
    lat = models.CharField(max_length=200, blank=True, null=True)
    lng = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.panic_sender.username


class Rating(models.Model):
    feedback_text = models.CharField(max_length=200, blank=True, null=True)
    rated_value = models.IntegerField(blank=True, null=True, default=0)
    all_time_rated_value_store = models.IntegerField(
        blank=True, null=True, default=0)
    count = models.IntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0.0)


class AmbulanceModel(models.Model):
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
