from django.db import models
from django.db.models.aggregates import Count
from Accounts.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Panic(models.Model):
    panic_sender = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    reason = models.CharField(max_length = 200, blank = False, null = False)
    lat = models.CharField(max_length=200,blank=True,null=True)
    lng = models.CharField(max_length=200,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.panic_sender.username

class Rating(models.Model):
    feedback_giver = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    feedback_text = models.CharField(max_length = 200, blank = True, null = True )
    rated_value = models.IntegerField(blank = True, null = True , default = 0)
    all_time_rated_value_store = models.IntegerField(blank = True, null = True , default = 0)
    count = models.IntegerField(blank = True, null = True, default = 0)
    avg_rating = models.FloatField(blank = True, null = True, default = 0.0)


@receiver(post_save, sender=User)
def create_ratings(sender, instance, created, **kwargs):
    if created:
        if instance.is_user :
            Rating.objects.create(rated_user=instance)


