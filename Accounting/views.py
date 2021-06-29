from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .serializer import *
from rest_framework.views import APIView
# Create your views here.


def add_member(request):
    return redirect('register')


def add_package(request):
    if request.method == 'POST':
        return redirect('packages')
    return render(request, 'Accounting/add_package.html')


def packages(request):
    return render(request, 'Accounting/packages.html')


def getmembership(request):
    return render(request, 'Accounting/get_membership.html')


def members(request):
    return render(request, 'Accounting/members.html')


class ScheduleTrip(View):

    def get(self, request):
        return render(request, 'Accounting/shcedule_trip.html')

    def post(self, request):
        form = ScheduleModelForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('trip_schedules')
        return render(request, 'Accounting/shcedule_trip.html')


class TripSchedules(View):
    def get(self, request):
        data = ScheduleModel.objects.all()
        # if request.user.is_user:
        #     data = ScheduleModel.objects.filter
        context = {
            'data': data,
        }
        return render(request, 'Accounting/trip_schedules.html', context)

# class TodaySchedule(APIView):
#     def get(self, request):


def add_paystub(request):
    return render(request, 'Accounting/add_paystub.html')


def paystub_report(request):
    return render(request, 'Accounting/paystub_report.html')
