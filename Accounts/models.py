from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(blank=True,null=True,unique=True)
    profile_pic = models.ImageField(upload_to='media/profile_pictures')
    contact = models.CharField(
        max_length=30, blank=False, null=False, unique=True)
    address = models.CharField(max_length=150, blank=False, null=False)
    quote = models.CharField(max_length=250, blank=True,
                             null=True, default='Bio Here. . .')
    latitude = models.CharField(
        max_length=30, blank=False, null=False, default='')
    longitude = models.CharField(
        max_length=30, blank=False, null=False, default='')
    has_membership = models.BooleanField(default=False)

    def __str__(self):
        user = self.first_name
        if user !='':
            return user
        else:
            user = self.username
            return user

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url


