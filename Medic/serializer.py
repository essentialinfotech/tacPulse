from rest_framework import serializers
from .models import *


class AmbulanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceModel
        fields = '__all__'
