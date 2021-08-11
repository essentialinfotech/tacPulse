from rest_framework import fields, serializers
from .models import *
from Accounts.models import User


class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'latitude', 'longitude']



#mobile app api serializers starts from here . . .
# foreignkey relation through serializer
class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)




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


class AssessmentCreateSerializer(serializers.ModelSerializer):
    # to_user = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)
    class Meta:
        model = Assesment
        fields = '__all__'
        depth = 1


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','receiver','message']
        depth = 1


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','receiver','message','sent']
        depth = 1