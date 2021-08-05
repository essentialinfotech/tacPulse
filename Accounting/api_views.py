from .models import *
from .serializer import *
from rest_framework.generics import ListAPIView
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


today = datetime.today()
week = datetime.today().date() - timedelta(days=7)
month = datetime.today().date() - timedelta(days=30)


class ScheduleToday(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = ScheduleModel.objects.filter(created_on__gte=today.date())
        elif self.request.user.is_staff:
            data = ScheduleModel.objects.filter(
                user=user_id, created_on__gte=today.date())
        else:
            data = {'data': 'nothing'}
        return data


class ScheduleWeek(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = ScheduleModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_staff:
            data = ScheduleModel.objects.filter(
                user=user_id, created_on__gte=week)
        else:
            data = {'data': 'nothing'}
        return data


class ScheduleMonth(ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = ScheduleModel.objects.filter(created_on__gte=month)
        elif self.request.user.is_staff:
            data = ScheduleModel.objects.filter(
                user=user_id, created_on__gte=month)
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
            data = TaskModel.objects.filter(
                user=user_id, created_on__gte=today.date())
        else:
            data = {'data': 'nothing'}
        return data


class TaskWeek(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_staff:
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
        elif self.request.user.is_staff:
            data = TaskModel.objects.filter(
                user=user_id, created_on__gte=month)
        else:
            data = {'data': 'nothing'}
        return data


class TransferredToday(ListAPIView):
    serializer_class = TransferredSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskTransferModel.objects.filter(
                created_on__gte=today.date())
        elif self.request.user.is_staff:
            data = TaskTransferModel.objects.filter(Q(transferred_by_id=user_id) | Q(
                transfer_to_id=user_id), created_on__gte=month)
        else:
            data = {'data': 'nothing'}
        return data


class TransferredWeek(ListAPIView):
    serializer_class = TransferredSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskTransferModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_staff:
            data = TaskTransferModel.objects.filter(Q(transferred_by_id=user_id) | Q(
                transfer_to_id=user_id), created_on__gte=month)

        else:
            data = {'data': 'nothing'}
        return data


class TransferredMonth(ListAPIView):
    serializer_class = TransferredSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = TaskTransferModel.objects.filter(created_on__gte=month)
        elif self.request.user.is_staff:
            data = TaskTransferModel.objects.filter(Q(transferred_by_id=user_id) | Q(
                transfer_to_id=user_id), created_on__gte=month)
        else:
            data = {'data': 'nothing'}
        return data


class StockRequestToday(ListAPIView):
    serializer_class = StockRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = StockRequestModel.objects.filter(
                created_on__gte=today.date())
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


@csrf_exempt
def api_schedule_status_update(request, pk):
    if request.method == 'POST':
        data = get_object_or_404(ScheduleModel, pk=pk)
        val = request.POST.get('val')
        if val == 'Pending':
            data.status = 'Pending'
        elif val == 'Approved':
            data.status = 'Approved'
        elif val == 'Declined':
            data.status = 'Declined'
            task = get_object_or_404(TaskModel, scheduled_task=pk)
            task.delete()
        else:
            data.status = 'Completed'
        data.save()
        return HttpResponse('Ok')



#mobile api's starts here. . .
class InspectionCheckLists(generics.ListAPIView):
    serializer_class = InspectionSerializer
    def get_queryset(self):
        reports = InspectionModel.objects.all()
        return reports


class PayStubReports(generics.ListAPIView):
    serializer_class = PaystubSerializer
    def get_queryset(self):
        reports = PaystubModel.objects.filter(created_on__month = datetime.now().month,
                                            created_on__year = datetime.now().year)
        return reports

class AuditCreateApi(generics.CreateAPIView):
    serializer_class = AuditCreateSerializer
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        if self.request.user.is_superuser:
            auditor = request.user
            serializer = self.get_serializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(auditor = auditor )
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response('Not an admin', status=status.HTTP_400_BAD_REQUEST)
