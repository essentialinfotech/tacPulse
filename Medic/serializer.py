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
        depth = 2


class AmbulanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceRequestModel
        fields = '__all__'
        depth = 1


class PanicNotiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanicNoti
        fields = '__all__'
        depth = 2


class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = '__all__'
        depth = 1


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        depth = 1


class HospitalTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalTransferModel
        fields = '__all__'
        depth = 1


# dispatch incident
class AsignedParamedicsWholeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedParamedicsAfterDispatchIncidentCrewAndVehicle
        fields = '__all__'
        depth = 4

class ParamedicsPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParamedicsPhases
        fields = '__all__'
        depth = 5
