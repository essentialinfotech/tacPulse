from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializer import *
from rest_framework import response
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.contrib.auth import authenticate, login, logout
from django.http import Http404


class DispatchesLocationAPI(ListAPIView):
    serializer_class = DispatchSerializer

    def get_queryset(self):
        data = User.objects.filter(is_staff = True, is_superuser=False)
        return data


#mobile api views  starts from here. . .
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class Profile(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        user = User.objects.filter(id = self.request.user.id)
        return user


class UpdateProfile(APIView):
    def put(self, request, format=None):
        user = self.request.user
        serializer = UpdateProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DispatchList(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        user = User.objects.filter(is_staff = True)
        return user


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.user.set_password(serializer.data.get("new_password"))
            self.user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'old password': [serializer.data.get("old_password")],
                'new password': [serializer.data.get("new_password")],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




