from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

# Create your views here.
def audit_form(request):
    return render(request,'medic/audit_form.html')


def assetment_form(request):
    return render(request,'medic/assesment_form.html')


def inspection_form(request):
    return render(request,'medic/inspection_form.html')


def case_note_form(request):
    return render(request,'medic/case_note_form.html')


def stock_req_form(request):
    return render(request,'medic/stock_req_form.html')


def tools_form(request):
    return render(request,'medic/tools_form.html')


def occurrence_form(request):
    return render(request,'medic/occurrence_form.html')


def dragable_form(request):
    return render(request,'medic/dragable_form.html')


def rating(request):
    return render(request,'medic/rate.html')


def dispatch_list(request):
    return render(request,'medic/dispatch_list.html')


def panic_system(request):
    url = request.META.get('HTTP_REFERER')
    panic = 'Give a panic request'
    if request.method == 'POST':
        messages.success(request,'Panic request sent')
        return HttpResponseRedirect(url)
    return render(request,'medic/panic.html',{'panic': panic})
        

