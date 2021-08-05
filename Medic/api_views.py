from django.http import response
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.generics import ListAPIView
from datetime import datetime, timedelta
from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

today = datetime.today()
week = datetime.today().date() - timedelta(days=7)
month = datetime.today().date() - timedelta(days=30)


class AmbulanceRequestToday(ListAPIView):
    serializer_class = AmbulanceRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = AmbulanceModel.objects.filter(created_on__gte=today.date())
        elif not self.request.user.is_superuser and not self.request.user.is_staff:
            data = AmbulanceModel.objects.filter(user=user_id, created_on__gte=today.date())
        return data


class AmbulanceRequestWeek(ListAPIView):
    serializer_class = AmbulanceRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            print('ambulance')
            data = AmbulanceModel.objects.filter(created_on__gte=week)
        elif not self.request.user.is_superuser and not self.request.user.is_staff:
            data = AmbulanceModel.objects.filter(user=user_id, created_on__gte=week)
        return data


class AmbulanceRequestMonth(ListAPIView):
    serializer_class = AmbulanceRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = AmbulanceModel.objects.filter(created_on__gte=month)
        elif not self.request.user.is_superuser and not self.request.user.is_staff:
            data = AmbulanceModel.objects.filter(user=user_id, created_on__gte=month)
        else:
            data = 'nothing'
        return data


#mobile api's starts here. . .
class OccurrenceReports(generics.ListAPIView):
    serializer_class = OccurrenceSerializer
    def get_queryset(self):
        reports = Occurrence.objects.all()
        if not reports:
            return Response({'reports': 'No reports yet'}, status=status.HTTP_204_NO_CONTENT)
        return reports


class Panic_Noti(generics.ListAPIView):
    serializer_class = PanicNotiSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return PanicNoti.objects.filter(is_seen = False).order_by('-id')

        

class AmbulanceRequest(generics.CreateAPIView):
    serializer_class = AmbulanceRequestSerializer
    permission_classes = [IsAuthenticated,]
    def post(self, request,  *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(commit = False)
            data.user = user
            data.save()
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
