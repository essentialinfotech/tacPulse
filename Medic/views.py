from django.shortcuts import render
from .models import *

# Create your views here.


def audit_form(request):
    return render(request, 'medic/audit_form.html')


def assetment_form(request):
    return render(request, 'medic/assesment_form.html')


def rating(request):
    return render(request, 'medic/rate.html')


def ambulance_request(request):
    return render(request, 'medic/ambulance_request.html')
