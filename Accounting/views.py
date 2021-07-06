from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .serializer import *
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.


def add_member(request):
    return redirect('register')


def add_package(request):
    if request.method == 'POST':
        return redirect('packages')
    return render(request, 'Accounting/add_package.html')


def packages(request):
    return render(request, 'Accounting/packages.html')


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
        data = ScheduleModel.objects.all()
        context = {
            'data': data,
        }
        return render(request, 'Accounting/trip_schedules.html', context)


class DeleteSchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(ScheduleModel, pk=pk)
            if data:
                data.delete()
                return redirect('shcedule_trip')
            return redirect('shcedule_trip')
        else:
            return render(request, 'accounts/forbidden.html')


class UpdateSchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(ScheduleModel, pk=pk)
        if request.user.is_superuser or request.user.id == data.user.id:
            form = ScheduleModelForm(instance=data)
            return render(request, 'Accounting/update_scedule.html', {'form': form})
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
                return render(request, 'Accounting/update_scedule.html', {'form': form})
        else:
            return render(request, 'accounts/forbidden.html')


class ScheduleDetails(LoginRequiredMixin, DetailView):
    model = ScheduleModel
    template_name = 'Accounting/sechdule_details.html'


class TrackSchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        data = get_object_or_404(ScheduleModel, pk=pk)
        return render(request, 'Accounting/track_schedule.html', {'data': data})


def task_create(request):
    if request.user.is_superuser:
        form = TaskModelForm()
        dispatch = User.objects.filter(is_staff=True)
        schedule = ScheduleModel.objects.filter(assigned=False)
        ambulance = AmbulanceModel.objects.filter(assigned=False)
        panic = Panic.objects.filter(assigned=False)
        if request.method == 'POST':
            form = TaskModelForm(request.POST)
            x = request.POST.get('task_type')
            at = request.POST.get('ambulance_task')
            st = request.POST.get('scheduled_task')
            pt = request.POST.get('panic_task')
            if form.is_valid():
                form.save(commit=False)
                if x == 'sch':
                    data = get_object_or_404(ScheduleModel, pk=st)
                    data.assigned = True
                    data.save()
                elif x == 'ambr':
                    data = get_object_or_404(AmbulanceModel, pk=at)
                    data.assigned = True
                    data.save()
                else:
                    data = get_object_or_404(PaystubModel, pk=pt)
                    data.assigned = True
                    data.save()
                form.save()
                return redirect('task_list')

        context = {
            'form': form,
            'dispatch': dispatch,
            'schedule': schedule,
            'ambulance': ambulance,
            'panic': panic
        }
        return render(request, 'Accounting/taskcreate.html', context)
    else:
        return render(request, 'accounts/forbidden.html')


class TasksList(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Accounting/task_list.html')


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


class TransferTask(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            form = TransferTaskForm()
            data = get_object_or_404(TaskModel, pk=pk)
            user_id = data.dispatch.id
            dispatches = User.objects.filter(~Q(is_superuser=True), ~Q(pk=user_id), is_staff=True)
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
            dispatches = User.objects.filter(~Q(is_superuser=True), ~Q(pk=user_id), is_staff=True)
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
    return render(request, 'Accounting/add_paystub.html')


def paystub_report(request):
    return render(request, 'Accounting/paystub_report.html')


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
            return render(request, 'Accounting/stock_requests.html')
        else:
            return render(request, 'accounts/forbidden.html')


class StockRequestDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(StockRequestModel, pk=pk)
            return render(request, 'Accounting/stc_req_detail.html', {'data':data})
        else:
            return render(request, 'accounts/forbidden.html')


class DeleteStock(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_superuser:
            data = get_object_or_404(StockRequestModel, pk=pk)
            return redirect('stock_requests')
