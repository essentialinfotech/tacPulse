from django.db.models.base import Model
from rest_framework import serializers
from .models import *
from Accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panic
        fields = '__all__'
        depth = 1


class AmbulanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceModel
        fields = '__all__'


class PanicNotiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanicNoti
        fields = '__all__'
        depth = 2
