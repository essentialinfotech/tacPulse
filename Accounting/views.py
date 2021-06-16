from django.shortcuts import render, redirect, get_object_or_404
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


def shcedule_trip(request):
    return render(request, 'Accounting/shcedule_trip.html')


def trip_schedules(request):
    return render(request, 'Accounting/trip_schedules.html')


def add_paystub(request):
    return render(request, 'Accounting/add_paystub.html')


def paystub_report(request):
    return render(request, 'Accounting/paystub_report.html')
