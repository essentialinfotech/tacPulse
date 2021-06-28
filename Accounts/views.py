from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from .decorators import user_passes_test, has_perm_admin, has_perm_user, has_perm_dispatch, REDIRECT_FIELD_NAME

import re
def regex_validation(number):
    regex= "^(?:\+27|0)(?:6\d|7[0-4]|7[6-9]|8[1-4])\d{7}$"
    if re.search(regex,number):
        print("Valid phone number:", number)
        return True
    else:
        print("Invalid phone number:", number)
        return False


# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request,'accounts/admin_dashboard.html')


def register(request):
    form = UserCreation()
    if request.method == 'POST':
        form = UserCreation(request.POST, request.FILES)
        is_dispatch = request.POST.get('is_stuff')

        if is_dispatch is not None:
            is_dispatch = True
        else:
            is_dispatch = False

        if form.is_valid():
            user = form.save(commit = False)
            user.is_staff = is_dispatch
            number = user.contact
            regex = regex_validation(number)
            if regex is True:
                user.save()
                return redirect('profile',id = user.id)
            else:
                return HttpResponse('Invalid phone number')
    return render(request,'registration/register.html',{'form':form})


@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def admin_profile(request, id):
    user = User.objects.all()
    me = User.objects.filter(id = id)
    context = {
        'user': user,
        'me': me,
    }
    return render(request,'accounts/admin_profile.html',context)


@user_passes_test(has_perm_dispatch, REDIRECT_FIELD_NAME)
def dispatch_profile(request, id):
    user = User.objects.filter(is_dispatch = True)
    return render(request, 'accounts/dispacth_profile.html',{'user':user})


@user_passes_test(has_perm_user, REDIRECT_FIELD_NAME)
def user_profile(request, id):
    user = User.objects.filter(Q(is_superuser = False) | Q(is_dispatch = False))
    return render(request, 'accounts/user_profile.html',{'user':user})


def chart_admin_profile(request):
    labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    data = ['30','500','87','400','12','300','52','200','12','100','13','50']
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def chart_dispatch_profile(request):
    labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    data = ['30','500','87','400','12','300','52','200','12','100','13','50']
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    

def edit_profile_admin(request):
    return render(request,'accounts/edit_profile_admin.html')


def edit_profile_dispatch(request):
    return render(request,'accounts/edit_profile_dispatch.html')


def edit_profile_user(request):
    return render(request,'accounts/edit_profile_user.html')


def reset_password(request):
    form = PasswordChangeForm(request.user)
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('logout')
    except:
        print('Demo purpose..no backend')
    context = {
        'form': form,
    }
    return render(request, 'accounts/reset_password.html', context)
