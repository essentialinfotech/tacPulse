from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = False, null= False, unique = True)
    email = models.EmailField(unique = True, blank = True, null = True)
    profile_pic = models.ImageField(upload_to = 'media/profile_pictures')
    contact = models.CharField(max_length = 30, blank = False, null = False)
    address = models.CharField(max_length = 150, blank = False, null = False)
    is_user = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    has_membership = models.BooleanField(default = False)

    def __str__(self):
        return self.username


