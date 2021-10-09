from Accounting import serializer
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
from django.db.models import Sum, Q,query

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
    def post(self, request, format=None):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id = user.id)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AmbulanceRequestList(generics.ListAPIView):
    serializer_class = AmbulanceRequestSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        if self.request.user.is_superuser:
            requests = AmbulanceModel.objects.all()
            serializer = self.get_serializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('You do not have permission to view this content', status=status.HTTP_400_BAD_REQUEST)


class PanicList(generics.ListAPIView):
    serializer_class = PanicSerializer
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        if request.user.is_staff:
            panics = Panic.objects.all().order_by('-id')
            serializer = PanicSerializer(panics, many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)


class PanicCreate(generics.CreateAPIView):
    serializer_class = PanicSerializer
    permission_classes = [IsAuthenticated,]
    def post(self,request,formate=None):
        serializer = PanicSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(panic_sender = request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FAQLIST(generics.ListAPIView):
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        faqs = FAQ.objects.all().order_by('-id')
        serializer = FAQSerializer(faqs, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class HospitalTransferAPI(generics.CreateAPIView):
    serializer_class = HospitalTransferSerializer
    permission_classes = [IsAuthenticated,]
    def post(self,request,formate=None):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(requested_by = request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class HospitalTransferList(generics.ListAPIView):
    serializer_class = HospitalTransferSerializer
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        transfers = HospitalTransferModel.objects.filter(requested_by = self.request.user).order_by('-id')
        serializer = HospitalTransferSerializer(transfers, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

