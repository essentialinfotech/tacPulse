from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='media/profile_pictures')
    contact = models.CharField(max_length=30, blank=False, null=False, unique = True)
    address = models.CharField(max_length=150, blank=False, null=False)
    latitude = models.CharField(
        max_length=30, blank=False, null=False, default='')
    longitude = models.CharField(
        max_length=30, blank=False, null=False, default='')
    has_membership = models.BooleanField(default=False)

    def __str__(self):
        return self.username


