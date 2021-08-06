from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from pytz import utc
from .forms import *
from .serializer import *
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
import json
import requests
from rest_framework.views import APIView
from django.contrib import messages
from Accounts.decorators import user_passes_test, has_perm_admin, has_perm_admin_dispatch, has_perm_user, \
    has_perm_dispatch, REDIRECT_FIELD_NAME
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

today = datetime.today()
week = datetime.today().date() - timedelta(days=7)
month = datetime.today().date() - timedelta(days=30)


# Create your views here.
def add_member(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def getmembership(request):
    packages = Package.objects.all()
    context = {
        'packages': packages,
    }
    return render(request, 'Accounting/get_membership.html',context)


@login_required
def payment(request,id):
    package = Package.objects.filter(id = id)

    context = {
        'package': package,
        'id': id,
    }
    return render(request,'Accounting/payment.html',context)


@login_required
@csrf_exempt
def payment_backend(request):
    token = ''
    package_id = ''
    package_price_in_cents = ''
    user = ''
    customer_contact = ''

    data = request.POST
    for k,v in data.items():
        if k == 'token':
            token = v
            print('token:',token)
        if k == 'package_id':
            package_id = v
            print('package_id:',package_id)
        if k == 'package_price_in_cents':
            package_price_in_cents = v
            print('package_price_in_cents:',package_price_in_cents)
        if k == 'user':
            user = v
            print('user:',user)
        if k == 'customer_contact':
            customer_contact = v
            print(customer_contact)

    # Anonymous test key. Replace with your key.
    SECRET_KEY = 'sk_test_960bfde0VBrLlpK098e4ffeb53e1'
    response = requests.post(
        'https://online.yoco.com/v1/charges/',
        headers={
            'X-Auth-Secret-Key': SECRET_KEY,
        },
        json={
            'token': token,
            'amountInCents': package_price_in_cents,
            'currency': 'ZAR',
            'metadata': {'user_id': request.user.id, 'package_id': package_id, 'customer_contact': customer_contact}
        },
        )

    package = Package.objects.get(id = package_id)
    package_membership_duration = package.package_membership_duration

    membership = MembershipModel.objects.create(user_id = user, package_id = package_id, token = token)
    membership.membership_end = membership.membership_date + timedelta(days = int(package_membership_duration))
    membership.save()

    user = User.objects.get(id = user)
    membership_end = membership.membership_end
    if membership_end.date()  == datetime.now().date():
        print('membership expired')
        user.has_membership = False
        user.renew_membership = True
        user.save()
    elif membership_end.date() > datetime.now().date():
        print('membership granted')
        user.has_membership = True
        user.renew_membership = False
        user.save()
    else:
        user.has_membership = False
        user.renew_membership = True
        user.save()
    return render(request,'Accounting/membership_purchased.html')


@login_required
def package_purchased(request):
    membership = MembershipModel.objects.filter(user = request.user).order_by('-id')
    context = {
        'membership': membership,
        'has_membership': User.objects.filter(id = request.user.id, has_membership = True).exists()
    }
    return render(request,'Accounting/membership_purchased.html', context)


@login_required
def viewing_membership_details_individual(request,id):
    mebership_details = MembershipModel.objects.filter(id = id)
    context = {
        'mebership_details': mebership_details,
    }
    return render(request,'Accounting/individual_membership_details.html',context)


@login_required
def members(request):
    memberships_holders = MembershipModel.objects.filter(membership_end__date__gt = datetime.today().date()).order_by('-id')
    context = {
        'memberships_holders': memberships_holders,
    }
    return render(request, 'Accounting/members.html',context)


class ScheduleTrip(LoginRequiredMixin, View):

    def get(self, request):
        form = ScheduleModelForm
        return render(request, 'Accounting/shcedule_trip.html', {'form': form})

    def post(self, request):
        form = ScheduleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trip_schedules')

        return render(request, 'Accounting/shcedule_trip.html', {'form': form})


class TripSchedules(LoginRequiredMixin, View):
    def get(self, request):
        title = "Schedule Requests"
        daily = ''
        weekly = ''
        monthly = ''
        if self.request.user.is_superuser:
            daily = ScheduleModel.objects.filter(
                created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                created_on__gte=month).order_by('-id')
        elif not self.request.user.is_staff and not self.request.user.is_superuser:
            user_id = request.user.id
            daily = ScheduleModel.objects.filter(
                user=user_id, created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                user=user_id, created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                user=user_id, created_on__gte=month).order_by('-id')

        context = {
            'title': title,
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly
        }
        return render(request, 'Accounting/trip_schedules.html', context)


class DeleteSchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(ScheduleModel, pk=pk)
            if data:
                data.delete()
                return redirect('trip_schedules')
            return redirect('trip_schedules')
        else:
            return render(request, 'accounts/forbidden.html')


class UpdateSchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(ScheduleModel, pk=pk)
        if request.user.is_superuser or request.user.id == data.user.id:
            form = ScheduleModelForm(instance=data)
            return render(request, 'Accounting/update_scedule.html', {'form': form, 'data': data})
        else:
            return render(request, 'accounts/forbidden.html')

    def post(self, request, pk):
        data = get_object_or_404(ScheduleModel, pk=pk)
        if request.user.is_superuser or request.user.id == data.user.id:
            if request.method == 'POST':
                form = ScheduleModelForm(request.POST, instance=data)
                if form.is_valid():
                    form.save()
                    return redirect('trip_schedules')
                return render(request, 'Accounting/update_scedule.html', {'form': form, 'data': data})
        else:
            return render(request, 'accounts/forbidden.html')


@login_required
def ScheduleDetails(request, pk):
    data = get_object_or_404(ScheduleModel, pk=pk)
    task = False
    task_data = ''
    try:
        if request.user.is_staff:
            task_data = TaskModel.objects.filter(
                task_type='sch', scheduled_task=pk)
            for i in task_data:
                task_data = i.task_desc
            task = True
    except:
        pass
    context = {
        'object': data,
        'task': task,
        'task_data': task_data
    }
    return render(request, 'Accounting/sechdule_details.html', context)


def schedule_status_change(request, pk):
    if request.user.is_staff:
        TaskModel.objects.filter(
            task_type='sch', scheduled_task=pk).update(status='Completed')
        schedule = get_object_or_404(ScheduleModel, pk=pk)
        schedule.status = 'Completed'
        schedule.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('forbidden')


class TrackSchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(ScheduleModel, pk=pk)
        return render(request, 'Accounting/track_schedule.html', {'data': data})


class AcceptedSchedule(LoginRequiredMixin, View):
    def get(self, request):
        title = "Accepted Schedule"
        daily = ''
        weekly = ''
        monthly = ''

        if self.request.user.is_superuser:
            daily = ScheduleModel.objects.filter(
                status='Approved', created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                status='Approved', created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                status='Approved', created_on__gte=month).order_by('-id')
        elif self.request.user.is_staff:
            user_id = request.user.id
            daily = ScheduleModel.objects.filter(
                dispatch=user_id, status='Approved', created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                dispatch=user_id, status='Approved', created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                dispatch=user_id, status='Approved', created_on__gte=month).order_by('-id')
        else:
            user_id = request.user.id
            daily = ScheduleModel.objects.filter(
                user=user_id, status='Approved', created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                user=user_id, status='Approved', created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                user=user_id, status='Approved', created_on__gte=month).order_by('-id')
        context = {
            'title': title,
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly
        }
        return render(request, 'Accounting/trip_schedules.html', context)


class CompletedSchedule(LoginRequiredMixin, View):
    def get(self, request):
        title = "Completed Schedule"
        if self.request.user.is_superuser:
            daily = ScheduleModel.objects.filter(
                status='Completed', created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                status='Completed', created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                status='Completed', created_on__gte=month).order_by('-id')
        elif self.request.user.is_staff:
            user_id = request.user.id
            daily = ScheduleModel.objects.filter(
                dispatch=user_id, status='Completed', created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                dispatch=user_id, status='Completed', created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                dispatch=user_id, status='Completed', created_on__gte=month).order_by('-id')

        elif self.request.user.is_staff:
            user_id = request.user.id
            daily = ScheduleModel.objects.filter(
                user=user_id, status='Completed', created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                user=user_id, status='Completed', created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                user=user_id, status='Completed', created_on__gte=month).order_by('-id')

        context = {
            'title': title,
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly
        }
        return render(request, 'Accounting/trip_schedules.html', context)


@login_required
def task_create(request):
    if request.user.is_superuser:
        form = TaskModelForm()
        dispatch = User.objects.filter(is_staff=True, is_superuser=False)
        schedule = ScheduleModel.objects.filter(assigned=False)
        ambulance = AmbulanceModel.objects.filter(assigned=False)
        hospital = HospitalTransferModel.objects.filter(assigned=False)
        panic = Panic.objects.filter(assigned=False)
        if request.method == 'POST':
            form = TaskModelForm(request.POST)
            x = request.POST.get('task_type')
            at = request.POST.get('ambulance_task')
            st = request.POST.get('scheduled_task')
            pt = request.POST.get('panic_task')
            ht = request.POST.get('hos_tra')
            if form.is_valid():
                form.save(commit=False)
                if x == 'sch':
                    data = get_object_or_404(ScheduleModel, pk=st)
                    data.assigned = True
                    data.status = 'Approved'
                    data.save()
                elif x == 'ambr':
                    data = get_object_or_404(AmbulanceModel, pk=at)
                    data.assigned = True
                    data.save()
                elif x == 'HT':
                    data = get_object_or_404(HospitalTransferModel, pk=ht)
                    data.assigned = True
                    data.save()
                else:
                    data = get_object_or_404(Panic, pk=pt)
                    data.assigned = True
                    data.save()
                form.save()
                return redirect('task_list')

        context = {
            'form': form,
            'dispatch': dispatch,
            'schedule': schedule,
            'ambulance': ambulance,
            'panic': panic,
            'hospital': hospital,
        }
        return render(request, 'Accounting/taskcreate.html', context)
    else:
        return render(request, 'accounts/forbidden.html')



class TasksList(LoginRequiredMixin, View):
    def get(self, request):
        if self.request.user.is_superuser:
            daily = TaskModel.objects.filter(
                created_on__gte=today.date()).order_by('-id')
            weekly = TaskModel.objects.filter(
                created_on__gte=week).order_by('-id')
            monthly = TaskModel.objects.filter(
                created_on__gte=month).order_by('-id')
        elif self.request.user.is_staff:
            user_id = request.user.id
            daily = TaskModel.objects.filter(
                dispatch=user_id, created_on__gte=today.date()).order_by('-id')
            weekly = TaskModel.objects.filter(
                dispatch=user_id, created_on__gte=week).order_by('-id')
            monthly = TaskModel.objects.filter(
                dispatch=user_id, created_on__gte=month).order_by('-id')

        context = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly
        }
        return render(request, 'Accounting/task_list.html', context)


class UpdateTask(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(TaskModel, pk=pk)
            form = TaskModelForm(instance=data)
            context = {
                'form': form,
                'data': data
            }
            return render(request, 'Accounting/taskupdate.html', context)
        else:
            return render(request, 'accounts/forbidden.html')

    def post(self, request, pk):
        if request.user.is_superuser:
            if request.method == 'POST':
                data = get_object_or_404(TaskModel, pk=pk)
                form = TaskModelForm(request.POST, instance=data)
                if form.is_valid():
                    form.save()
                    return redirect('task_list')
        else:
            return render(request, 'accounts/forbidden.html')


class DeleteTask(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(TaskModel, pk=pk)
            if data:
                data.delete()
                return redirect('task_list')
        else:
            return render(request, 'accounts/forbidden.html')


@login_required
def task_detail(request, pk):
    data = get_object_or_404(TaskModel, pk=pk)
    return render(request, 'Accounting/task_detail.html', {'object': data})


class TransferTask(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            form = TransferTaskForm()
            data = get_object_or_404(TaskModel, pk=pk)
            user_id = data.dispatch.id
            dispatches = User.objects.filter(
                ~Q(pk=user_id), is_staff=True, is_superuser=False)
            context = {
                'form': form,
                'pk': pk,
                'data': data,
                'dispatches': dispatches
            }
            return render(request, 'Accounting/task_transfer.html', context)
        else:
            return render(request, 'accounts/forbidden.html')

    def post(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            form = TransferTaskForm(request.POST)
            data = get_object_or_404(TaskModel, pk=pk)
            user_id = data.dispatch.id
            dispatches = User.objects.filter(
                ~Q(is_superuser=True), ~Q(pk=user_id), is_staff=True)
            if form.is_valid():
                data.status = 'Transferred'
                data.save()
                form.save()
                return redirect('task_list')
            context = {
                'form': form,
                'pk': pk,
                'data': data,
                'dispatches': dispatches
            }
            return render(request, 'Accounting/task_transfer.html', context)
        else:
            return render(request, 'accounts/forbidden.html')


class TransferredTasks(LoginRequiredMixin, View):
    def get(self, request):
        daily = ''
        weekly = ''
        monthly = ''
        if request.user.is_superuser:
            daily = TaskTransferModel.objects.filter(
                created_on__gte=today.date())
            weekly = TaskTransferModel.objects.filter(created_on__gte=week)
            monthly = TaskTransferModel.objects.filter(created_on__gte=month)
        if request.user.is_staff and not request.user.is_superuser:
            user_id = request.user.id
            print('ok')
            daily = TaskTransferModel.objects.filter(Q(transferred_by_id=user_id) | Q(
                transfer_to_id=user_id), created_on__gte=today.date())
            weekly = TaskTransferModel.objects.filter(
                Q(transferred_by_id=user_id) | Q(transfer_to_id=user_id), created_on__gte=week)
            monthly = TaskTransferModel.objects.filter(
                Q(transferred_by_id=user_id) | Q(transfer_to_id=user_id), created_on__gte=month)
        context = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly
        }
        context
        return render(request, 'Accounting/transfered_tasks.html', context)


@login_required
def add_paystub(request):
    if request.user.is_superuser:
        form = PaystubForm()
        dispatch = User.objects.filter(is_staff=True, is_superuser=False)
        if request.method == 'POST':
            form = PaystubForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('paystub_report')
        context = {
            'form': form,
            'dispatch': dispatch
        }
        return render(request, 'Accounting/add_paystub.html', context)
    else:
        return redirect('forbidden')

@login_required
def paystub_report(request):
    if request.user.is_superuser:
        daily = PaystubModel.objects.filter(created_on__gte=today.date())
        weekly = PaystubModel.objects.filter(created_on__gte=week)
        monthly = PaystubModel.objects.filter(created_on__gte=month)
    else:
        user_id = request.user.id
        daily = PaystubModel.objects.filter(
            dispatch=user_id, created_on__gte=today.date())
        weekly = PaystubModel.objects.filter(
            dispatch=user_id, created_on__gte=week)
        monthly = PaystubModel.objects.filter(
            dispatch=user_id, created_on__gte=month)
    context = {
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly
    }
    return render(request, 'Accounting/paystub_report.html', context)


@login_required
def update_paystub_report(request, pk):
    if request.user.is_superuser:
        data = get_object_or_404(PaystubModel, pk=pk)
        data_user = data.dispatch.id
        dispatch = User.objects.filter(
            ~Q(id=data_user), is_staff=True, is_superuser=False)
        form = PaystubForm(instance=data)
        if request.method == 'POST':
            form = PaystubForm(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                return redirect('paystub_report')
        context = {
            'form': form,
            'dispatch': dispatch,
            'data': data
        }
        return render(request, 'Accounting/update_paystub.html', context)
    else:
        return redirect('forbidden')


@login_required
def delete_paystub(request, pk):
    if request.user.is_superuser:
        data = get_object_or_404(PaystubModel, pk=pk)
        data.delete()
        return redirect('paystub_report')


@login_required
def stock_request(request):
    form = StockRequestForm()
    if request.method == 'POST':
        form = StockRequestForm(request.POST, request.FILES)
        if form.is_valid():
            rc = form.cleaned_data['receiver']
            sb = form.cleaned_data['subject']
            mb = form.cleaned_data['message_body']
            at = request.FILES.getlist('attachment')
            try:
                mail = EmailMessage(sb, mb, settings.EMAIL_HOST_USER, [rc])
                for f in at:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                form_obj = form.save(commit=False)
                form_obj.requested = True
                form_obj.save()
                return redirect('stock_requests')
            except:
                return HttpResponse('Something Went Wrong')
    return render(request, 'Accounting/stock_req.html', {'form': form})


@login_required
def cancel_stock_request(request):
    form = StockRequestForm()
    rcv = StockRequestModel.objects.filter(
        requested=True).values('receiver').distinct()
    if request.method == 'POST':
        form = StockRequestForm(request.POST, request.FILES)
        if form.is_valid():
            rc = form.cleaned_data['receiver']
            sb = form.cleaned_data['subject']
            mb = form.cleaned_data['message_body']
            at = request.FILES.getlist('attachment')
            try:
                mail = EmailMessage(sb, mb, settings.EMAIL_HOST_USER, [rc])
                for f in at:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                form_obj = form.save(commit=False)
                form_obj.cancel = True
                form_obj.save()
                return redirect('stock_requests')

            except:
                return HttpResponse('Something Went Wrong')
    return render(request, 'Accounting/cancel_stock_req.html', {'form': form, 'rcv': rcv})


class StockRequest(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            daily = StockRequestModel.objects.filter(
                created_on__gte=today.date()).order_by('-id')
            weekly = StockRequestModel.objects.filter(
                created_on__gte=week).order_by('-id')
            monthly = StockRequestModel.objects.filter(
                created_on__gte=month).order_by('-id')
            context = {
                'daily': daily,
                'weekly': weekly,
                'monthly': monthly
            }
            return render(request, 'Accounting/stock_requests.html', context)
        else:
            return render(request, 'accounts/forbidden.html')


class StockRequestDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(StockRequestModel, pk=pk)
            return render(request, 'Accounting/stc_req_detail.html', {'data': data})
        else:
            return render(request, 'accounts/forbidden.html')


class DeleteStock(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(StockRequestModel, pk=pk)
            data.delete()
            return redirect('stock_requests')


@login_required
def packages(request):
    packages = Package.objects.all()
    context = {
        'packages': packages,
    }
    return render(request, 'Accounting/packages.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def add_package(request):
    form = PackageForm()
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package Created')
            return redirect('packages')
    context = {
        'form': form,
    }
    return render(request, 'Accounting/add_package.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def edit_package(request, id):
    data = Package.objects.get(id=id)
    form = PackageForm(instance=data)
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package Edited')
            return redirect('packages')
    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'Accounting/edit_package.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def del_package(request, id):
    obj = get_object_or_404(Package, id=id)
    obj.delete()
    messages.success(request, 'Package deleted')
    return redirect('packages')

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def create_inspection(request):
    form = InspectionForm()
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            print(form.errors)
            instance = form.save(commit=False)
            instance.inspector = request.user
            instance.save()
            messages.success(request,'Inspection Report Created')
            return redirect('inpection_reports')
    return render(request,'Accounting/inspection_create.html',{'form': form})

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def inpection_reports(request):
    reports = InspectionModel.objects.all()
    context = {
        'inspection_reports': reports,
    }
    return render(request,'Accounting/inspection_reports.html',context)

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def edit_inspection(request,id):
    data = get_object_or_404(InspectionModel, id = id)
    form = InspectionForm(instance = data)
    if request.method == 'POST':
        form = InspectionForm(request.POST,instance = data)
        if form.is_valid():
            print(form.errors)
            instance = form.save(commit=False)
            instance.inspector = request.user
            instance.save()
            messages.success(request,'Inspection Report Edited')
            return redirect('inpection_reports')
    return render(request,'Accounting/inspection_edit.html',{'form': form, 'id': id})

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def del_inspection(request,id):
    obj = get_object_or_404(InspectionModel , id = id)
    obj.delete()
    messages.success(request,'Report Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def membership_noti(request):
    membership_noti = MembershipNoti.objects.filter(is_seen = False).order_by('-id')
    data = []
    for i in membership_noti:
        prefetch = {
            'first_name': i.membership.user.first_name,
            'last_name': i.membership.user.last_name,
            'noti_text': i.noti_text,
            'created': i.created,
            'is_seen': i.is_seen,
            'membership_id': i.membership.id,
            'membership_noti_model_id': i.id,
            'user_id': i.membership.user.id,
        }
        data.append(prefetch)
    return JsonResponse(data,safe=False)


@login_required
def membership_noti_mark_as_seen(request,id):
    noti = MembershipNoti.objects.get(id = id)
    noti.is_seen = True
    noti.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(has_perm_user,REDIRECT_FIELD_NAME)
def user_membership_renewal_noti(request):
    data = []
    membership = MembershipModel.objects.filter(user_id = request.user.id)
    for i in membership:
        membership_end = i.membership_end
        if membership_end.date() <= datetime.now().date():
            MembershipRenewalNoti.objects.get_or_create(noti_for_id = i.id, 
                                                 noti_text = 'Membership Expired.Please renew your membership to get our premium service')
    
    renewal_noti = MembershipRenewalNoti.objects.filter(is_seen = False, 
                                                        noti_for__user_id = request.user.id).order_by('-id')
    for i in renewal_noti:
        prefetch = {
            'renewal_noti_id': i.id,
            'membership_model_id': i.noti_for.id,
            'noti_text': i.noti_text,
            'is_seen': i.is_seen,
            'created': i.created,
        }
        data.append(prefetch)
    return JsonResponse(data,safe=False)


@login_required
@user_passes_test(has_perm_user,REDIRECT_FIELD_NAME)
def mark_as_seen_membership_renewal_noti(request,id):
    noti = MembershipRenewalNoti.objects.get(id = id)
    noti.is_seen = True
    noti.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def employee_leave(request):
    form = LeaveForm()
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employee_name = request.user
            first_day_of_leave_request = instance.first_day_of_leave_request
            last_day_of_leave_request = instance.last_day_of_leave_request
            total_num_in_days = last_day_of_leave_request.date() - first_day_of_leave_request.date()
            print(total_num_in_days)
            instance.total_num_in_days = total_num_in_days
            instance.employee_clock = 'D'+str(request.user.id)
            instance.save()
            return redirect('my_leaves', request.user.id)
    context = {
        'form': form,
    }
    return render(request,'Accounting/leave_req.html',context)

@login_required
def my_leaves(request,id):
    my_leaves = Leaves.objects.filter(employee_name_id = id).order_by('-id')
    context = {
        'my_leaves': my_leaves,
    }
    return render(request,'Accounting/my_leaves.html', context)


@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def employee_leaves(request):
    leaves = Leaves.objects.all().order_by('-id')
    context = {
        'leaves': leaves,
    }
    return render(request,'Accounting/employee_leaves.html', context)


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def delete_leaves(request,id):
    obj = Leaves.objects.filter(id =id)
    obj.delete()
    messages.success(request,'Leave report Deleted')
    return redirect('employee_leaves')


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def payrol_deduction_reports(request):
    reports = PayrolDeduction.objects.all().order_by('-id')
    context = {
        'reports': reports,
    }
    return render(request,'Accounting/payrol_deduction_reports.html',context)

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def payroll_deduction_form(request):
    form = PayrolDeductionForm()
    if request.method == 'POST':
        monthly_deductions = request.POST.get('monthly_deductions')
        special_deductions = request.POST.get('special_deductions')
        penalties_financial_loss = request.POST.get('penalties_financial_loss')
        if monthly_deductions is not None:
            monthly_deductions = True
        else:
            monthly_deductions = False

        if special_deductions is not None:
            special_deductions = True
        else:
            special_deductions = False

        if penalties_financial_loss is not None:
            penalties_financial_loss = True
        else:
             penalties_financial_loss = False

        form = PayrolDeductionForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.report_by = request.user
            instance.monthly_deductions = monthly_deductions
            instance.special_deductions = special_deductions
            instance.penalties_financial_loss = penalties_financial_loss
            instance.save()
            messages.success(request,'Payroll Deduction Created')
            return redirect('payrol_deduction_reports')
    context ={
        'form': form,
    }
    return render(request,'Accounting/payroll_deduction_form.html',context)

@login_required
def payroll_deduction_individual_report(request,id):
    data = PayrolDeduction.objects.get(id = id)
    form = PayrolDeductionFormView(instance=data)
    context = {
        'form': form,
        'data': data,
        'id': id,
    }
    return render(request,'Accounting/individual_payroll_deductions.html',context)