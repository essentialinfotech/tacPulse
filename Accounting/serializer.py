from django.db.models import fields
from rest_framework import serializers
from .models import *


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleModel
        fields = '__all__'
        depth = 1


class TransferredSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTransferModel
        fields = '__all__'
        depth = 4


class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequestModel
        fields = '__all__'


#mobile serializers starts here . . 
class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionModel
        fields = '__all__'
        depth = 1

class PaystubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaystubModel
        fields = '__all__'
        depth = 1

class AuditCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audit
        fields = '__all__'
        depth = 1


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'
        depth = 4