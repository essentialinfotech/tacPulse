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
    renew_membership = models.BooleanField(default=False)

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


class Assesment(models.Model):
    RATE = [
        ('Good','Good'),
        ('Satisfactory','Satisfactory'),
        ('Excellent','Excellent'),
        ('Poor','Poor'),
        ('Very Poor','Very Poor'),
    ]

    by_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_that_will_be_assisted')
    msg = models.CharField(max_length=100,blank=True, null=True)
    rate = models.CharField(max_length=30,choices=RATE)
    warning = models.BooleanField(default=False,help_text="want to warn?")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rate


class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user',blank=True, null=True)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user',blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='messagefiles',blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.first_name


