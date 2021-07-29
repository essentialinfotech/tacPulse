from django.db.models import fields
from rest_framework import serializers
from .models import *


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleModel
        fields = '__all__'
        depth = 1


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'
        depth = 4


class TransferredSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTransferModel
        fields = '__all__'
        depth = 4


class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequestModel
        fields = '__all__'
