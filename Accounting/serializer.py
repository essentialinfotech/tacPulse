from django.db.models import fields
from rest_framework import serializers
from .models import *


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


class ScheduleSerializer(serializers.ModelSerializer):
    # start_datetime = serializers.DateTimeField(format=None,input_formats=['%Y-%m-%dT%H:%M:%SZ',])
    # end_datetime = serializers.DateTimeField(format=None,input_formats=['%Y-%m-%dT%H:%M:%SZ',])
    class Meta:
        model = ScheduleModel
        fields = '__all__'
        depth = 1