from .models import *
from .serializer import *
from rest_framework.generics import ListAPIView
from datetime import datetime, timedelta

today = datetime.today()
week = datetime.today().date() - timedelta(days=7)
month = datetime.today().date() - timedelta(days=30)


class AmbulanceRequestToday(ListAPIView):
    serializer_class = AmbulanceRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = AmbulanceModel.objects.filter(created_on__gte=today.date())
        elif self.request.user.is_user:
            data = AmbulanceModel.objects.filter(user=user_id, created_on__gte=today.date())
        return data


class AmbulanceRequestWeek(ListAPIView):
    serializer_class = AmbulanceRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = AmbulanceModel.objects.filter(created_on__gte=week)
        elif self.request.user.is_user:
            data = AmbulanceModel.objects.filter(user=user_id, created_on__gte=week)
        return data


class AmbulanceRequestMonth(ListAPIView):
    serializer_class = AmbulanceRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            data = AmbulanceModel.objects.filter(created_on__gte=month)
        elif self.request.user.is_user:
            data = AmbulanceModel.objects.filter(user=user_id, created_on__gte=month)
        else:
            data = 'nothing'
        return data

