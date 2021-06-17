from django.shortcuts import render
from .models import *

# Create your views here.


def audit_form(request):
    return render(request, 'medic/audit_form.html')


def assetment_form(request):
    return render(request, 'medic/assesment_form.html')


def inspection_form(request):
    return render(request, 'medic/inspection_form.html')


def case_note_form(request):
    return render(request, 'medic/case_note_form.html')


def stock_req_form(request):
    return render(request, 'medic/stock_req_form.html')


def tools_form(request):
    return render(request, 'medic/tools_form.html')


def rating(request):
    return render(request, 'medic/rate.html')


def ambulance_request(request):
    return render(request, 'medic/ambulance_request.html')
    return render(request, 'medic/rate.html')


def dispatch_list(request):
    return render(request, 'medic/dispatch_list.html')
