from Medic.views import rating
from Medic.models import Panic, AmbulanceModel, Rating
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Accounting.models import TaskModel
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import  update_session_auth_hash,authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from .decorators import has_perm_admin_dispatch, user_passes_test, has_perm_admin, has_perm_user, has_perm_dispatch, is_active, \
                         REDIRECT_FIELD_NAME, INACTIVE_REDIRECT_FIELD_NAME
import datetime
import re

this_month = datetime.datetime.now().month
this_day = datetime.datetime.today()
this_year = datetime.datetime.now().year

def regex_validation(number):
    regex= "^(?:\+27|0)(?:6\d|7[0-4]|7[6-9]|8[1-4])\d{7}$"
    if re.search(regex, number):
        print("Valid phone number:", number)
        return True
    else:
        print("Invalid phone number:", number)
        return False


# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser:
        deactivated_users =  User.objects.filter(is_active = False)
        rating = Rating.objects.all()
        star1 = False
        star2 = False
        star3 = False
        star4 = False
        star5 = False
        for i in rating:
            if i.avg_rating <=1:
                star1 =True
            if i.avg_rating <=2 and i.avg_rating > 1:
                star2 =True
            if i.avg_rating <=3 and i.avg_rating > 2:
                star3 = True
            if i.avg_rating <=4 and i.avg_rating > 3:
                star4 = True
            if i.avg_rating <=5 and i.avg_rating > 4:
                star5 = True
                
        context = {
            'star1': star1,
            'star2': star2,
            'star3': star3,
            'star4': star4,
            'star5': star5,
            'deactivated_users': deactivated_users,
        }
        return render(request,'accounts/admin_dashboard.html', context)

    if request.user.is_staff and not request.user.is_superuser:
        return redirect('dispatch_profile', id=request.user.id)
    else:
        return redirect('user_profile', id=request.user.id)


def register(request):
    form = UserCreation()
    if request.method == 'POST':
        form = UserCreation(request.POST, request.FILES)
        is_dispatch = request.POST.get('is_staff')
        email = request.POST.get('username')

        if is_dispatch is not None:
            is_dispatch = True
        else:
            is_dispatch = False

        if form.is_valid():
            user = form.save(commit = False)
            user.is_staff = is_dispatch
            user.email = email
            number = user.contact
            regex = regex_validation(number)
            if regex is True:
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile',id = user.id)
            else:
                return HttpResponse('Invalid phone number')
    return render(request,'registration/register.html',{'form':form})


def profile(request,id):
    user = User.objects.get(id=id)
    if user.is_staff and not user.is_superuser:
        return redirect('dispatch_profile', id)
    elif user.is_superuser:
        return redirect('my_profile', id)
    else:
        return redirect('user_profile', id)


@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def admin_profile(request, id):
    user = User.objects.filter(is_superuser = False, is_staff = False)
    dispatch = User.objects.filter(is_staff = True, is_superuser = False)
    all_user = User.objects.filter(is_superuser = False)
    me = User.objects.filter(id = id)

    daily_req = AmbulanceModel.objects.filter(created_on__date = this_day).order_by('-id')

    monthly_req = AmbulanceModel.objects.filter(created_on__month = this_month, created_on__year = this_year).order_by('-id')

    weekly_req = AmbulanceModel.objects.filter(created_on__iso_week_day__gte = 1, \
                                                 created_on__month = this_month,\
                                                created_on__year = this_year).order_by('-id')
    
    print('Weekly:',weekly_req)

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
    return render(request,'accounts/admin_profile.html',context)


@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
def dispatch_profile(request, id):
    user = User.objects.filter(is_staff = True, id=id, is_superuser = False)
    patients = User.objects.filter(is_superuser = False, is_staff = False)  
    panic_req_month = Panic.objects.filter(timestamp__month = this_month, \
                                             timestamp__year = this_year).order_by('-id')
    task = TaskModel.objects.filter(dispatch_id = id)
    assesments = Assesment.objects.filter(to_user_id = id)
    context = {
        'user': user,
        'patients': patients,
        'panic_req_month': panic_req_month,
        'task': task,
        'assesments': assesments,
        'id': id,
    }
    return render(request, 'accounts/dispacth_profile.html', context)


def user_profile(request, id):
    user = User.objects.filter(is_superuser = False, is_staff = False, id=id)
    ambulance_req = AmbulanceModel.objects.filter(user_id = id,created_on__year = this_year)
    panic_req_yearly = Panic.objects.filter(panic_sender_id = id, timestamp__year = this_year)
    ambulance_req_total = AmbulanceModel.objects.filter(user_id = id,created_on__year = this_year).count()
    dispatch = User.objects.filter(is_staff = True, is_superuser = False)
    context = {
        'user': user,
        'dispatch': dispatch,
        'ambulance_req': ambulance_req,
        'ambulance_req_total': ambulance_req_total,
        'panic_req_yearly': panic_req_yearly,
        'id': id,
    }
    return render(request, 'accounts/user_profile.html', context)


def monthly_request_chart_ambulance(request):
    labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
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

    for i in range(0,13):
        if i == 1:
            Jan = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Jan)
        if i == 2:
            Feb = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Feb)
        if i == 3:
            Mar = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Mar)
        if i == 4:
            Apr = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Apr)
        if i == 5:
            May = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(May)
        if i == 6:
            Jun = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Jun)
        if i == 7:
            Jul = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Jul)  
        if i == 8:
            Aug = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Aug)   
        if i == 9:
            Sep = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Sep)  
        if i == 10:
            Oct = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Oct)  
        if i == 11:
            Nov = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Nov)  
        if i == 12:
            Dec = AmbulanceModel.objects.filter(created_on__month = i, created_on__year = this_year).count()
            data.append(Dec)  

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
 

@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def edit_profile_admin(request,id):
    data = User.objects.get(id = id)
    form = EditProfile(instance=data)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=data)
        if form.is_valid():
            email = form.cleaned_data['username']
            data.email = email
            data.save()
            form.save()
            return redirect('profile',id)
    context = {
        'form': form,
        'data': data,
        'id': id,
    }
    return render(request,'accounts/edit_profile_admin.html', context)


@user_passes_test(has_perm_dispatch, REDIRECT_FIELD_NAME)
def edit_profile_dispatch(request,id):
    data = User.objects.get(id = id)
    form = EditProfile(instance=data)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=data)
        if form.is_valid():
            email = form.cleaned_data['username']
            data.email = email
            data.save()
            form.save()
            return redirect('profile',id)
    context = {
        'form': form,
        'data': data,
        'id': id,
    }
    return render(request,'accounts/edit_profile_dispatch.html', context)

@user_passes_test(has_perm_user,REDIRECT_FIELD_NAME)
def edit_profile_user(request,id):
    data = User.objects.get(id = id)
    form = EditProfile(instance=data)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=data)
        if form.is_valid():
            email = form.cleaned_data['username']
            data.email = email
            data.save()
            form.save()
            return redirect('profile',id)
    context = {
        'form': form,
        'data': data,
        'id': id,
    }
    return render(request,'accounts/edit_profile_user.html',context)


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


@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def delete_any_user(request,id):
    url = request.META.get('HTTP_REFERER')
    user = User.objects.filter(id = id)
    user.delete()
    return HttpResponseRedirect(url)


def deactivate(request,id):
    user = User.objects.get(id = id)
    if request.user.is_superuser:
        if user.is_active is True:
            user.is_active = False
            user.save()
            return HttpResponse('Account Deactivated')
    else:
        return HttpResponse('This action can only be handled by admins')


def activate(request,id):
    try:
        user = User.objects.get(id = id)
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


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def assetment_form(request):
    form = AssesmentForm()
    if request.method == 'POST':
        form = AssesmentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.by_user = request.user
            instance.save()
            messages.success(request,'Assessment Created')
            return redirect('assesment_list_users')
    context = {
        'form': form,
    }
    return render(request, 'accounts/assesment_form.html', context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def assetment_form_edit(request,id):
    data = Assesment.objects.get(id = id)
    form = AssesmentForm(instance = data)
    if request.method == 'POST':
        form = AssesmentForm(request.POST, instance = data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.by_user = request.user
            instance.save()
            messages.success(request,'Assessment Created')
            return redirect('assesment_list_users')
    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'accounts/assesment_form_edit.html', context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def del_assesment(request,id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(Assesment, id = id)
    obj.delete()
    return HttpResponseRedirect(url)


@user_passes_test(has_perm_admin_dispatch,REDIRECT_FIELD_NAME)
def assessment_report_individually(request,id):
    diff = ''
    warning = Assesment.objects.filter(to_user_id = id,warning = True,created__month = this_month,
                                            created__year = this_year).count()
    month_assesments = Assesment.objects.filter(to_user_id = id,created__month = this_month,
                                            created__year = this_year).order_by('-id')
    year_assesments = Assesment.objects.filter(to_user_id = id,created__year = this_year).order_by('-id')

    good_category = Assesment.objects.filter(rate = 'Good',created__month = this_month, 
                                                created__year = this_year,\
                                                to_user_id = id).count()
    excellent_category = Assesment.objects.filter(rate = 'Excellent',created__month = this_month, 
                                                created__year = this_year,\
                                                to_user_id = id).count()
    satisfactory_category = Assesment.objects.filter(rate = 'Satisfactory',created__month = this_month, 
                                                created__year = this_year,\
                                                to_user_id = id).count()
    poor_category = Assesment.objects.filter(rate = 'Poor',created__month = this_month, 
                                                created__year = this_year,\
                                                to_user_id = id).count()
    very_poor_category = Assesment.objects.filter(rate = 'Very Poor',created__month = this_month, 
                                                created__year = this_year,\
                                                to_user_id = id).count()
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
    return render(request,'accounts/assessment_report.html', context)


@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def assesment_list_users(request):
    users = []
    user = Assesment.objects.values_list('to_user_id', flat=True).distinct()
    id = None
    for i in user:
        id = i
        data = User.objects.filter(id = id)
        users.append(data)
    print('result:',users)
    context = {
        'users': users,
    }
    return render(request,'accounts/assesments_list_users.html', context)

        

