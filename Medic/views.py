from __future__ import division
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import success
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .forms import *
import datetime
from .serializer import *
from django.views import View
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.views.generic import UpdateView, DetailView
from rest_framework.generics import ListAPIView
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from Accounts.decorators import \
                                 user_passes_test,REDIRECT_FIELD_NAME,\
                                INACTIVE_REDIRECT_FIELD_NAME, \
                                has_perm_dispatch,has_perm_user,has_perm_admin,\
                                has_perm_admin_dispatch


# global
this_month = datetime.datetime.now().month
this_day = datetime.datetime.today()
this_year = datetime.datetime.now().year

def invoice_no(type):
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    invoice_no = '#'+str(type) +str(round(timestamp))
    return invoice_no

def unique_id(id):
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    unique_id = '#'+str(round(timestamp))+str(-(id))
    return unique_id


# Create your views here.
def audit_form(request):
    return render(request, 'medic/audit_form.html')


def audit_report(request):
    return render(request, 'medic/audit_report.html')


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


def occurrence_form(request):
    form = OccurrenceForm()
    if request.method == 'POST':
        form = OccurrenceForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.occurrence_giver = request.user
            instance.occurrence_id = unique_id(id = request.user.id)
            instance.save()
            messages.success(request,'Occurrence Created')
            return redirect('occurrence_report')
    context = {
        'form': form,
    }
    return render(request,'medic/occurrence_form.html', context)


def occurrence_report(request):
    monthly_occurences = Occurrence.objects.filter(created__month = this_month, \
                                                    created__year = this_year)

    daily_occurences = Occurrence.objects.filter(created__date = this_day)

    weekly_occurences = Occurrence.objects.filter(created__iso_week_day__gte = 1,\
                                                     created__month = this_month,\
                                                    created__year = this_year)

    context = {
        'monthly_occurences': monthly_occurences,
        'daily_occurences': daily_occurences,
        'weekly_occurences': weekly_occurences,
    }
    return render(request,'medic/occurrence_report.html', context)


def common_delete(request,id):
    url = request.META.get('HTTP_REFERER')
    try:
        occurrence = get_object_or_404(Occurrence,id=id)
        if occurrence:
            occurrence.delete()
            return HttpResponseRedirect(url)
        else:
            return HttpResponse('Not Found')
    except:
        return HttpResponseRedirect(url)

def edit_occurrence(request,id):
    data = Occurrence.objects.get(id=id)
    form = OccurrenceForm(instance=data)
    if request.method == 'POST':
        form = OccurrenceForm(request.POST,request.FILES, instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.occurrence_giver = request.user
            instance.occurrence_id = unique_id(id=request.user.id)
            instance.save()
            print(form.errors)
            return redirect('occurrence_report')
    context = {
        'form': form,
        'id': id
    }
    return render(request,'medic/edit_occurence.html', context)



def dragable_form(request):
    return render(request, 'medic/dragable_form.html')

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


@csrf_exempt
def feedback(request):
    url = request.META.get('HTTP_REFERER')
    value = ''
    if request.method == 'POST':
        feedback = request.POST
        for k,v in feedback.items():
            if v:
                value = v
        if value!='':
            Feedback.objects.create(author_id = request.user.id, feedback_text = value)
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


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


class AmbulanceRequestUpdate(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(AmbulanceModel, pk=pk)
        context = {
            'data': data
        }
        return render(request, 'medic/ambulance_req_up.html', context)

    def post(self, request, pk):
        data = get_object_or_404(AmbulanceModel, pk=pk)
        form = AmbulanceModelForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('ambulance_request_report')
        context = {
            'data': data
        }

        return render(request, 'medic/ambulance_req_up.html', context)


class AmbulanceTrackLocation(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = AmbulanceModel.objects.get(pk=pk)
        context = {
            'data': data
        }
        return render(request, 'medic/trac_req.html', context)


class AmbulanceRequestDelete(LoginRequiredMixin,View):

    def get(self, request, pk):
        try:
            data = get_object_or_404(AmbulanceModel, pk=pk)
            if data:
                data.delete()
            return redirect('ambulance_request_report')

        except:
            return redirect('ambulance_request_report')


def dispatch_list(request):
    return render(request, 'medic/dispatch_list.html')


def hospital_transfer(request):
    return render(request, 'medic/hospita_transfer.html')


def hospital_transfer_report(request):
    return render(request, 'medic/hospita_transfer_report.html')

@login_required
def panic_system(request):
    panic = 'Give a panic request'
    if request.method == 'POST':
        reason = request.POST.get('reason')
        emergency_contact = request.POST.get('emergency_contact')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        place = request.POST.get('place')
        emmergency_contact = request.POST.get('emmergency_contact')
        my_panic = Panic.objects.create(panic_sender_id=request.user.id, emergency_contact = emergency_contact , reason=reason, place = place ,lat=lat, lng=lng)
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
                'email': panic.panic_sender.username,
                'first_name': panic.panic_sender.first_name,
                'contact': panic.panic_sender.contact,
                'emergency_contact': panic.emergency_contact,
                'reason': panic.reason,
                'place': panic.place,
                'timestamp': panic.timestamp,
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


class Panic_Noti(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = PanicNotiSerializer
    def get_queryset(self):
        return PanicNoti.objects.filter(is_responded = False)


def property_report(request):
    day_property = PropertyTools.objects.filter(created__date = this_day)
    week_property = PropertyTools.objects.filter(created__iso_week_day__gte = 1,\
                                                created__month = this_month, \
                                                created__year = this_year)
    month_property = PropertyTools.objects.filter(created__month = this_month, \
                                                created__year = this_year)
    context = {
        'day_property': day_property,
        'week_property': week_property,
        'month_property': month_property,
    }
    return render(request,'medic/property_report.html',context)


def property_add(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            total = price*quantity
            instance.total_price = total
            type = instance.property_type
            type = type[:1]
            instance.invoice_id = invoice_no(type)
            instance.save()
            messages.success(request,'Property Report Created')
            return redirect('property_report')
    context = {
        'form': form
    }
    return render(request,'medic/property_form.html',context)


def property_edit(request,id):
    data = PropertyTools.objects.get(id = id)
    form = PropertyForm(instance=data)
    if request.method == 'POST':
        form = PropertyForm(request.POST,instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            total = price*quantity
            instance.total_price = total
            instance.user = request.user
            type = instance.property_type
            type = type[:1]
            instance.invoice_id = invoice_no(type)
            instance.save()
            messages.success(request,'Property has been edited')
            return redirect('property_report')
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/property_edit.html',context)
    

def property_del(request,id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(PropertyTools, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(url)
    

def render_to_pdf(template,context):
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")


def invoice_pdf_property(request,id):
    property = PropertyTools.objects.get(id=id)
    context = {
        'property': property,
        'id':id
    }
    template = get_template('medic/property_pdf_invoice.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=invoice.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def faq(request):
    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs,
    }
    return render(request,'medic/faq.html',context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def create_faq(request):
    if request.method == 'POST':
        qs = request.POST.get('ques')
        ans = request.POST.get('ans')
        FAQ.objects.create(author = request.user, ques = qs, ans = ans)
        messages.success(request,'FAQ was created')
        return redirect('faq')
    return render(request,'medic/create_faq.html')


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def edit_faq(request,id):
    data = FAQ.objects.get(id =id)
    form = FAQFORM(instance=data)
    if request.method == 'POST':
        form = FAQFORM(request.POST,request.FILES,instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request,'FAQ was Edited')
            return redirect('faq')
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/edit_faq.html',context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def del_faq(request,id):
    obj = get_object_or_404(FAQ, id = id)
    obj.delete()
    return redirect('faq')