from django.db import models
from Accounts.models import *
# Create your models here.

class Panic(models.Model):
    panic_sender = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    lat = models.CharField(max_length=200,blank=True,null=True)
    lng = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.panic_sender.username
