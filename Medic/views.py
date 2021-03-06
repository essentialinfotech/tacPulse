from __future__ import division
from email.mime import image
from django import dispatch
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import success
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Accounting.views import vehicle_maintenance
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
from Medic.utils import pdf
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

from django.utils.decorators import method_decorator
import requests

# global
this_month = datetime.datetime.now().month
this_day = datetime.datetime.today()
this_year = datetime.datetime.now().year


def invoice_no(type):
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    invoice_no = '#'+str(type) + str(round(timestamp))
    return invoice_no

def unique_id(id):
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    unique_id = '#'+str(round(timestamp)) + str(-(id))
    return unique_id

def case_number():
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    case_no = '#' + str(timestamp)
    if '.' in case_no:
        case_no = case_no.replace('.', '')
    return case_no

def run_id(call_number):
    if len(str(call_number)) == 1:
        call_number = '0' + str(call_number)
    time = datetime.datetime.now().strftime("%Y%m%d")
    unique_run_id = 'TP#' + str(time) + '/' + str(call_number)
    return unique_run_id

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


# this is for dispatch emergency incident report . not an ambulance  form submitted by user
def ambulance_request(request):
    form = EmergencyMedDisIncidentReportForm()

    # generating run ID
    today_date = this_day.date()
    todays_emergency_calls = AmbulanceModel.objects.filter(created_on__date = today_date).count()
    caller_number = todays_emergency_calls + 1
    generate_run_id = run_id(caller_number)

    if request.method == 'POST':
        main_form = request.POST.get('main_form')
        if main_form is not None:
            panic_id = request.POST.get('panic_id')
            form = EmergencyMedDisIncidentReportForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.run_id = generate_run_id
                instance.save()

                try:
                    panic = Panic.objects.get(id = int(panic_id))
                except:
                    panic = None
                if panic is not None:
                    check_if_any_panic_assigned = AmbulanceModel.objects.filter(panic = panic)
                    if check_if_any_panic_assigned:
                        instance.delete()
                        return HttpResponse('This panic id is already assigned to a dispatch incident')
                instance.panic = panic
                instance.save()
                return redirect('dispatch_incident_crew_and_vehicle', id=instance.id)

    context = {
        'form': form,
        'generate_run_id': generate_run_id,
        }
    return render(request, 'medic/ambulance_request.html',context)


def dispatch_incident_crew_and_vehicle(request,id):
    ambulance_model = AmbulanceModel.objects.get(id = id)
    run_id = ambulance_model.run_id
    backslash = '\n'

    user = User.objects.filter(medic = True)
    assigned_units = DispatchIncidentCrewAndVehicle.objects.filter(parent_id = id)

    form = DispatchIncidentCrewAndVehicleForm()
    # senior_form = SeniorForm()
    # assist_1_form = Assist01Form()
    # assist_2_form = Assist02Form()
    if request.method == 'POST':
        # senior_form = SeniorForm(request.POST)
        # assist_1_form = Assist01Form(request.POST)
        # assist_2_form = Assist02Form(request.POST)

        # if senior_form.is_valid():
        #     senior_form.save()
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # if assist_1_form.is_valid():
        #     assist_1_form.save()
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # if assist_2_form.is_valid():
        #     assist_2_form.save()
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        main_form = request.POST.get('main_form')
        if main_form is not None:
            data = []

            form = DispatchIncidentCrewAndVehicleForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.parent_id = id
                instance.save()

                other_medics = request.POST.get('other_medics')
                if other_medics is not None:
                    medic_lists = request.POST.getlist('paramedics')
                    medics = User.objects.filter(id__in = list(medic_lists)).values_list('contact', flat=True)

                    for i in medics:
                        contacts = {
                            'address': str(i),
                        }
                        data.append(contacts)

                    for i in medic_lists:
                        assigned_medics = AssignedParamedicsAfterDispatchIncidentCrewAndVehicle.objects.create(
                                                                                                parent = instance.parent,
                                                                                                for_crew_id = instance.id,
                                                                                                paramedics_id = i,
                                                                                            )

                    requests.post(
                        'https://api.bulksms.com/v1/messages',
                        headers = {
                                'Authorization': 'Basic' + ' ' +  'dGFjX3B1bHNlOmxvdmViaXRl',
                            },

                        json = {
                                "to": data,
                                "body": "You have assigned with a task of emergency medical response please check your app for further details"
                            }
                    )

                else:
                    unit = request.POST.get('assigned_unit')
                    get_unit_paramedics_contacts = AssignUnitCreateWithParamedics.objects.filter(uni_name_id = unit).values_list('paramedics__contact', flat=True)
                    get_medic_ids = AssignUnitCreateWithParamedics.objects.filter(uni_name_id = unit).values_list('paramedics_id', flat=True)

                    for i in get_unit_paramedics_contacts:
                        contacts = {
                            'address': str(i),
                        }
                        data.append(contacts)
                    print(data)

                    for i in get_medic_ids:
                        assigned_medics = AssignedParamedicsAfterDispatchIncidentCrewAndVehicle.objects.create(
                                                                                                parent = instance.parent,
                                                                                                for_crew_id = instance.id,
                                                                                                paramedics_id = i,
                                                                                            )
                    # sending SMS to paramedics
                    requests.post(
                        'https://api.bulksms.com/v1/messages',
                        headers = {
                                'Authorization': 'Basic' + ' ' +  'dGFjX3B1bHNlOmxvdmViaXRl',
                            },

                        json = {
                                "to": data,
                                "body": f"""You have been {backslash} allocated case {backslash} {run_id} by {backslash} TAC-Pulse ERS (WEB). {backslash} Please open the {backslash} TAC-Pulse ERS App {backslash} for further details."""
                            }
                    )
                    
                    # sending SMS to patient/caller/panic sender(caller_number)
                    requests.post(
                        'https://api.bulksms.com/v1/messages',
                        headers = {
                                'Authorization': 'Basic' + ' ' +  'dGFjX3B1bHNlOmxvdmViaXRl',
                            },

                        json = {
                                "to": [{
                                    'address': str(ambulance_model.caller_number),
                                }],

                                "body": f"""TAC-Pulse ERS has dispatched {backslash} an ambulance to assist you. {backslash} Please have your medical {backslash} aid card,and ID document {backslash} ready. Your call reference number is {run_id} {backslash} | 0861 666 911"""
                            }
                    )
                return redirect('add_another_dispatch_incident_crew_and_vehicle', id)

    context = {
        'user': user,
        'form': form,
        # 'senior_form': senior_form,
        # 'assist_1_form': assist_1_form,
        # 'assist_2_form': assist_2_form,
        'assigned_units': assigned_units,
        'id': id,
    }
    return render(request,'medic/dispatch_incident_crew_and_vehicle.html',context)


@login_required
def add_another_dispatch_incident_crew_and_vehicle(request,id):
    assigned_units = DispatchIncidentCrewAndVehicle.objects.filter(parent_id = id)
    paramedics = AssignedParamedicsAfterDispatchIncidentCrewAndVehicle.objects.filter(parent_id = id)
    print(assigned_units,paramedics)
    context = {
        'assigned_units': assigned_units,
        'paramedics': paramedics,
        'id':id,
    }
    return render(request,'medic/add_another_dispatch_incident_crew_and_vehicle.html',context)


@login_required
def dispatch_incident_travel_details(request,id):
    dispatch_incident_main_model = AmbulanceModel.objects.get(id = id)
    units = dispatch_incident_main_model.how_many_units_dispatched
    total_form = Vehicles_count_with_info_for_ambulance_request.objects.filter(parent_id = id).count()
    # print(units,type(units),total_form)
    if int(units) == total_form:
        return redirect('dispatch_incident_service_notes', id)

    form = VehicleCountForm()
    if request.method == 'POST':
        form = VehicleCountForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent_id = id
            instance.save()
        if int(units) == total_form:
            return redirect('dispatch_incident_service_notes', id)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/vehicle_detail_for_incident.html',context)


@login_required
def dispatch_incident_service_notes(request,id):
    form = DispatchIncidentServiceNoteForm()
    scribe_form = ScribeForm()
    if request.method == 'POST':
        scribe_form = ScribeForm(request.POST)
        main_form = request.POST.get('main_form')
        if scribe_form.is_valid():
            scribe_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if main_form is not None:
            form = DispatchIncidentServiceNoteForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.parent_id = id
                instance.service_noted_by = request.user
                instance.save()
                return redirect('add_another_dispatch_incident_service_notes', id)
    context = {
        'scribe_form': scribe_form,
        'form': form,
        'id': id,
    }
    return render(request,'medic/dispatch_incident_service_notes.html',context)


@login_required
def add_another_dispatch_incident_service_notes(request,id):
    service_notes = DispatchIncidentServiceNotes.objects.filter(parent_id = id)
    context = {
        'service_note': service_notes,
        'id': id,
    }
    return render(request,'medic/add_another_dispatch_incident_service_notes.html',context)


@login_required
def dispatch_incident_location_details(request,id):
    form = DispatchIncidentLocationDetailsForm()
    if request.method == 'POST':
        form = DispatchIncidentLocationDetailsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent_id = id
            instance.save()
            return redirect('add_another_dispatch_incident_location_details', id)
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/dispatch_incident_location_details.html',context)


@login_required
def add_another_dispatch_incident_location_details(request,id):
    unit = DispatchIncidentLocationDetails.objects.filter(parent_id = id)
    context = {
        'unit': unit,
        'id': id,
    }
    return render(request,'medic/add_another_dispatch_incident_location_details.html',context)


@login_required
def dispatch_incident_patient_info(request,id):
    form = DispatchIncidentPatientInformationForm()
    if request.method == 'POST':
        form = DispatchIncidentPatientInformationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent_id = id
            instance.save()
            return redirect('add_another_dispatch_incident_patient_info', id)
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/dispatch_incident_patient_info.html',context)


@login_required
def add_another_dispatch_incident_patient_info(request,id):
    patient = DispatchIncidentPatientInformation.objects.filter(parent_id = id)
    context = {
        'patient': patient,
        'id': id,
    }
    return render(request,'medic/add_another_dispatch_incident_patient_info.html',context)


@login_required
def dispatch_incident_photos_and_others(request,id):
    form = DispatchIncidentPhotosForm()
    if request.method == 'POST':
        form = DispatchIncidentPhotosForm(request.POST,request.FILES)
        photo = request.POST.get('photo')
        if photo:
            # decoding webcam image from text string to image
            format, imgstr = photo.split(';base64,') 
            ext = format.split('/')[-1] 
            photo = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            photo = None

        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent_id = id
            instance.photo = photo
            instance.save()
            return redirect('add_another_dispatch_incident_photos_and_others', id)
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/dispatch_incident_photos_and_others.html',context)


@login_required
def add_another_dispatch_incident_photos_and_others(request,id):
    photos_and_other_choices = DispatchIncidentPhotos.objects.filter(parent_id = id)
    context = {
        'photos_and_other_choices': photos_and_other_choices,
        'id': id,
    }
    return render(request,'medic/add_another_dispatch_incident_photos_and_others.html',context)


@login_required
def dispatch_incident_dispatcher_certification(request,id):
    am_model = AmbulanceModel.objects.get(id = id)
    dispatcher_name = am_model.user.first_name + ' ' + am_model.user.last_name
    form = DispatchIncidentDispatcherCertificationForm()
    if request.method == 'POST':
        # dispatcher_name = request.POST.get('dispatcher_name')
        # if dispatcher_name:
        #     DispatchIncidentNameOfDispatcher.objects.create(dispatcher_name = dispatcher_name)
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        main_form = request.POST.get('main_form')
        if main_form:
            form = DispatchIncidentDispatcherCertificationForm(request.POST)

            # decoding signature canvas from text string to image
            signature = request.POST.get('signature')
            if signature:
                format, imgstr = signature.split(';base64,') 
                ext = format.split('/')[-1] 
                signature = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                signature = None
            if form.is_valid():
                instance = form.save(commit=False)
                instance.parent_id = id
                instance.signature = signature
                instance.save()
                return redirect('dispatch_incident_report_pdf', id)
            
    context = {
        'form': form,
        'dispatcher_name': dispatcher_name,
        'am_model': am_model,
        'id': id,
    }
    return render(request,'medic/dispatch_incident_dispatcher_certification.html', context)


@login_required
def dispatch_incident_submission_review_all(request):
    incident = AmbulanceModel.objects.all()
    context = {
        'incident': incident,
    }
    return render(request,'medic/dispatch_incident_submission_review_all.html',context)

@login_required
def dispatch_incident_submission_review(request,id):
    incident = AmbulanceModel.objects.get(id = id)
    crew_vehicle = DispatchIncidentCrewAndVehicle.objects.filter(parent_id = id)
    service_notes = DispatchIncidentServiceNotes.objects.filter(parent_id = id)
    loc_details = DispatchIncidentLocationDetails.objects.filter(parent_id = id)
    odo = Vehicles_count_with_info_for_ambulance_request.objects.filter(parent_id = id)
    patient_info = DispatchIncidentPatientInformation.objects.filter(parent_id = id)
    photos_other_documents = DispatchIncidentPhotos.objects.filter(parent_id = id)
    certificate = DispatchIncidentDispatcherCertification.objects.filter(parent_id = id)

    context = {
        'incident': incident,
        'crew_vehicle': crew_vehicle,
        'service_notes': service_notes,
        'loc_details': loc_details,
        'photos_other_documents': photos_other_documents,
        'certificate': certificate,
        'odo': odo,
        'patient_info': patient_info,
        'id':id,
    }
    return render(request,'medic/dispatch_incident_submission_review.html',context)

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
        if self.request.user.is_staff:
            daily = AmbulanceRequestModel.objects.filter(created_on__gte=self.today.date())
            weekly = AmbulanceRequestModel.objects.filter(created_on__gte=self.week)
            monthly = AmbulanceRequestModel.objects.filter(created_on__gte=self.month)
        elif not self.request.user.is_superuser and not self.request.user.is_staff:
            daily = AmbulanceRequestModel.objects.filter(user=user_id, created_on__gte=self.today.date())
            weekly = AmbulanceRequestModel.objects.filter(user=user_id, created_on__gte=self.week)
            monthly = AmbulanceRequestModel.objects.filter(user=user_id, created_on__gte=self.month)
        context = {
            'weekly': weekly,
            'daily': daily,
            'monthly': monthly
        }
        return render(request, 'medic/ambulance_request_report.html', context)


@login_required
def ambulance_request_real(request):
    form = AmbulanceModelForm()
    if request.method == 'POST':
        form = AmbulanceModelForm(request.POST,request.FILES)
        if form.is_valid():
            loc = request.POST.get('loc')
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')
            instance = form.save(commit = False)
            instance.user = request.user
            instance.loc = loc
            instance.lat = float(lat)
            instance.lng = float(lng)
            instance.save()
            messages.success(request,'Ambulance request was sent')
            return redirect('ambulance_request_report')
    context = {
        'form': form
    }
    return render(request,'medic/ambulance_request_form.html',context)



class AmbulanceRequestDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(AmbulanceRequestModel, pk=pk)
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
        data = AmbulanceRequestModel.objects.get(pk=pk)
        context = {
            'data': data
        }
        return render(request, 'medic/trac_req.html', context)


class AmbulanceRequestDelete(LoginRequiredMixin,View):

    def get(self, request, pk):
        try:
            data = get_object_or_404(AmbulanceRequestModel, pk=pk)
            if data:
                data.delete()
                messages.success('Ambulance Report was deleted')
            return redirect('ambulance_request_report')
        except:
            return redirect('ambulance_request_report')

@login_required
def ambulance_task_complete(request, pk):
    TaskModel.objects.filter(task_type='ambr', ambulance_task=pk).update(status='Completed')
    ambulance = get_object_or_404(AmbulanceRequestModel, pk=pk)
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
    form = PanicForWhome()
    if request.method == 'POST':
        reason = request.POST.get('reason')
        emergency_contact = request.POST.get('emergency_contact')
        for_whome = request.POST.get('for_whome')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        place = request.POST.get('place')
        my_panic = Panic.objects.create(panic_sender_id=request.user.id, 
                                        emergency_contact = emergency_contact ,
                                        for_whome = for_whome,
                                        reason=reason, place = place ,
                                        lat=lat, lng=lng)
        if request.user.is_staff:
            return redirect('check_panic_requests_location', id=my_panic.id)
        else:
            return HttpResponse('Panic request sent successfully')
    return render(request, 'medic/panic.html', {'panic': panic,'form': form,})

@login_required
def del_panic(request, id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(Panic, id=id)
    obj.delete()
    return HttpResponseRedirect(url)

@login_required
def check_panic_requests(request):
    panic_requests = Panic.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    panic_requests = Paginator(panic_requests, 30)
    try:
        panic_requests = panic_requests.page(page)
    except PageNotAnInteger:
        panic_requests = panic_requests.page(1)
    except EmptyPage:
        panic_requests = panic_requests.page(panic_requests.num_pages)

    context = {
        'panic_requests': panic_requests,
    }
    return render(request, 'medic/panic_requests.html', context)

@login_required
def check_panic_requests_location(request, id):
    context = {}
    if request.user.is_staff or request.user.medic:
        try:
            this_panic = Panic.objects.filter(id=id)
            panic = Panic.objects.get(id=id)
            dispatch_incident = panic.ambulancemodel_set.all()

            context = {
                'dispatch_incident': dispatch_incident,
                'panic': panic,
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
                'panic': panic,
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
            'sound_played': i.sound_played,
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

@csrf_exempt
def panic_noti_sound_off_view(request):
    if request.method == 'POST':
        data = request.POST
        for k,v in data.items():
            if k == 'noti_id':
                id = v
    noti = PanicNoti.objects.filter(id = id).update(sound_played = True)

    return JsonResponse('ok', safe=False)

@login_required
def mark_seen_panic_noti(request,id):
    noti = PanicNoti.objects.get(id = id)
    if request.user.is_superuser:
        noti.is_seen = True
        noti.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('you are not allowed to perform this action')

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
    # ParamedicsPhases will be here
    crew_vehicle = DispatchIncidentCrewAndVehicle.objects.filter(parent_id = id)
    service_notes = DispatchIncidentServiceNotes.objects.filter(parent_id = id)
    loc_details = DispatchIncidentLocationDetails.objects.filter(parent_id = id)
    odo = ParamedicsPhases.objects.filter(parent__parent_id = id)
    patient_info = DispatchIncidentPatientInformation.objects.filter(parent_id = id)
    photos_other_documents = DispatchIncidentPhotos.objects.filter(parent_id = id)
    certificate = DispatchIncidentDispatcherCertification.objects.filter(parent_id = id)

    responding_address = ParamedicsPhases.objects.filter(parent__parent_id = id, status = 'Respond')
    scene_address = ParamedicsPhases.objects.filter(parent__parent_id = id, status = 'On-Scene')
    facility_address = ParamedicsPhases.objects.filter(parent__parent_id = id, status = 'Arrives-Hospital')
    end_address = ParamedicsPhases.objects.filter(parent__parent_id = id, status = 'Return-Back-To-Base')

    current_site = get_current_site(request)

    context = {
        'incident': incident,
        'crew_vehicle': crew_vehicle,
        'service_notes': service_notes,
        'loc_details': loc_details,
        'photos_other_documents': photos_other_documents,
        'certificate': certificate,
        'odo': odo,
        'patient_info': patient_info,
        'id':id,
        'domain': current_site.domain,

        'responding_address': responding_address,
        'scene_address': scene_address,
        'facility_address': facility_address,
        'end_address': end_address,
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
        paramedic_phases = ParamedicPhasesNotification.objects.filter(is_seen = False).count()
        total_noti_length = panic_noti + membership_noti + h_transfer_noti + renewal_noti + paramedic_phases

    elif request.user.is_staff and not request.user.medic and not request.user.is_superuser:
        renewal_noti = MembershipRenewalNoti.objects.filter(noti_for__user_id = request.user.id,is_seen = False).count()
        h_transfer_noti = HospitalTransferNoti.objects.filter(mark_read_admin = False).count()
        panic_noti = PanicNoti.objects.filter(is_seen = False).count()
        paramedic_phases = ParamedicPhasesNotification.objects.filter(is_seen = False).count()
        total_noti_length = panic_noti + renewal_noti + h_transfer_noti + paramedic_phases

    elif not request.user.is_superuser and request.user.is_staff and  request.user.medic :
        renewal_noti = MembershipRenewalNoti.objects.filter(noti_for__user_id = request.user.id,is_seen = False).count()
        h_transfer_noti = HospitalTransferNoti.objects.filter(mark_read_admin = False).count()
        panic_noti = PanicNoti.objects.filter(is_seen = False).count()
        paramedic_phases = ParamedicPhasesNotification.objects.filter(is_seen = False).count()
        total_noti_length = panic_noti + renewal_noti + h_transfer_noti + paramedic_phases


    elif not request.user.is_staff and not request.user.is_superuser and not request.user.medic:
        renewal_noti = MembershipRenewalNoti.objects.filter(noti_for__user_id = request.user.id,is_seen = False).count()
        h_transfer_noti = HospitalTransferNoti.objects.filter(noti_for__requested_by = request.user,mark_read_user = False).count()
        total_noti_length = renewal_noti + h_transfer_noti


    elif request.user.medic and not request.user.is_staff:
        paramedic_phases = ParamedicPhasesNotification.objects.filter(is_seen = False).count()
        total_noti_length = paramedic_phases


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
    commets = BlogComment.objects.filter(comment_for_id = id).order_by('-id')
    count_comment = len(commets)
    context = {
        'blog': blog,
        'commets': commets,
        'count_comment': count_comment,
    }
    return render(request,'medic/single_blog.html',context)


@login_required
def blog_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        id = request.POST.get('id')
        print(id)
        if comment:
            BlogComment.objects.create(
                comment_for_id = id,
                commenter = request.user,
                comment = comment
            )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
    if request.user.is_suseruser:
        obj.mark_read_admin = True
        obj.save()
    elif not request.user.medic and not request.user.is_staff:
        obj.mark_read_user = True
        obj.save()
    else:
        return HttpResponse('You are not allowed to perform this action')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def form_save(request):
    if request.method == "POST":
        data = request.POST.get('json')
        title = request.POST.get('title')
        FormBuilder.objects.create(title=title,json=data)
        return JsonResponse({'data':"success"})
    return render(request,'medic/form-builder.html')


class FormList(ListView):
    model = FormBuilder
    template_name = 'medic/form-list.html'


class FormListDelete(View):
    def get(self,request):
        id = request.GET.get('id')
        obj = FormBuilder.objects.get(id=id)
        obj.delete()
        return JsonResponse({"deleted":True})


class FormDataEdit(View):
    def get(self,request,pk):
        obj = FormData.objects.get(id=pk)
        json_form = json.loads(obj.form.json)
        context = {
            'json_form':json.dumps(json_form)
        }
        return render(request,'medic/edit/form_data.html',context)


class Form(View):
    def get(self, request,pk):
        get_form = FormBuilder.objects.get(id=pk)
        json_form = json.loads(get_form.json)
        context = {
            'id': json.dumps(pk),
            'json_form':json.dumps(json_form),
        }
        return render(request,'medic/forms.html',context)

@csrf_exempt
def save_form(request):
    if request.method == "POST":
        data = request.POST.get('formdata')
        id = request.POST.get('id')
        FormData.objects.create(form_id=int(id),data=data)
    return JsonResponse({"data":"success"})


class FormDatatable(View):
    def get(self,request,pk):
        data = FormData.objects.filter(form_id=pk)
        context = {
            'data':data
        }
        return render(request,'medic/form-datas.html',context)



class FormDataDetails(DetailView):
    model = FormData
    template_name = 'medic/form-data-details.html'

    def get_context_data(self, **kwargs):
        context = super(FormDataDetails,self).get_context_data(**kwargs)
        data = FormData.objects.get(id=self.kwargs['pk'])
        values = []
        for i in json.loads(data.data):
            values.append(i['value'])
        labels = []
        for i in json.loads(data.form.json):
            labels.append(i['label'])
        context['values'] = json.dumps(values)
        context['labels'] = json.dumps(labels)
        return context



class FormDataDelete(View):
    def get(self,request):
        id = request.GET.get('id')
        obj = FormData.objects.get(id=id)
        obj.delete()
        return JsonResponse({"deleted":True})


class AddCallSign(CreateView):
    model = CallSign
    fields = '__all__'
    template_name = 'medic/add_call_sign.html'
    success_url = reverse_lazy('call_sign')


class CallSignList(ListView):
    model = CallSign
    template_name = 'medic/call_sign.html'


class EditCallSign(UpdateView):
    model = CallSign
    fields = '__all__'
    template_name = 'medic/edit/call_sign.html'
    success_url = reverse_lazy('call_sign')


class EditVehicleInformation(UpdateView):
    model = VehicleProfile
    fields = '__all__'
    template_name = 'medic/edit/vehicle_information.html'
    success_url = reverse_lazy('vehicle_profile_report')


class VehicleInformation(CreateView):
    model = VehicleProfile
    fields = '__all__'
    template_name = "medic/vehicle-information.html"

    def get_context_data(self, **kwargs):
        context = super(VehicleInformation,self).get_context_data(**kwargs)
        context['call_sign'] = CallSign.objects.all()
        return context

    def form_valid(self, form):
        signature = self.request.POST.get('signature')
        format, imgstr = signature.split(';base64,') 
        ext = format.split('/')[-1] 
        signature = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        self.obj = form.save(commit=False)
        self.obj.signature = signature
        self.obj = form.save()
        return redirect('vehicle_category',self.obj.id)


class VehicleCategory(CreateView):
    model = Category
    fields = ['category','description','quantity']
    template_name = 'medic/vehicle_category.html'


    def get_context_data(self, **kwargs):
        context = super(VehicleCategory,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['categories'] = Category.objects.filter(vehicle_profile_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
            self.obj = form.save(commit=False)
            self.obj.vehicle_profile_id = self.kwargs['pk']
            self.obj = form.save()
            return redirect('vehicle_category',self.obj.vehicle_profile_id)


class VehiclePhotograph(CreateView):
    model = DateOfPicture
    fields = ['date_of_image','description','photograph']
    template_name = 'medic/vehicle_photograph.html'

    def get_context_data(self, **kwargs):
        context = super(VehiclePhotograph,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['photographs'] = DateOfPicture.objects.filter(vehicle_profile_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
            self.obj = form.save(commit=False)
            self.obj.vehicle_profile_id = self.kwargs['pk']
            self.obj = form.save()
            return redirect('vehicle_photograph',self.obj.vehicle_profile_id)


class VehicleProfileReport(ListView):
    model = VehicleProfile
    template_name = 'medic/vehicle_profile_report.html'


class VehicleProfileDelete(View):
    def get(self,request):
        id = request.GET.get('id')
        obj = VehicleProfile.objects.get(id=id)
        obj.delete()
        return JsonResponse({"deleted":True})

def categories_pictures(request,pk):
    categories = Category.objects.filter(vehicle_profile_id=pk)
    photographs = DateOfPicture.objects.filter(vehicle_profile_id=pk)
    context = {
        'categories':categories,
        'photographs':photographs
    }
    return render(request,'medic/vehicle_categories&pictures.html',context)



class GetVehicleInformation(View):
    def get(self,request):
        id = request.GET.get('id')
        call_sign = CallSign.objects.get(id=id)
        context = {
            'registration' : call_sign.registration,
            'make':call_sign.make,
            'model':call_sign.model,
            'color':call_sign.color,
            'vin':call_sign.vin,
            'yofr':call_sign.yofr,
            'petrolium':call_sign.petrolium,
            'service_interval':call_sign.service_interval,
            'dot':call_sign.dot,
        }
        return JsonResponse(context)



class DailyPreventiveInsperctions(CreateView):
    model = FleetPreventiveManagement
    fields = ['date','location','call_sign','expiry']
    template_name = 'medic/vehicle_daily_preventive_insperctions.html'

    def form_valid(self, form):
        self.obj = form.save()
        return redirect('vehicle_information', self.obj.id)


class VehicleInformations(View):
    def get(self,request,pk):
        obj = FleetPreventiveManagement.objects.get(id=pk)
        context = {
            'obj':obj
        }
        return render(request,'medic/vehicle_information_fleet.html',context)


class PreinspectionSelections(UpdateView):
    model = FleetPreventiveManagement
    fields = ['current_odo','secondary_battery','secondary_inverter']
    template_name = 'medic/vehicle_preinspection_selections.html'

    def form_valid(self, form):
        self.obj = form.save()
        return redirect('battery_main', self.obj.id)


class FleetTechnicianConfirmations(UpdateView):
    model = FleetPreventiveManagement
    fields = ['notes','signature','certification_date','certification_time']
    template_name = 'medic/vehicle_fleettechnicianconfirmations.html'

    def form_valid(self, form):
        signature = self.request.POST.get('signature')
        format, imgstr = signature.split(';base64,') 
        ext = format.split('/')[-1] 
        signature = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        self.obj = form.save(commit=False)
        self.obj.signature = signature
        self.obj = form.save()
        return redirect('fleet_preventive_management_report')


class BatteryMain(CreateView):
    model = Battery
    fields = ['elements','status','notes','photo']
    template_name = 'medic/vehicle_battery.html'

    def get_context_data(self, **kwargs):
        context = super(BatteryMain,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['battery'] = Battery.objects.filter(fleet_preventive_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.fleet_preventive_id = self.kwargs['pk']
        self.obj = form.save()
        return redirect('battery_main',self.obj.fleet_preventive_id)


class EditBattery(UpdateView):
    model = Battery
    fields = ['elements','status','notes','photo']
    template_name = 'medic/edit/battery.html'
    success_url = reverse_lazy('fleet_preventive_management_report')


class InverterMain(CreateView):
    model = Inverter
    fields = ['elements','status','notes','photo']
    template_name = 'medic/vehicle_inverter.html'

    def get_context_data(self, **kwargs):
        context = super(InverterMain,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['inverter'] = Inverter.objects.filter(fleet_preventive_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.fleet_preventive_id = self.kwargs['pk']
        self.obj = form.save()
        return redirect('inverter_main',self.obj.fleet_preventive_id)


class EditInverter(UpdateView):
    model = Inverter
    fields = ['elements','status','notes','photo']
    template_name = 'medic/edit/inverter.html'
    success_url = reverse_lazy('fleet_preventive_management_report')


class BodyBrandings(CreateView):
    model = BodyBranding
    fields = ['elements','status','notes','photo']
    template_name = 'medic/vehicle_bodybranding.html'

    def get_context_data(self, **kwargs):
        context = super(BodyBrandings,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['bodybranding'] = BodyBranding.objects.filter(fleet_preventive_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.fleet_preventive_id = self.kwargs['pk']
        self.obj = form.save()
        return redirect('bodybranding',self.obj.fleet_preventive_id)


class EditBodyBranding(UpdateView):
    model = BodyBranding
    fields = ['elements','status','notes','photo']
    template_name = 'medic/edit/body_branding.html'
    success_url = reverse_lazy('fleet_preventive_management_report')


class FluidInspections(CreateView):
    model = FluidInspection
    fields = ['elements','status','notes','photo']
    template_name = 'medic/vehicle_fluidinspection.html'

    def get_context_data(self, **kwargs):
        context = super(FluidInspections,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['fluidinspection'] = FluidInspection.objects.filter(fleet_preventive_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.fleet_preventive_id = self.kwargs['pk']
        self.obj = form.save()
        return redirect('fluid_inspection',self.obj.fleet_preventive_id)


class EditFluidInspections(UpdateView):
    model = FluidInspection
    fields = ['elements','status','notes','photo']
    template_name = 'medic/edit/fluid_inspection.html'
    success_url = reverse_lazy('fleet_preventive_management_report')


class InternalSystems(CreateView):
    model = InternalSystem
    fields = ['elements','status','notes','photo']
    template_name = 'medic/vehicle_internalsystems.html'

    def get_context_data(self, **kwargs):
        context = super(InternalSystems,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['internalsystems'] = InternalSystem.objects.filter(fleet_preventive_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.fleet_preventive_id = self.kwargs['pk']
        self.obj = form.save()
        return redirect('internal_systems',self.obj.fleet_preventive_id)


class EditInternalSystems(UpdateView):
    model = InternalSystem
    fields = ['elements','status','notes','photo']
    template_name = 'medic/edit/internal_system.html'
    success_url = reverse_lazy('fleet_preventive_management_report')


class Lights(CreateView):
    model = Light
    fields = ['elements','status','notes','photo']
    template_name = 'medic/vehicle_lights.html'

    def get_context_data(self, **kwargs):
        context = super(Lights,self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        context['light'] = Light.objects.filter(fleet_preventive_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.fleet_preventive_id = self.kwargs['pk']
        self.obj = form.save()
        return redirect('technician',self.obj.fleet_preventive_id)


class EditLights(UpdateView):
    model = Light
    fields = ['elements','status','notes','photo']
    template_name = 'medic/edit/light.html'
    success_url = reverse_lazy('fleet_preventive_management_report')


class FleetPreventiveManagementReport(ListView):
    model = FleetPreventiveManagement
    template_name = 'medic/vehicle_fleetPreventive_management_report.html'


class FleetManagementOtherData(View):
    def get(self,request,pk):
        battery = Battery.objects.filter(fleet_preventive_id = pk)
        inverter = Inverter.objects.filter(fleet_preventive_id = pk)
        bodybranding = BodyBranding.objects.filter(fleet_preventive_id = pk)
        fluidinspection = FluidInspection.objects.filter(fleet_preventive_id = pk)
        internalsystem = InternalSystem.objects.filter(fleet_preventive_id = pk)
        light = Light.objects.filter(fleet_preventive_id = pk)
        context = {
            'battery':battery,
            'inverter':inverter,
            'bodybranding':bodybranding,
            'fluidinspection':fluidinspection,
            'internalsystem':internalsystem,
            'light':light
        }
        return render(request,'medic/vehicle_fleetmanagementotherdata.html',context)


class EditFleetManagement(UpdateView):
    model = FleetPreventiveManagement
    fields = '__all__'
    template_name = 'medic/edit/fleet_management.html'
    success_url = reverse_lazy('fleet_preventive_management_report')

 
class FleetManagementDelete(View):
    def get(self,request):
        id = request.GET.get('id')
        obj = FleetPreventiveManagement.objects.get(id=id)
        obj.delete()
        return JsonResponse({"deleted":True})


# not done
def electronic_cash_pdf(request,id):
    electronic_cash = Electric_Cash_Receipt.objects.get(id = id)
    electronic_invoice = Electric_Cash_Receipt_Invoice.objects.filter(invo_for_id = id)
    invoice_summary = ElectricInvoiceSummary.objects.filter(summary_for_id = id)

    current_site = get_current_site(request)
    context = {
        'electronic_cash': electronic_cash,
        'electronic_invoice': electronic_invoice,
        'invoice_summary': invoice_summary,
        'id':id,
        'domain': current_site.domain,
    }
    
    template = get_template('medic/electronic_cash_pdf.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=electronic_cash_invoice_report.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def purchaseOrder_pdf(request,id):
    order = PurchaseOrder.objects.get(id = id)
    vehicle_maintenance = VehicleMaintenance.objects.filter(order_id = id)
    vehicle_maintenance_total = VehicleMaintenanceTotal.objects.filter(order_for_id = id)
    product = Product.objects.filter(order_id = id)
    p_totals = Product_totals.objects.filter(order_for_id = id)
    services = Services_Training.objects.filter(service_for_id = id)
    s_totals = Service_Totals.objects.filter(service_for_id = id)
    terms = TermsAndConditions.objects.filter(terms_for_id = id)
    approvals = PurchaseApproval.objects.filter(approval_for_id = id)
    p_o_rec = PO_Items_Received.objects.filter(received_for_id = id)
    quality = Quality_Control_Inspection.objects.filter(quality_for_id = id)

    current_site = get_current_site(request)
    context = {
        'order': order,
        'vehicle_maintenance': vehicle_maintenance,
        'vehicle_maintenance_total': vehicle_maintenance_total,
        'product': product,
        'p_totals': p_totals,
        'services': services,
        's_totals': s_totals,
        'terms': terms,
        'p_o_rec': p_o_rec,
        'quality': quality,
        'approvals': approvals,
        'id':id,
        'domain': current_site.domain,
    }
    
    template = get_template('medic/purchase_order_pdf.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=order_invoice_report.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def quotation_emergency_operations_pdf(request,id):
    client = ProspectiveClient.objects.get(id = id)
    service_details = ServiceDetails.objects.filter(parent_id = id)
    em_operations = EmergencyOperations.objects.filter(parent_id = id)
    total_call_costing = TotalCallCosting.objects.filter(parent_id = id)

    current_site = get_current_site(request)
    context = {
        'client': client,
        'service_details': service_details,
        'em_operations': em_operations,
        'total_call_costing': total_call_costing,
        'id':id,
        'domain': current_site.domain,
    }
    
    template = get_template('medic/quotation_emergency_operation_pdf.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=quotation_emergency_operation.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def quotation_events_sports_pdf(request,id):
    client = EventsProspectiveClient.objects.get(id = id)
    service_details = EventsServiceDetails.objects.filter(parent_id = id)
    particulars = EventSportParticulars.objects.filter(parent_id = id)
    total_costing = TotalEventSportCosting.objects.filter(parent_id = id)
    inclusion = EventServiceInclusion.objects.filter(parent_id = id)
    exclusion = EventServiceExclusion.objects.filter(parent_id = id)

    current_site = get_current_site(request)
    context = {
        'client': client,
        'service_details': service_details,
        'particulars': particulars,
        'total_costing': total_costing,
        'inclusion': inclusion,
        'exclusion': exclusion,
        'id':id,
        'domain': current_site.domain,
    }
    
    template = get_template('medic/quotation_events_sports_pdf.html')
    pdf = render_to_pdf(template, context)

    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=quotation_sport_event.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


class GenerateFormBuilderDataPdf(View):
    def get(self, request, *args, **kwargs):
        data = FormData.objects.get(id=self.kwargs['pk'])
        values = []
        for i in json.loads(data.data):
            values.append(i['value'])
        labels = []
        for i in json.loads(data.form.json):
            labels.append(i['label'])
        context = {
            'values':values,
            'labels':labels
        }
        get_pdf = pdf('medic/pdf/form_builder_pdf.html',context)
        return HttpResponse(get_pdf, content_type='application/pdf')


# delete view for finance part and emergency dispatch incident part
@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_electronic_cash_receipt(request,id):
    obj = get_object_or_404(Electric_Cash_Receipt, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_emergency_dispatch_incident_report(request,id):
    obj = get_object_or_404(AmbulanceModel, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_expense_reimbursement_record_report(request,id):
    obj = get_object_or_404(Expense_Reimbursement_Record, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_purchase_order_report(request,id):
    obj = get_object_or_404(PurchaseOrder, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_quotation_emergency_operation_report(request,id):
    obj = get_object_or_404(ProspectiveClient, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_quotation_event_sport_report(request,id):
    obj = get_object_or_404(EventsProspectiveClient, id=id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# ends
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def dispatch_emergency_incident_submissions(request):
    dispatch_emergency_incidents = AmbulanceModel.objects.all()
    context = {
        'incidents': dispatch_emergency_incidents,
    }
    return render(request,'medic/dispatch_emergency_incident_submissions.html',context)

@login_required
def edit_emergency_dispatch_incident_report_call_intake_phase(request,id):
    obj = get_object_or_404(AmbulanceModel, id=id)
    try:
        panic = Panic.objects.get(id = obj.panic.id)
    except:
        panic = None

    form = EmergencyMedDisIncidentReportForm(instance = obj)
    if request.method == 'POST':
        form = EmergencyMedDisIncidentReportForm(request.POST,instance=obj)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.panic = panic
            instance.save()
            return redirect('dispatch_incident_crew_and_vehicle', id)
    context = {
        'form': form,
        'id': id,
    }
    return render(request,'medic/edit/edit_emergency_dispatch_incident_report_call_intake_phase.html',context)


@login_required
def edit_dispatch_incident_crew_and_vehicle(request,id):
    user = User.objects.filter(medic = True)

    obj = get_object_or_404(DispatchIncidentCrewAndVehicle, id=id)
    parent = get_object_or_404(AmbulanceModel, id = obj.parent.id)
    assigned_units = DispatchIncidentCrewAndVehicle.objects.filter(parent = parent)

    form = DispatchIncidentCrewAndVehicleForm(instance = obj)
    # senior_form = SeniorForm()
    # assist_1_form = Assist01Form()
    # assist_2_form = Assist02Form()
    if request.method == 'POST':
        # senior_form = SeniorForm(request.POST)
        # assist_1_form = Assist01Form(request.POST)
        # assist_2_form = Assist02Form(request.POST)


        # if senior_form.is_valid():
        #     senior_form.save()
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # if assist_1_form.is_valid():
        #     assist_1_form.save()
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # if assist_2_form.is_valid():
        #     assist_2_form.save()
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        main_form = request.POST.get('main_form')
        if main_form is not None:
            form = DispatchIncidentCrewAndVehicleForm(request.POST,instance=obj)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.parent = parent
                instance.save()
                return redirect('add_another_dispatch_incident_crew_and_vehicle', id = parent.id)

    context = {
        'user': user,
        'form': form,
        # 'senior_form': senior_form,
        # 'assist_1_form': assist_1_form,
        # 'assist_2_form': assist_2_form,
        'parent': parent,
        'data': obj,
        'assigned_units': assigned_units,
        'id': id,
    }
    return render(request,'medic/edit/edit_dispatch_incident_crew_and_vehicle.html',context)


@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def create_unit(request):
    form = CreateUnitForm()
    if request.method == 'POST':
        uni_name = request.POST.get('uni_name')
        vehicle_type = request.POST.get('vehicle_type')
        max_crew = request.POST.get('max_crew')
        reg = request.POST.get('reg')
        if UnitNames.objects.filter(uni_name__iexact = uni_name).exists():
            messages.warning(request,f'A unit with {uni_name} already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        form = CreateUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paramedics_with_assigned_unit_list')
    context = {
        'form': form,
    }
    return render(request,'medic/create_unit.html',context)



@login_required
@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def assign_paramedics_to_units(request):
    form = AssignUnitFullFormWithParamedicsAdd()
    if request.method == 'POST':
        form = AssignUnitFullFormWithParamedicsAdd(request.POST)
        # getting the id of unit model
        unit = request.POST.get('uni_name')

        unit_model = UnitNames.objects.get(id = unit )
        check_max_crew = AssignUnitCreateWithParamedics.objects.filter(uni_name = unit).count()
        print(check_max_crew,unit_model.max_crew)
        if check_max_crew >= unit_model.max_crew:
            messages.warning(request,f"""This Vehicle/Unit maximun crew is {unit_model.max_crew} and already two crew members are assigned with this vehicle.""")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if form.is_valid():
            assigned, created = AssignUnitCreateWithParamedics.objects.get_or_create(
                uni_name = form.cleaned_data['uni_name'],
                paramedics = form.cleaned_data['paramedics']
            )
            if created:
                messages.success(request,'Paramedic assigned')
                return redirect('assign_paramedics_to_units')
            if assigned:
                messages.success(request,'Paramedic already assigned to this unit')
                return redirect('assign_paramedics_to_units')
            
    context = {
        'form': form,
    }
    return render(request,'medic/assign_paramedics_to_units.html',context)


@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def paramedics_with_assigned_unit_list(request):
    # only units
    planned = UnitNames.objects.filter(vehicle_type = 'Planned Patient Transport')
    am = UnitNames.objects.filter(vehicle_type = 'Ambulance')
    response = UnitNames.objects.filter(vehicle_type = 'Response Vehicle')

    # with paramedics
    planed_units = AssignUnitCreateWithParamedics.objects.filter(uni_name__vehicle_type = 'Planned Patient Transport')
    am_units = AssignUnitCreateWithParamedics.objects.filter(uni_name__vehicle_type = 'Ambulance')
    response_units = AssignUnitCreateWithParamedics.objects.filter(uni_name__vehicle_type = 'Response Vehicle')
    
    context = {
        'planned': planned,
        'am': am,
        'response': response,

        'planed_units': planed_units,
        'am_units': am_units,
        'response_units': response_units,
    }
    return render(request,'medic/paramedics_with_assigned_unit_list.html',context)

@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def delete_paramedics_with_assigned_unit_list(request,id):
    obj = get_object_or_404(AssignUnitCreateWithParamedics, id=id)
    medic = obj.paramedics.username
    obj.delete()
    messages.success(request,f'{medic} has been deleted from this unit')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def show_medic_via_selected_unit(request):
    data = []
    if request.method == 'POST':
        frontend_data = request.POST
        for k,v in frontend_data.items():
            if k == 'val':
                id = v
        medics = AssignUnitCreateWithParamedics.objects.filter(
            uni_name_id = id
        )

        if medics:
            for i in medics:
                prefetch = {
                    'found': True,
                    'username': str(i.paramedics.first_name) + ' ' + str(i.paramedics.last_name),
                    'contact': i.paramedics.contact,
                    'user_id': i.paramedics.id,
                    'unit_reg': i.uni_name.reg,
                }
                data.append(prefetch)
        else:
            prefetch = {
                'found': False,
                'msg': 'No paramedic assigned with this unit'
            }
            data.append(prefetch)
        return JsonResponse(data,safe=False)
    

@csrf_exempt
def auto_fill_panic_data_to_call_intake_2nd_phase(request):
    if request.method == 'POST':
        data = request.POST
        for k,v in data.items():
            if k == 'panic_id':
                panic_id = v
        try:
            panic = get_object_or_404(Panic, id = panic_id)
            response = {
                'found': True,
                'panic_sender': panic.panic_sender.first_name,
                'contact': panic.emergency_contact,
                'panic_sender_id': panic.panic_sender.id,
                'reason': panic.reason,
                'for_whome': panic.for_whome,
                'place': panic.place,
                'panic_creation_time': panic.timestamp,
            }
            print(panic.timestamp)
        except:
            response = {
                'found': False,
            }
        return JsonResponse(response,safe=False)


# @login_required
# @user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
# def case_note_create_for_dispatch_emergency_incident(request,id):
#     dispatch_emergency_incident_parent_form_that_is_ambulance_model = get_object_or_404(AmbulanceModel,id = id)
#     if request.method == 'POST':
#         #return redirect('case_notes')
#         case_note = request.POST.get('case_note')
#         if case_note:
#             note = CaseNote.objects.create(
#                 creator = request.user,
#                 case_dispatch_form = dispatch_emergency_incident_parent_form_that_is_ambulance_model,
#                 case_no = case_number(),
#                 case_note = case_note,
#             )
#     context = {
#         'id': id,
#         'dispatch_emergency_incident_parent_form_that_is_ambulance_model': dispatch_emergency_incident_parent_form_that_is_ambulance_model,
#         'note': note,
#     }
#     return render(request, 'medic/case_note_form_for_dispatch_emergency_incident.html',context)



@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def paramedic_phases(request,id):
    phases = ParamedicsPhases.objects.filter(parent__parent_id = id)
    context = {
        'phases': phases
    }
    return render(request,'medic/paramedic_phases.html',context)


@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def emergency_incident_dispatch_individual_parts_medium(request,id):
    call_intake_phase = AmbulanceModel.objects.get(id = id)
    crews = call_intake_phase.dispatchincidentcrewandvehicle_set.all()
    assigned_medics = call_intake_phase.assignedparamedicsafterdispatchincidentcrewandvehicle_set.all()
    travel_details = ParamedicsPhases.objects.filter(parent__parent_id = id)
    service_notes = call_intake_phase.dispatchincidentservicenotes_set.all()
    patient_info = DispatchIncidentPatientInformation.objects.filter(parent = call_intake_phase)
    photos = DispatchIncidentPhotos.objects.filter(parent = call_intake_phase)
    certification = DispatchIncidentDispatcherCertification.objects.filter(parent = call_intake_phase)
    context = {
        'id': id,
        'call_intake_phase': call_intake_phase,
        'crews': crews,
        'assigned_medics': assigned_medics,
        'travel_details': travel_details,
        'service_notes': service_notes,
        'patient_info': patient_info,
        'photos': photos,
        'certification': certification,

    }
    return render(request,'medic/emergency_incident_dispatch_individual_parts_medium.html',context)

@login_required
def paramedic_phase_noti(request):
    if request.user.is_staff or request.user.medic or request.user.is_superuser:
        data = []
        noti = ParamedicPhasesNotification.objects.filter(is_seen = False,noti_for__parent__parent__closed = False).order_by('-id')
        for i in noti:
            prefetch = {
                'run_id': i.noti_for.parent.parent.run_id,
                'incident_id': i.noti_for.parent.parent.id,
                'noti_id': i.id,
                'noti_text': i.text,
                'time': i.created,
            }
            data.append(prefetch)
        return JsonResponse(data,safe=False)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def mark_seen_paramedic_phase_noti(request,id):
    noti = ParamedicPhasesNotification.objects.get(id = id)
    noti.is_seen = True
    noti.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def close_dispatch_emergency_incident(request,id):
    incident = AmbulanceModel.objects.get(id = id)
    incident.closed = True
    incident.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GroupChatView(TemplateView):
    template_name = 'medic/group_chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['am_model_instance'] = AmbulanceModel.objects.get(id = self.kwargs['id'])
        context['chat_users'] = AssignedParamedicsAfterDispatchIncidentCrewAndVehicle.objects.filter(parent_id = self.kwargs['id'])
        context['inbox'] = GroupChat.objects.filter(am_model_id = self.kwargs['id'])
        # ambulance model id
        context['am_id'] = self.kwargs['id']
        return context

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('img')
        attachment = request.FILES.get('attachment')
        if images:
            for img in images:
                GroupChat.objects.create(
                    am_model_id = self.kwargs['id'],
                    sender = self.request.user,
                    img = img,
                )
        if attachment:
                GroupChat.objects.create(
                    am_model_id = self.kwargs['id'],
                    sender = request.user,
                    attachment = attachment,
                )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
@login_required
def delete_dispatch_sms(request,id):
    inbox = GroupChat.objects.filter(am_model_id = id)
    for i in inbox:
        i.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))