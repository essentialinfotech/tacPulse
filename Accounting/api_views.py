from .models import *
from .serializer import *
from rest_framework.generics import ListAPIView
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

today = datetime.today()
week = datetime.today().date() - timedelta(days=7)
month = datetime.today().date() - timedelta(days=30)


class ScheduleToday(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = ScheduleModel.objects.filter(created_on__gte=today.date())
        elif self.request.user.is_user:
            data = ScheduleModel.objects.filter(user=user_id, created_on__gte=today.date())
        else:
            data = {'data': 'nothing'}
        return data


class ScheduleWeek(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = ScheduleModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_user:
            data = ScheduleModel.objects.filter(user=user_id, created_on__gte=week)
        else:
            data = {'data': 'nothing'}
        return data


class ScheduleMonth(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = ScheduleModel.objects.filter(created_on__gte=month)
        elif self.request.user.is_user:
            data = ScheduleModel.objects.filter(user=user_id, created_on__gte=month)
        else:
            data = {'data': 'nothing'}
        return data


class TaskToday(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskModel.objects.filter(created_on__gte=today.date())
        elif self.request.user.is_staff:
            data = TaskModel.objects.filter(user=user_id, created_on__gte=today.date())
        else:
            data = {'data': 'nothing'}
        return data


class TaskWeek(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_user:
            data = TaskModel.objects.filter(user=user_id, created_on__gte=week)
        else:
            data = {'data': 'nothing'}
        return data


class TaskMonth(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskModel.objects.filter(created_on__gte=month)
        elif self.request.user.is_user:
            data = TaskModel.objects.filter(user=user_id, created_on__gte=month)
        else:
            data = {'data': 'nothing'}
        return data


class TransferredToday(ListAPIView):
    serializer_class = TransferredSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskTransferModel.objects.filter(created_on__gte=today.date())
        elif self.request.user.is_staff:
            data = TaskTransferModel.objects.filter(Q(dispatch=user_id) or Q(transfer_to=user_id), created_on__gte=month).distinct('id')
        else:
            data = {'data': 'nothing'}
        return data


class TransferredWeek(ListAPIView):
    serializer_class = TransferredSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskTransferModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_user:
            data = TaskTransferModel.objects.filter(Q(dispatch=user_id) or Q(transfer_to=user_id), created_on__gte=month).distinct('id')
        else:
            data = {'data': 'nothing'}
        return data


class TransferredMonth(ListAPIView):
    serializer_class = TransferredSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskTransferModel.objects.filter(created_on__gte=month)
        elif self.request.user.is_user:
            data = TaskTransferModel.objects.filter(Q(dispatch=user_id) or Q(transfer_to=user_id), created_on__gte=month).distinct('id')
        else:
            data = {'data': 'nothing'}
        return data


class StockRequestToday(ListAPIView):
    serializer_class = StockRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = StockRequestModel.objects.filter(created_on__gte=today.date())
        else:
            data = {'data': 'nothing'}
        return data


class StockRequestWeek(ListAPIView):
    serializer_class = StockRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = StockRequestModel.objects.filter(created_on__gte=week)
        else:
            data = {'data': 'nothing'}
        return data


class StockRequestMonth(ListAPIView):
    serializer_class = StockRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = StockRequestModel.objects.filter(created_on__gte=month)
        else:
            data = {'data': 'nothing'}
        return data


class StockRequested(ListAPIView):
    serializer_class = StockRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = StockRequestModel.objects.filter(requested=True)
        else:
            data = {'data': 'nothing'}
        return data


class StockRequestCanceled(ListAPIView):
    serializer_class = StockRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = StockRequestModel.objects.filter(cancel=True)
        else:
            data = {'data': 'nothing'}
        return data



