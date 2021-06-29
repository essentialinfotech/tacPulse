from __future__ import division
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .serializer import *
from django.views import View
from django.views.generic import UpdateView, DetailView
from rest_framework.generics import ListAPIView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def audit_form(request):
    return render(request, 'medic/audit_form.html')


def audit_report(request):
    return render(request, 'medic/audit_report.html')


def assetment_form(request):
    return render(request, 'medic/assesment_form.html')


def inspection_form(request):
    return render(request, 'medic/inspection_form.html')


def inspaction_report(request):
    return render(request, 'medic/inspaction_report.html')


def case_note_form(request):
    return render(request, 'medic/case_note_form.html')


def case_reports(request):
    return render(request, 'medic/case_reports.html')


def stock_req_form(request):
    return render(request, 'medic/stock_req_form.html')


def stock_req_reports(request):
    return render(request, 'medic/stock_req_reports.html')


def tools_form(request):
    return render(request, 'medic/tools_form.html')


def occurrence_form(request):
    return render(request, 'medic/occurrence_form.html')


def occurrence_report(request):
    return render(request, 'medic/occurrence_report.html')


def dragable_form(request):
    return render(request, 'medic/dragable_form.html')


def tools_report(request):
    return render(request, 'medic/tools_report.html')


def schedule_report(request):
    return render(request, 'medic/schedule_report.html')


@csrf_exempt
def rating(request):
    if request.method == 'POST':
        star_value = request.POST
        rating = Rating.objects.all()
        value = 0
        for k, v in star_value.items():
            value = v
        if not rating:
            first_avg = int(value) / 1
            Rating.objects.create(rated_value=value, all_time_rated_value_store=value,
                                  count=1, avg_rating=first_avg)
        elif rating:
            for i in rating:
                i.rated_value = int(value)
                i.count = i.count + 1
                count = i.count
                i.all_time_rated_value_store = i.all_time_rated_value_store + i.rated_value
                view_all_time_rated_value_store = i.all_time_rated_value_store
                avg_rating = view_all_time_rated_value_store / count
                i.avg_rating = format(avg_rating, ".1f")
                average = i.avg_rating
                i.save()
                Rating.objects.update(rated_value=value, all_time_rated_value_store=view_all_time_rated_value_store,
                                      count=count, avg_rating=average)
                print(average)
                print(star_value)
    return render(request, 'medic/rate.html')


class AmbulanceRequest(View):

    def get(self, request):
        return render(request, 'medic/ambulance_request.html')

    def post(self, request):
        form = AmbulanceModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ambulance_request_report')
        return render(request, 'medic/ambulance_request.html')


class AmbulanceRequestReport(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'medic/ambulance_request_report.html')


class AmbulanceRequestDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(AmbulanceModel, pk=pk)
        context = {
            'data': data
        }
        return render(request, 'medic/ambulancereq_detail.html', context)


class AmbulanceTrackLocation(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = AmbulanceModel.objects.get(pk=pk)
        context = {
            'data': data
        }
        return render(request, 'medic/trac_req.html', context)


def dispatch_list(request):
    return render(request, 'medic/dispatch_list.html')


def hospital_transfer(request):
    return render(request, 'medic/hospita_transfer.html')


def hospital_transfer_report(request):
    return render(request, 'medic/hospita_transfer_report.html')


def panic_system(request):
    panic = 'Give a panic request'
    if request.method == 'POST':
        reason = request.POST.get('reason')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        my_panic = Panic.objects.create(panic_sender_id=request.user.id, reason=reason, lat=lat, lng=lng)
        return redirect('check_panic_requests_location', id=my_panic.id)
    return render(request, 'medic/panic.html', {'panic': panic})


def del_panic(request, id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(Panic, id=id)
    obj.delete()
    return HttpResponseRedirect(url)


def check_panic_requests(request):
    panic_requests = Panic.objects.all().order_by('-id')
    context = {
        'panic_requests': panic_requests,
    }
    return render(request, 'medic/panic_requests.html', context)


def check_panic_requests_location(request, id):
    context = {}
    if request.user.is_authenticated:
        try:
            panic = Panic.objects.get(id=id)
            context = {
                'name': panic.panic_sender.username,
                'reason': panic.reason,
                'lat': panic.lat,
                'lng': panic.lng,
                'id': id,
            }
            print(context)
        except:
            return HttpResponse('This panic data has been deleted/not found')
    else:
        return HttpResponse('Please Login First')
    return render(request, 'medic/panic_location_check_admin.html', context)


def task_transfer_req(request):
    return render(request, 'medic/task_transfer_req.html')


def get_route(request):
    return render(request, 'medic/route.html')
