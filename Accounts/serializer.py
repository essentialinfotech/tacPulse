from rest_framework import serializers
from .models import *


class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'latitude', 'longitude']