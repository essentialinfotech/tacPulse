from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .serializer import *
from rest_framework.views import APIView
from django.contrib import messages
from Accounts.decorators import user_passes_test,has_perm_admin,\
                                has_perm_admin_dispatch,has_perm_user,\
                                has_perm_dispatch,REDIRECT_FIELD_NAME
# Create your views here.


def add_member(request):
    return redirect('register')


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


def packages(request):
    packages = Package.objects.all()
    context = {
        'packages': packages,
    }
    return render(request, 'Accounting/packages.html',context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def add_package(request):
    form = PackageForm()
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Package Created')
            return redirect('packages')
    context = {
        'form': form,
    }
    return render(request,'Accounting/add_package.html',context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def edit_package(request,id):
    data = Package.objects.get(id = id)
    form = PackageForm(instance=data)
    if request.method == 'POST':
        form = PackageForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Package Edited')
            return redirect('packages')
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'Accounting/edit_package.html',context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def del_package(request,id):
    obj = get_object_or_404(Package, id=id)
    obj.delete()
    messages.success(request,'Package deleted')
    return redirect('packages')
