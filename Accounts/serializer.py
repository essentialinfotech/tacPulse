from rest_framework import fields, serializers
from .models import *


class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'latitude', 'longitude']



#mobile app api serializers starts from here . . .
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'password', 'password1',
                    'username','contact','address', 'is_staff','profile_pic')
        extra_kwargs = {'password': {'write_only': True},
                        'password1': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'],
            first_name=validated_data['first_name'], last_name=validated_data['last_name'],
            contact = validated_data['contact'],address = validated_data['address'],
            is_staff = validated_data['is_staff'],profile_pic = validated_data['profile_pic'],)
        user.set_password(validated_data['password1'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=100)

    class Meta:
        fields = ['username', 'password']