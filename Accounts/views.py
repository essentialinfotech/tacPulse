from django.views.decorators import csrf
from Medic.views import rating
from Medic.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Accounting.models import MembershipModel, TaskModel
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Sum
from .decorators import has_perm_admin_dispatch, user_passes_test, has_perm_admin, has_perm_user, has_perm_dispatch, is_active, \
    REDIRECT_FIELD_NAME, INACTIVE_REDIRECT_FIELD_NAME
import datetime
import re
from django.views.decorators.csrf import csrf_exempt

this_month = datetime.datetime.now().month
this_day = datetime.datetime.today()
this_year = datetime.datetime.now().year


def regex_validation(number):
    regex = "^(?:\+27|0)(?:6\d|7[0-4]|7[6-9]|8[1-4])\d{7}$"
    if re.search(regex, number):
        print("Valid phone number:", number)
        return True
    else:
        print("Invalid phone number:", number)
        return False


def landing(request):
    blogs = Blog.objects.all()[:2]
    context = {
        'blogs': blogs,
    }
    return render(request,'landing/landing.html', context)

# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser:
        has_membership = User.objects.filter(has_membership = True)
        renew_membership = User.objects.filter(renew_membership = True)

        membership = MembershipModel.objects.all()

        ambulance_requests_monthly = AmbulanceRequestModel.objects.filter(created_on__month = this_month)
        ambulance_requests_monthly = len(ambulance_requests_monthly)

        ambulance_requests_daily = AmbulanceRequestModel.objects.filter(created_on__date = this_day)
        ambulance_requests_daily = len(ambulance_requests_daily)

        panic_requests_daily = Panic.objects.filter(timestamp__date = this_day)
        panic_requests_daily = len(panic_requests_daily)

        total_customers = User.objects.filter(is_superuser = False,is_staff = False,is_active = True).count()
        total_dispatch = User.objects.filter(is_superuser = False,is_staff = True,is_active = True).count()

        hos_trans = HospitalTransferModel.objects.filter(created_on__month = this_month, created_on__year = this_year)

        deactivated_users = User.objects.filter(is_active=False)
        rating = Rating.objects.all()
        average_rating = Rating.objects.values_list('avg_rating',flat=True)
        recent_panics = Panic.objects.filter(timestamp__year = this_year)[:10]
        star1 = False
        star2 = False
        star3 = False
        star4 = False
        star5 = False
        star0_5 = False
        star1_5 = False
        star2_5 = False
        star3_5 = False
        star4_5 = False

        for i in rating:
            avg = i.avg_rating
            if avg <= 0.5 and avg > 0:
                star0_5 = True

            if avg <= 1 and avg > 0.5:
                star1 = True

            if avg <= 1.5 and avg > 1:
                star1_5 = True

            if avg <= 2 and avg > 1.5:
                star2 = True

            if avg <= 2.5 and avg > 2:
                star2_5 = True

            if avg <= 3 and avg > 2.5:
                star3 = True

            if avg <= 3.5 and avg > 3:
                star3_5 = True

            if avg <= 4 and avg > 3.5:
                star4 = True

            if avg <= 4.5 and avg > 4:
                star4_5 = True

            if avg <= 5 and avg > 4.5:
                star5 = True

        hos_transfer = HospitalTransferModel.objects.filter(completed=True).order_by('-id')

        context = {
            'star1': star1,
            'star2': star2,
            'star3': star3,
            'star4': star4,
            'star5': star5,
            'star0_5': star0_5,
            'star1_5': star1_5,
            'star2_5': star2_5,
            'star3_5': star3_5,
            'star4_5': star4_5,
            'average_rating': average_rating,
            'deactivated_users': deactivated_users,
            'hos_transfer': hos_transfer,
            'ambulance_requests_monthly': ambulance_requests_monthly,
            'ambulance_requests_daily': ambulance_requests_daily,
            'panic_requests_daily': panic_requests_daily,
            'total_customers': total_customers,
            'total_dispatch': total_dispatch,
            'hos_trans': hos_trans,
            'recent_panics': recent_panics,
            'membership': membership,
            'has_membership': has_membership,
            'renew_membership': renew_membership,
        }
        return render(request, 'accounts/admin_dashboard.html', context)

    if request.user.is_staff and not request.user.is_superuser:
        return redirect('dispatch_profile', id=request.user.id)
    if request.user.medic:
        return redirect('medic_profile', id=request.user.id)
    else:
        return redirect('user_profile', id=request.user.id)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def register(request):
    form = UserCreation()
    if request.method == 'POST':
        form = UserCreation(request.POST, request.FILES)
        is_dispatch = request.POST.get('is_staff')
        medic = request.POST.get('medic')
        email = request.POST.get('username')

        if is_dispatch is not None:
            is_dispatch = True
        else:
            is_dispatch = False

        if medic is not None:
            medic = True
        else:
            medic = False

        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = is_dispatch
            user.medic = medic
            user.email = email
            number = user.contact
            regex = regex_validation(number)
            if regex is True:
                user.save()
                # login(request, user,
                #       backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile', id=user.id)
            else:
                return HttpResponse('Invalid phone number')
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    if user.is_staff and not user.is_superuser:
        return redirect('dispatch_profile', id)
    elif user.is_superuser:
        return redirect('my_profile', id)
    elif user.medic and not user.is_staff:
        return redirect('medic_profile', id)
    else:
        return redirect('user_profile', id)


@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def admin_profile(request, id):
    from datetime import datetime, timedelta
    last_seven_days = datetime.today() - timedelta(days=7)
    
    user = User.objects.filter(is_superuser=False, is_staff=False, medic = False)
    dispatch = User.objects.filter(is_staff=True, is_superuser=False)
    all_user = User.objects.filter(is_superuser=False)
    me = User.objects.filter(id=id)

    daily_req = AmbulanceRequestModel.objects.filter(
        created_on__date=this_day).order_by('-id')

    monthly_req = AmbulanceRequestModel.objects.filter(
        created_on__month=this_month, created_on__year=this_year).order_by('-id')

    weekly_req = AmbulanceRequestModel.objects.filter(created_on__gte = last_seven_days,
                                               created_on__month=this_month,
                                               created_on__year=this_year).order_by('-id')

    print('Weekly:', weekly_req)

    context = {
        'user': user,
        'dispatch': dispatch,
        'me': me,
        'all_user': all_user,
        'daily_req': daily_req,
        'monthly_req': monthly_req,
        'weekly_req': weekly_req,
        'id': id,
    }
    return render(request, 'accounts/admin_profile.html', context)


@login_required
@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
def medic_profile(request, id):
    user = User.objects.filter(id = id)
    chat = User.objects.filter(~Q(id = request.user.id))
    patients = User.objects.filter(is_superuser = False, is_staff = False, medic = False)
    panic_req_month = Panic.objects.filter(timestamp__month=this_month,
                                           timestamp__year=this_year).order_by('-id')
    task = TaskModel.objects.filter(dispatch_id=id, created_on__month = this_month)
    assesments = Assesment.objects.filter(to_user_id=id)
    context = {
        'user': user,
        'chat': chat,
        'patients': patients,
        'panic_req_month': panic_req_month,
        'task': task,
        'assesments': assesments,
        'id': id,
    }
    return render(request, 'accounts/medic_profile.html', context)


@login_required
@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
def dispatch_profile(request, id):
    user = User.objects.filter(id=id)
    chat = User.objects.filter(~Q(id = request.user.id))
    patients = User.objects.filter(is_superuser=False, is_staff=False, medic = False)
    panic_req_month = Panic.objects.filter(timestamp__month=this_month,
                                           timestamp__year=this_year).order_by('-id')
    task = TaskModel.objects.filter(dispatch_id=id, created_on__month = this_month)
    assesments = Assesment.objects.filter(to_user_id=id)
    context = {
        'user': user,
        'chat': chat,
        'patients': patients,
        'panic_req_month': panic_req_month,
        'task': task,
        'assesments': assesments,
        'id': id,
    }
    return render(request, 'accounts/dispacth_profile.html', context)

@login_required
@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
def user_profile(request, id):
    user = User.objects.filter(id=id)
    chat = User.objects.filter(~Q(id = request.user.id))
    ambulance_req = AmbulanceRequestModel.objects.filter(
        user_id=id, created_on__year=this_year)
    panic_req_yearly = Panic.objects.filter(
        panic_sender_id=id, timestamp__year=this_year)
    ambulance_req_total = AmbulanceRequestModel.objects.filter(
        user_id=id, created_on__year=this_year).count()
    dispatch = User.objects.filter(is_staff=True, is_superuser=False)
    context = {
        'user': user,
        'chat': chat,
        'dispatch': dispatch,
        'ambulance_req': ambulance_req,
        'ambulance_req_total': ambulance_req_total,
        'panic_req_yearly': panic_req_yearly,
        'id': id,
    }
    return render(request, 'accounts/user_profile.html', context)


def monthly_request_chart_ambulance(request):
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = []
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
            Jan = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Jan)
        if i == 2:
            Feb = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Feb)
        if i == 3:
            Mar = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Mar)
        if i == 4:
            Apr = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Apr)
        if i == 5:
            May = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(May)
        if i == 6:
            Jun = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Jun)
        if i == 7:
            Jul = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Jul)
        if i == 8:
            Aug = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Aug)
        if i == 9:
            Sep = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Sep)
        if i == 10:
            Oct = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Oct)
        if i == 11:
            Nov = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Nov)
        if i == 12:
            Dec = AmbulanceRequestModel.objects.filter(
                created_on__month=i, created_on__year=this_year).count()
            data.append(Dec)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def edit_profile_admin(request, id):
    data = User.objects.get(id=id)
    form = EditProfile(instance=data)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=data)
        if form.is_valid():
            email = form.cleaned_data['username']
            data.email = email
            data.save()
            form.save()
            return redirect('profile', id)
    context = {
        'form': form,
        'data': data,
        'id': id,
    }
    return render(request, 'accounts/edit_profile_admin.html', context)

@login_required
def edit_profile_medic(request, id):
    if id == request.user.id: 
        data = User.objects.get(id=id)
        form = EditProfile(instance=data)
        if request.method == 'POST':
            form = EditProfile(request.POST, request.FILES, instance=data)
            if form.is_valid():
                email = form.cleaned_data['username']
                data.email = email
                data.save()
                form.save()
                return redirect('profile', id)
        context = {
            'form': form,
            'data': data,
            'id': id,
        }
        return render(request, 'accounts/edit_profile_medic.html', context)
    else:
        return redirect('forbidden')

@login_required
@user_passes_test(has_perm_dispatch, REDIRECT_FIELD_NAME)
def edit_profile_dispatch(request, id):
    if id == request.user.id: 
        data = User.objects.get(id=id)
        form = EditProfile(instance=data)
        if request.method == 'POST':
            form = EditProfile(request.POST, request.FILES, instance=data)
            if form.is_valid():
                email = form.cleaned_data['username']
                data.email = email
                data.save()
                form.save()
                return redirect('profile', id)
        context = {
            'form': form,
            'data': data,
            'id': id,
        }
        return render(request, 'accounts/edit_profile_dispatch.html', context)
    else:
        return redirect('forbidden')

@login_required
@user_passes_test(has_perm_user, REDIRECT_FIELD_NAME)
def edit_profile_user(request, id):
    if id == request.user.id: 
        data = User.objects.get(id=id)
        form = EditProfile(instance=data)
        if request.method == 'POST':
            form = EditProfile(request.POST, request.FILES, instance=data)
            if form.is_valid():
                email = form.cleaned_data['username']
                data.email = email
                data.save()
                form.save()
                return redirect('profile', id)
        context = {
            'form': form,
            'data': data,
            'id': id,
        }
        return render(request, 'accounts/edit_profile_user.html', context)
    else:
        return redirect('forbidden')


def change_pass(request):
    form = PasswordChangeForm(request.user)
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('logout')
    except:
        return HttpResponse('Internal Server Error')
    context = {
        'form': form,
    }
    return render(request, 'accounts/reset_password.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def delete_any_user(request, id):
    url = request.META.get('HTTP_REFERER')
    user = User.objects.filter(id=id)
    user.delete()
    return HttpResponseRedirect(url)

@login_required
def deactivate(request, id):
    user = User.objects.get(id=id)
    if request.user.is_superuser:
        if user.is_active is True:
            user.is_active = False
            user.save()
            return HttpResponse('Account Deactivated')
        else:
            return HttpResponse('Already Deactivated')
    else:
        return HttpResponse('This action can only be handled by admins')

@login_required
def activate(request, id):
    try:
        user = User.objects.get(id=id)
        if request.user.is_superuser:
            if user.is_active is False:
                user.is_active = True
                user.save()
                return HttpResponse('Account Activated')
            else:
                return HttpResponse('user not found or account already active')
        else:
            return HttpResponse('Only admins can activate your account')
    except:
        return HttpResponse('Internal Server Error')


class TrackDispatches(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'accounts/track_dispatches.html')
        else:
            return redirect('forbidden')

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def assetment_form(request):
    form = AssesmentForm()
    if request.method == 'POST':
        form = AssesmentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.by_user = request.user
            instance.save()
            messages.success(request, 'Assessment Created')
            return redirect('assesment_list_users')
    context = {
        'form': form,
    }
    return render(request, 'accounts/assesment_form.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def assetment_form_edit(request, id):
    data = Assesment.objects.get(id=id)
    form = AssesmentForm(instance=data)
    if request.method == 'POST':
        form = AssesmentForm(request.POST, instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.by_user = request.user
            instance.save()
            messages.success(request, 'Assessment Created')
            return redirect('assesment_list_users')
    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'accounts/assesment_form_edit.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def del_assesment(request, id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(Assesment, id=id)
    obj.delete()
    return HttpResponseRedirect(url)

@login_required
@user_passes_test(has_perm_admin_dispatch, REDIRECT_FIELD_NAME)
def assessment_report_individually(request, id):
    diff = ''
    warning = Assesment.objects.filter(to_user_id=id, warning=True, created__month=this_month,
                                       created__year=this_year).count()
    month_assesments = Assesment.objects.filter(to_user_id=id, created__month=this_month,
                                                created__year=this_year).order_by('-id')
    year_assesments = Assesment.objects.filter(
        to_user_id=id, created__year=this_year).order_by('-id')

    good_category = Assesment.objects.filter(rate='Good', created__month=this_month,
                                             created__year=this_year,
                                             to_user_id=id).count()
    excellent_category = Assesment.objects.filter(rate='Excellent', created__month=this_month,
                                                  created__year=this_year,
                                                  to_user_id=id).count()
    satisfactory_category = Assesment.objects.filter(rate='Satisfactory', created__month=this_month,
                                                     created__year=this_year,
                                                     to_user_id=id).count()
    poor_category = Assesment.objects.filter(rate='Poor', created__month=this_month,
                                             created__year=this_year,
                                             to_user_id=id).count()
    very_poor_category = Assesment.objects.filter(rate='Very Poor', created__month=this_month,
                                                  created__year=this_year,
                                                  to_user_id=id).count()
    good = good_category + excellent_category + satisfactory_category
    bad = poor_category + very_poor_category
    if good > bad:
        diff = str(good - bad) + ' positive rating more than negative rating'
    elif good < bad:
        diff = str(bad - good) + ' negative rating more than positive rating'
    elif good == bad:
        diff = 'Negative and Positive ratios are equal'
    else:
        diff = ''
    context = {
        'month_assesments': month_assesments,
        'year_assesments': year_assesments,
        'diff': diff,
        'warning': warning,
        'id': id,
    }
    return render(request, 'accounts/assessment_report.html', context)

@login_required
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def assesment_list_users(request):
    users = []
    user = Assesment.objects.values_list('to_user_id', flat=True).distinct()
    id = None
    for i in user:
        id = i
        data = User.objects.filter(id=id)
        users.append(data)
    print('result:', users)
    context = {
        'users': users,
    }
    return render(request, 'accounts/assesments_list_users.html', context)

@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def customer_list(request):
    customers = User.objects.filter(is_superuser = False, is_staff = False, medic = False)
    context = {
        'customers': customers,
    }
    return render(request,'accounts/customer_list.html',context)

@login_required
def send_message(request,id):
    # to delete messages on next day
    all_msges_except_today = Message.objects.filter(sent__date__lt = this_day)
    for i in all_msges_except_today:
        i.delete()

    online_user = request.user
    messages = Message.objects.filter(Q(sender = request.user, receiver_id = id)| 
                                        Q(sender_id = id, receiver = request.user)).order_by('sent')
    users = User.objects.filter(~Q(id = request.user.id))
    other_user = User.objects.get(id = id)

    if request.method == 'POST':
        sender = request.user
        message = request.POST.get('message')
        file = request.FILES.get('file')
        if file is None:
            file = None
        if message or file:
            Message.objects.create(sender = sender, file = file , receiver_id = id, message = message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {
        'messages': messages,
        'users': users,
        'other_user': other_user,
        'online_user': online_user,
        'id': id,
    }
    return render(request,'accounts/chat.html',context)

@login_required
def delete_message(request,id):
    msg = Message.objects.filter(Q(sender = request.user, receiver_id = id)|
                                Q(sender_id = id , receiver = request.user))
    msg.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def post_pos_dispatch(request):
    if request.method == 'POST':
        data = request.POST
        for k,v in data.items():
            if  k=='lat':
                latitude = v
            if k=='lng':
                longitude = v
        user = User.objects.get(id = request.user.id)
        user.latitude = latitude
        user.longitude = longitude
        user.save()
        print(user.latitude,user.longitude)
        return HttpResponse('Lat , Lng: Posted')


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def corporate_users(request):
    user = User.objects.filter(Q(is_staff = True) | Q(medic = True), is_superuser = False)
    context = {
        'user': user
    }
    return render(request,'accounts/corporate_users.html',context)
    

@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def manage_role(request,id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        is_staff = request.POST.get('is_staff')
        medic = request.POST.get('medic')

        if is_staff is not None:
            is_staff = True
        else:
            is_staff = False

        if medic is not None:
            medic = True
        else:
            medic = False

        user.is_staff = is_staff
        user.medic = medic
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'user': user,
        'id': id,
    }
    return render(request,'accounts/manage_roles.html',context)


