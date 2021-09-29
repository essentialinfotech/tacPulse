from __future__ import division
from django import dispatch
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import success
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from .models import *
from Accounting.models import *
from django.http import HttpResponseRedirect, HttpResponse, request
from django.contrib import messages
import json
from django.db.models import Sum, Q,query
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from Accounting.models import *
from Accounting.forms import *
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
import base64
from django.core.files.base import ContentFile
from django.views.generic import CreateView,ListView,TemplateView,UpdateView,DeleteView
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


def case_number():
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    case_no = '#C'+str(round(timestamp))
    return case_no


# Create your views here.
@login_required
def audit_report(request):
    audits = Audit.objects.all()
    context = {
        'audits': audits,
    }
    return render(request, 'medic/audit_report.html',context)

@login_required
def inspection_form(request):
    return render(request, 'medic/inspection_form.html')

@login_required
def inspaction_report(request):
    return render(request, 'medic/inspaction_report.html')

@login_required
def occurrence_form(request):
    form = OccurrenceForm()
    if request.method == 'POST':
        form = OccurrenceForm(request.POST,request.FILES)
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

@login_required
def occurrence_report(request):
    from datetime import datetime, timedelta
    last_seven_days = datetime.today() - timedelta(days=7)
    print(last_seven_days)
    monthly_occurences = Occurrence.objects.filter(created__month = this_month, \
                                                    created__year = this_year)

    daily_occurences = Occurrence.objects.filter(created__date = this_day)

    weekly_occurences = Occurrence.objects.filter(created__gte = last_seven_days,\
                                                     created__month = this_month,
                                                    created__year = this_year)

    context = {
        'monthly_occurences': monthly_occurences,
        'daily_occurences': daily_occurences,
        'weekly_occurences': weekly_occurences,
    }
    return render(request,'medic/occurrence_report.html', context)

@login_required
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

@login_required
def edit_occurrence(request,id):
    data = Occurrence.objects.get(id=id)
    form = OccurrenceForm(instance=data)
    if request.method == 'POST':
        form = OccurrenceForm(request.POST,request.FILES,instance=data)
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

@login_required
def occurrence_details(request,id):
    obj = Occurrence.objects.get(id = id)
    context = {
        'obj': obj,
    }
    return render(request,'medic/detail_occurrence.html',context)

@login_required
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

@login_required
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

@login_required
def feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-id')
    context = {
        'feedbacks': feedbacks,
    }
    return render(request,'medic/feedbacks_view.html',context)

@login_required
def del_feedback(request,id):
    obj = get_object_or_404(Feedback, id=id)
    obj.delete()
    messages.success(request,'Feedback Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# this is for incident report by dispatch not a a form submitted by user
def ambulance_request(request):
    form = EmergencyMedDisIncidentReportForm()
    senior_form = SeniorForm()
    scribe_form = ScribeForm()
    assist_1_form = Assist01Form()
    assist_2_form = Assist02Form()

    if request.method == 'POST':
        form = EmergencyMedDisIncidentReportForm(request.POST,request.FILES)
        senior_form = SeniorForm(request.POST)
        scribe_form = ScribeForm(request.POST)
        assist_1_form = Assist01Form(request.POST)
        assist_2_form = Assist02Form(request.POST)

        main_form = request.POST.get('main_form')

        if senior_form.is_valid():
            senior_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if scribe_form.is_valid():
            scribe_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if assist_1_form.is_valid():
            assist_1_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if assist_2_form.is_valid():
            assist_2_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        if main_form is not None:
            if form.is_valid():
                # decoding webcam image from text string to image
                photo = request.POST.get('photo')
                format, imgstr = photo.split(';base64,') 
                ext = format.split('/')[-1] 
                photo = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                # decoding signature canvas from text string to image
                signature = request.POST.get('signature')
                format, imgstr = signature.split(';base64,') 
                ext = format.split('/')[-1] 
                signature = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                photos_and_other_choices = request.POST.get('photos_and_other_choices')
                if photos_and_other_choices is not None:
                    add_space = " "
                    photos_and_other_choices = add_space.join(photos_and_other_choices)
                instance = form.save(commit=False)
                instance.photo = photo
                instance.signature = signature
                instance.photos_and_other_choices = photos_and_other_choices
                instance.user = request.user
                instance.save()
                return redirect('fill_vehicle_details', id=instance.id,total_unit = instance.how_many_units_dispatched)

    context = {
        'senior_form': senior_form,
        'scribe_form': scribe_form,
        'assist_1_form': assist_1_form,
        'assist_2_form': assist_2_form,
        'form': form,
        }
    return render(request, 'medic/ambulance_request.html',context)


def fill_vehicle_details(request,id,total_unit):
    incident = AmbulanceModel.objects.get(id = id)
    vehicle_with_unit = Vehicles_count_with_info_for_ambulance_request.objects.filter(vehicle_for_id = id).count()

    if vehicle_with_unit == int(incident.how_many_units_dispatched):
        return redirect('dispatch_incident_report_pdf', id)

    if request.method == 'POST':
        vehicle_no = request.POST.get('vehicle_no')
        responding = request.POST.get('responding')
        odo01 = request.POST.get('odo01')
        on_scene = request.POST.get('on_scene')
        odo2 = request.POST.get('odo2')
        depart_scene = request.POST.get('depart_scene')
        arrive_fac = request.POST.get('arrive_fac')
        odo3 = request.POST.get('odo3')
        hand_over = request.POST.get('hand_over')
        depart = request.POST.get('depart')
        end_standing_free = request.POST.get('end_standing_free')
        odo04 = request.POST.get('odo04')

        Vehicles_count_with_info_for_ambulance_request.objects.create(
            vehicle_for_id = id,
            vehicle_no = vehicle_no,
            responding = responding,
            odo01 = odo01,
            on_scene = on_scene,
            odo2 = odo2,
            depart_scene = depart_scene,
            arrive_fac = arrive_fac,
            odo3 = odo3,
            hand_over = hand_over,
            depart = depart,
            end_standing_free = end_standing_free,
            odo04 = odo04,
        )

    context = {
        'incident': incident,
        'id': id,
        'total_unit': total_unit,
    }
    return render(request,'medic/vehicle_detail_for_incident.html',context)


class AmbulanceRequestReport(LoginRequiredMixin, View):
    from datetime import datetime, timedelta

    today = datetime.today()
    week = datetime.today().date() - timedelta(days=7)
    month = datetime.today().date() - timedelta(days=30)

    def get(self, request):
        monthly=''
        daily=''
        weekly=''
        user_id = request.user.id
        if self.request.user.is_superuser:
            daily = AmbulanceModel.objects.filter(created_on__gte=self.today.date())
            weekly = AmbulanceModel.objects.filter(created_on__gte=self.week)
            monthly = AmbulanceModel.objects.filter(created_on__gte=self.month)
        elif not self.request.user.is_superuser and not self.request.user.is_staff:
            daily = AmbulanceModel.objects.filter(user=user_id, created_on__gte=self.today.date())
            weekly = AmbulanceModel.objects.filter(user=user_id, created_on__gte=self.week)
            monthly = AmbulanceModel.objects.filter(user=user_id, created_on__gte=self.month)
        context = {
            'weekly': weekly,
            'daily': daily,
            'monthly': monthly
        }
        return render(request, 'medic/ambulance_request_report.html', context)


@login_required
def ambulance_request_real(request):
    pass



class AmbulanceRequestDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(AmbulanceModel, pk=pk)
        task = False
        task_data = ''
        desc = ''
        dispatch_id= ''
        if request.user.is_staff:
            task_data = TaskModel.objects.filter(task_type='ambr', ambulance_task=pk)
            for i in task_data:
                dispatch_id = i.dispatch.id
                desc = i.task_desc
            if dispatch_id == request.user.id:
                task = True
                task_data = desc
        context = {
            'data': data,
            'task': task,
            'task_data': task_data
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

@login_required
def ambulance_task_complete(request, pk):
    TaskModel.objects.filter(task_type='ambr', ambulance_task=pk).update(status='Completed')
    ambulance = get_object_or_404(AmbulanceModel, pk=pk)
    ambulance.completed = True
    ambulance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def dispatch_list(request):
    dispatches = User.objects.filter(is_staff = True,is_superuser = False)
    return render(request, 'medic/dispatch_list.html',{'dispatches': dispatches})

@login_required
def hospital_transfer(request):
    form = HospitalTransferForm()
    if request.method == 'POST':
        form = HospitalTransferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Tranfer request sent')
            return redirect('hospital_transfer_report')
    return render(request, 'medic/hospital_transfer.html', {'form': form})

@login_required
def hospital_transfer_report(request):
    from datetime import datetime, timedelta
    today = datetime.today()
    week = datetime.today().date() - timedelta(days=7)
    month = datetime.today().date() - timedelta(days=30)
    if request.user.is_superuser:
        daily = HospitalTransferModel.objects.filter(created_on__gte=today.date()).order_by('-id')
        weekly = HospitalTransferModel.objects.filter(created_on__gte=week).order_by('-id')
        monthly = HospitalTransferModel.objects.filter(created_on__gte=month).order_by('-id')
    elif not request.user.is_staff:
        user_id = request.user.id
        daily = HospitalTransferModel.objects.filter(requested_by=user_id, created_on__gte=today.date()).order_by('-id')
        weekly = HospitalTransferModel.objects.filter(requested_by=user_id, created_on__gte=week).order_by('-id')
        monthly = HospitalTransferModel.objects.filter(requested_by=user_id, created_on__gte=month).order_by('-id')
    context = {
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly
    }
    return render(request, 'medic/hospita_transfer_report.html', context)

@login_required
def update_hospital_request(request, pk):
    data = get_object_or_404(HospitalTransferModel, pk=pk)
    form = HospitalTransferForm(instance=data)
    if request.method == 'POST':
        form = HospitalTransferForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('hospital_transfer_report')
    return render(request, 'medic/hospital_transfer_up.html', {'form': form, 'data': data})

@login_required
def delete_hospital_request(request, pk):
    if not request.user.is_staff or request.user.is_superuser:
        data = get_object_or_404(HospitalTransferModel, pk=pk)
        data.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def details_hospital_request(request, pk):
    data = get_object_or_404(HospitalTransferModel, pk=pk)
    return render(request, 'medic/hos_request_detail.html', {'object':data})

@login_required
def hospital_transfered(request, pk):
    if request.user.is_staff:
        data = get_object_or_404(HospitalTransferModel, pk=pk)
        TaskModel.objects.filter(task_type='HT', hos_tra=pk).update(status='Completed')
        data.completed = True
        data.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('forbidden')


@login_required
def panic_system(request):
    panic = 'Give a panic request'
    if request.method == 'POST':
        reason = request.POST.get('reason')
        emergency_contact = request.POST.get('emergency_contact')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        place = request.POST.get('place')
        my_panic = Panic.objects.create(panic_sender_id=request.user.id, emergency_contact = emergency_contact , reason=reason, place = place ,lat=lat, lng=lng)
        if request.user.is_staff:
            return redirect('check_panic_requests_location', id=my_panic.id)
        else:
            return HttpResponse('Panic request sent successfully')
    return render(request, 'medic/panic.html', {'panic': panic})

@login_required
def del_panic(request, id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(Panic, id=id)
    obj.delete()
    return HttpResponseRedirect(url)

@login_required
def check_panic_requests(request):
    panic_requests = Panic.objects.all().order_by('-id')
    context = {
        'panic_requests': panic_requests,
    }
    return render(request, 'medic/panic_requests.html', context)

@login_required
def check_panic_requests_location(request, id):
    context = {}
    if request.user.is_staff:
        task = False
        try:
            this_panic = Panic.objects.filter(id=id)
            panic = Panic.objects.get(id=id)
            task_data = TaskModel.objects.filter(task_type='pan', panic_task=id)
            for i in task_data:
                task_data = i.task_desc
            if task_data:
                task = True

            context = {
                'task': task,
                'task_data': task_data,
                'email': panic.panic_sender.username,
                'first_name': panic.panic_sender.first_name,
                'contact': panic.panic_sender.contact,
                'emergency_contact': panic.emergency_contact,
                'reason': panic.reason,
                'place': panic.place,
                'timestamp': panic.timestamp,
                'lat': panic.lat,
                'lng': panic.lng,
                'this_panic': this_panic,
                'id': id,
            }

        except:
            return HttpResponse('This panic data has been deleted/not found')
    elif request.user.is_authenticated:
        try:
            this_panic =Panic.objects.filter(id = id)
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
                'this_panic':this_panic,
                'id':id,
            }
        except:
            return HttpResponse('This panic data has been deleted/not found')

    else:
        return HttpResponse('Please Login First')
    return render(request, 'medic/panic_location_check_admin.html', context)


@login_required
def complete_panic_task(request, pk):
    if request.user.is_staff:
        TaskModel.objects.filter(task_type='pan', panic_task=pk).update(status='Completed')
        panic = get_object_or_404(Panic, pk=pk)
        panic.completed = True
        panic.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('forbidden')

@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def panic_noti(request):
    data = []
    noti = PanicNoti.objects.filter(is_seen = False).order_by('-id')
    for i in noti:
        prefetch = {
            'first_name': i.panic.panic_sender.first_name,
            'last_name': i.panic.panic_sender.last_name,
            'noti_text': i.text,
            'is_seen': i.is_seen,
            'created': i.created,
            'panic_id': i.panic.id,
            'noti_id': i.id,
        }
        data.append(prefetch)
    return JsonResponse(data,safe=False)

@login_required
def mark_seen_panic_noti(request,id):
    noti = PanicNoti.objects.get(id = id)
    noti.is_seen = True
    noti.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def property_report(request):
    from datetime import datetime, timedelta
    last_seven_days = datetime.today() - timedelta(days=7)
    day_property = PropertyTools.objects.filter(created__date = this_day)
    week_property = PropertyTools.objects.filter(created__gte = last_seven_days,\
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

@login_required
def property_add(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            print(quantity)
            vat = form.cleaned_data['vat']
            price = form.cleaned_data['price']
            vat_amount = price*(vat/100)
            price_with_vat = price + vat_amount
            total = price_with_vat*quantity
            instance = form.save(commit=False)
            instance.total_price = total
            instance.user = request.user
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

@login_required
def property_edit(request,id):
    data = PropertyTools.objects.get(id = id)
    form = PropertyForm(instance=data)
    if request.method == 'POST':
        form = PropertyForm(request.POST,instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            quantity = instance.quantity
            vat = instance.vat
            price = instance.price
            vat_amount = price*(vat/100)
            price_with_vat = price + vat_amount
            total = price_with_vat*quantity
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
    

@login_required
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
        content = "inline; filename=invoice_property.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def dispatch_incident_report_pdf(request,id):
    incident = AmbulanceModel.objects.get(id = id)
    vehicles = Vehicles_count_with_info_for_ambulance_request.objects.filter(vehicle_for_id = id)
    current_site = get_current_site(request)
    context = {
        'incident': incident,
        'vehicles': vehicles,
        'id':id,
        'domain': current_site.domain,
    }
    template = get_template('medic/dispatch_incident_report_pdf.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=incident_report.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


@login_required
def faq(request):
    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs,
    }
    return render(request,'medic/faq.html',context)

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def create_faq(request):
    if request.method == 'POST':
        qs = request.POST.get('ques')
        ans = request.POST.get('ans')
        FAQ.objects.create(author = request.user, ques = qs, ans = ans)
        messages.success(request,'FAQ was created')
        return redirect('faq')
    return render(request,'medic/create_faq.html')

@login_required
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

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def del_faq(request,id):
    obj = get_object_or_404(FAQ, id = id)
    obj.delete()
    return redirect('faq')

@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def case_notes(request):
    cases = CaseNote.objects.all().order_by('-id')
    context = {
        'cases': cases,
    }
    return render(request,'medic/case_reports.html',context)

@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def case_note_create(request,id):
    panic = get_object_or_404(Panic,id = id)
    case = CaseNote.objects.filter(case_panic_id = panic)
    if case:
        return HttpResponse('Case already created')
    else:
        form = CaseForm()
        if request.method == 'POST':
            form = CaseForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.creator = request.user
                instance.case_no = case_number()
                instance.case_panic = panic
                instance.save()
                messages.success(request,'Case Note created')
                return redirect('case_notes')
    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'medic/case_note_form.html',context)

@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def case_del(request,id):
    obj = CaseNote.objects.get(id=id)
    obj.delete()
    messages.success(request,'Note Deleted')
    return redirect('case_notes')

@login_required
def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            user = User.objects.filter(Q(first_name__startswith = query) | Q(last_name__startswith = query) | \
                                        Q(username__startswith = query) | Q(contact__startswith = query))
            if user:
                context = {
                    'user': user,
                }
                return render(request,'medic/search_results.html',context)
            else:
                return HttpResponse('Not Found')
        else:
            return HttpResponse('Empty Query Field can not be found')

@login_required    
def autocomplete(request):
    mylist = []
    term = request.GET.get('term')
    user = User.objects.filter(Q(first_name__startswith = term) | Q(last_name__startswith = term) | \
                                Q(username__startswith = term) | Q(contact__startswith = term))
    if user:
        mylist += [i.first_name for i in user]
    else:
        mylist = ['No user found']
    return JsonResponse(mylist, safe=False)


def noti_length(request):
    total_noti_length = 0
    if request.user.is_superuser:
        panic_noti = PanicNoti.objects.filter(is_seen = False).count()
        membership_noti = MembershipNoti.objects.filter(is_seen = False).count()
        renewal_noti = MembershipRenewalNoti.objects.filter(is_seen = False).count()
        h_transfer_noti = HospitalTransferNoti.objects.filter(mark_read_admin = False).count()
        total_noti_length = panic_noti + membership_noti + h_transfer_noti + renewal_noti

    if request.user.is_staff and not request.user.is_superuser:
        renewal_noti = MembershipRenewalNoti.objects.filter(noti_for__user_id = request.user.id,is_seen = False).count()
        h_transfer_noti = HospitalTransferNoti.objects.filter(mark_read_admin = False)
        panic_noti = PanicNoti.objects.filter(is_seen = False).count()
        total_noti_length = panic_noti + renewal_noti + h_transfer_noti

    if not request.user.is_staff and not request.user.is_superuser:
        renewal_noti = MembershipRenewalNoti.objects.filter(noti_for__user_id = request.user.id,is_seen = False).count()
        h_transfer_noti = HospitalTransferNoti.objects.filter(noti_for__requested_by = request.user,mark_read_user = False).count()
        total_noti_length = renewal_noti + h_transfer_noti
    data = {
        'total_noti_length': total_noti_length,
    }
    return JsonResponse(data,safe=False)

        
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def membership_earnings_monthly_chart_dashboard(request):
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = []
    user_join_data = []
    Jan = 0
    Feb = 0
    Mar = 0
    Apr = 0
    May = 0
    Jun = 0
    Jul = 0
    Aug = 0
    Sep = 0
    Oct = 0
    Nov = 0
    Dec = 0

    for i in range(0, 13):
        if i == 1:
            Jan = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Jan.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            jan = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(jan)
        if i == 2:
            Feb = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Feb.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Feb = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Feb)
        if i == 3:
            Mar = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Mar.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Mar = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Mar)
        if i == 4:
            Apr = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Apr.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Apr = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Apr)
        if i == 5:
            May = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in May.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            May = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(May)
        if i == 6:
            Jun = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Jun.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Jun = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Jun)
        if i == 7:
            Jul = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Jul.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Jul = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Jul)
        if i == 8:
            Aug = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Aug.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Aug = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Aug)
        if i == 9:
            Sep = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Sep.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Sep = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Sep)
        if i == 10:
            Oct = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Oct.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Oct = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Oct)
        if i == 11:
            Nov = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Nov.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Nov = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Nov) 
        if i == 12:
            Dec = MembershipModel.objects.filter(
                membership_date__month=i, membership_date__year=this_year).values(
                'package__p_price').aggregate(Sum('package__p_price'))
            for k,v in Dec.items():
                if v is not None:
                    data.append(v)
                else:
                    v = 0
                    data.append(v)
            Dec = User.objects.filter(is_staff = False, date_joined__month = i, date_joined__year = this_year).count()
            user_join_data.append(Dec)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'user_join_data': user_join_data,
    })


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def audit_form(request):
    form = AuditForm()
    if request.method == 'POST':
        form = AuditForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.auditor = request.user
            instance.save()
            messages.success(request,'Audit Created')
            return redirect('audit_report')
    context = {
        'form': form,
    }
    return render(request, 'medic/audit_form.html',context)


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def audit_edit(request,id):
    data = Audit.objects.get(id = id)
    form = AuditForm(instance=data)
    if request.method == 'POST':
        form = AuditForm(request.POST,instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.auditor = request.user
            instance.save()
            messages.success(request,'Audit Edited')
            return redirect('audit_report')
    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'medic/audit_edit.html',context)

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def audit_delete(request,id):
    obj = get_object_or_404(Audit, id=id)
    obj.delete()
    messages.success(request,'Audit Deleted')
    return redirect('audit_report')


def create_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.success(request,'Post Created')
        return redirect('blog_list')
    context = {
        'form': form,
    }
    return render(request,'medic/create_blog.html',context)


def blog_list(request):
    blogs = Blog.objects.all().order_by('-id')
    context = {
        'blogs': blogs,
    }
    return render(request,'medic/all_blogs.html',context)


def single_blog(request,id):
    blog = Blog.objects.get(id = id)
    context = {
        'blog': blog,
    }
    return render(request,'medic/single_blog.html',context)


@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def Ambulance_request_noti_for_admin_dispatch(request):
    data = []
    noti = AmbulanceNoti.objects.filter(mark_read_admin = False).order_by('-id')
    for i in noti:
        prefetch = {
            'first_name': i.noti_for.user.first_name,
            'last_name': i.noti_for.user.last_name,
            'text': i.text,
            'mark_read_admin': i.mark_read_admin,
            'created': i.created,
            'noti_id': i.id,
            'ambulance_req_id': i.noti_for.id,
        }
        data.append(prefetch)
    return JsonResponse(data,safe=False)


@login_required
def hospital_transfer_noti_for_admin_dispatch(request):
    data = []
    if request.user.is_staff:
        noti = HospitalTransferNoti.objects.filter(mark_read_admin = False).order_by('-id')
    else:
        noti = HospitalTransferNoti.objects.filter(noti_for__requested_by = request.user,mark_read_user = False).order_by('-id')
    for i in noti:
        prefetch = {
            'first_name': i.noti_for.requested_by.first_name,
            'last_name': i.noti_for.requested_by.last_name,
            'text': i.text,
            'mark_read_admin': i.mark_read_admin,
            'created': i.created,
            'noti_id': i.id,
            'ambulance_req_id': i.noti_for.id,
        }
        data.append(prefetch)
    return JsonResponse(data,safe=False)


@login_required
def h_transfer_noti_mark_seen(request,id):
    obj = HospitalTransferNoti.objects.get(id=id)
    if request.user.is_staff:
        obj.mark_read_admin = True
        obj.save()
    else:
        obj.mark_read_user = True
        obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class FormSave(View):
    def get(self,request):
        data = request.GET.get('json')
        title = request.GET.get('title')
        FormBuilder.objects.create(title=title,json=data)
        return render(request,'medic/form-builder.html')


class FormList(ListView):
    model = FormBuilder
    template_name = 'medic/form-list.html'


class Form(View):
    def get(self, request,pk):
        get_form = FormBuilder.objects.get(id=pk)
        json_form = json.loads(get_form.json)
        context = {
            'id': json.dumps(pk),
            'json_form':json.dumps(json_form),
        }
        return render(request,'medic/forms.html',context)


def SaveForm(request):
    data = request.GET.get('formdata')
    id = request.GET.get('id')
    FormData.objects.create(form_id=int(id),data=data)
    return JsonResponse({"data":"success"})


class FormDatatable(View):
    def get(self,request,pk):
        data = FormData.objects.filter(form_id=pk)
        context = {
            'data':data
        }
        return render(request,'medic/form-submit.html',context)


class FormDatas(View):
    def get(self,request):
        data = [{
            "zipcode": "01262",
            "city": "Stockbridge",
            "county": "Berkshire"
        }, {
            "zipcode": "02881",
            "city": "Kingston",
            "county": "Washington"
        }, {
            "zipcode": "03470",
            "city": "Winchester",
            "county": "Cheshire"
        }, {
            "zipcode": "14477",
            "city": "Kent",
            "county": "Orleans"
        }, {
            "zipcode": "28652",
            "city": "Minneapolis",
            "county": "Avery"
        }, {
            "zipcode": "98101",
            "city": "Seattle",
            "county": "King"
        }]
        return HttpResponse(data)