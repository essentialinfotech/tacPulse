from django.shortcuts import get_object_or_404, render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

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
    return render(request,'medic/occurrence_form.html')


def occurrence_report(request):
    return render(request,'medic/occurrence_report.html')


def dragable_form(request):
    return render(request,'medic/dragable_form.html')


def rating(request):
    return render(request, 'medic/rate.html')


def ambulance_request(request):
    return render(request, 'medic/ambulance_request.html')


def ambulance_request_report(request):
    return render(request, 'medic/ambulance_request_report.html')


def dispatch_list(request):
    return render(request, 'medic/dispatch_list.html')


def hospital_transfer(request):
    return render(request, 'medic/hospita_transfer.html')


def hospital_transfer_report(request):
    return render(request, 'medic/hospita_transfer_report.html')



def panic_system(request):
    url = request.META.get('HTTP_REFERER')
    panic = 'Give a panic request'
    if request.method == 'POST':
        reason = request.POST.get('reason')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        Panic.objects.create(panic_sender_id = request.user.id, reason = reason , lat = lat, lng = lng)
        return HttpResponseRedirect(url)
    return render(request,'medic/panic.html',{'panic': panic})


def del_panic(request,id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(Panic, id = id)
    obj.delete()
    return HttpResponseRedirect(url)


def check_panic_requests(request):
    panic_requests = Panic.objects.all().order_by('-id')
    context = {
        'panic_requests': panic_requests,
        }
    return render(request,'medic/panic_requests.html',context)


def check_panic_requests_location(request,id):
    panic = Panic.objects.get(panic_sender_id = id)
    context = {
        'reason': panic.reason,
        'lat': panic.lat,
        'lng': panic.lng,
        'id': id,
    }
    print(context)
    return render(request,'medic/panic_location_check_admin.html', context)


def task_transfer_req(request):
    return render(request, 'medic/task_transfer_req.html')


def get_route(request):
    return render(request, 'medic/route.html')
