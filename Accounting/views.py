from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import *
from .serializer import *
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.views import APIView
from django.contrib import messages
from Accounts.decorators import user_passes_test, has_perm_admin, has_perm_admin_dispatch, has_perm_user, \
    has_perm_dispatch, REDIRECT_FIELD_NAME
from datetime import datetime, timedelta

today = datetime.today()
week = datetime.today().date() - timedelta(days=7)
month = datetime.today().date() - timedelta(days=30)


# Create your views here.


def add_member(request):
    return redirect('register')


def getmembership(request):
    return render(request, 'Accounting/get_membership.html')


def members(request):
    return render(request, 'Accounting/members.html')


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
        if self.request.user.is_superuser:
            daily = ScheduleModel.objects.filter(
                created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                created_on__gte=month).order_by('-id')
        elif self.request.user.is_staff:
            user_id = request.user.id
            daily = ScheduleModel.objects.filter(
                dispatch=user_id, created_on__gte=today.date()).order_by('-id')
            weekly = ScheduleModel.objects.filter(
                dispatch=user_id, created_on__gte=week).order_by('-id')
            monthly = ScheduleModel.objects.filter(
                dispatch=user_id, created_on__gte=month).order_by('-id')
        else:
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
        return render(request, 'Accounting/transfered_tasks.html')


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


def delete_paystub(request, pk):
    if request.user.is_superuser:
        data = get_object_or_404(PaystubModel, pk=pk)
        data.delete()
        return redirect('paystub_report')


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


def cancel_stock_request(request):
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
                form_obj.cancel = True
                form_obj.save()
                return redirect('stock_requests')

            except:
                return HttpResponse('Something Went Wrong')
    return render(request, 'Accounting/cancel_stock_req.html', {'form': form})


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


def packages(request):
    packages = Package.objects.all()
    context = {
        'packages': packages,
    }
    return render(request, 'Accounting/packages.html', context)


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


@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def del_package(request, id):
    obj = get_object_or_404(Package, id=id)
    obj.delete()
    messages.success(request, 'Package deleted')
    return redirect('packages')
