from django.shortcuts import render
from .models import *

# Create your views here.
def audit_form(request):
    return render(request,'medic/audit_form.html')


def assetment_form(request):
    return render(request,'medic/assesment_form.html')


def rating(request):
    return render(request,'medic/rate.html')


def dispatch_list(request):
    return render(request,'medic/dispatch_list.html')

