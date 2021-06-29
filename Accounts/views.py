from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from .decorators import user_passes_test, has_perm_admin, has_perm_user, has_perm_dispatch, is_active, \
                         REDIRECT_FIELD_NAME, INACTIVE_REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, login

import re
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
        context = {
            'deactivated_users': deactivated_users,
        }
        return render(request,'accounts/admin_dashboard.html', context)

    if request.user.is_staff:
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
    if user.is_staff:
        return redirect('dispatch_profile', id)
    elif user.is_superuser:
        return redirect('admin_profile', id)
    else:
        return redirect('user_profile', id)

@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
@user_passes_test(has_perm_admin, REDIRECT_FIELD_NAME)
def admin_profile(request, id):
    user = User.objects.filter(is_superuser = False, is_staff = False)
    dispatch = User.objects.filter(is_staff = True)
    all_user = User.objects.filter(is_superuser = False)
    me = User.objects.filter(id = id)
    context = {
        'user': user,
        'dispatch': dispatch,
        'me': me,
        'all_user': all_user,
    }
    return render(request,'accounts/admin_profile.html',context)


@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
@user_passes_test(has_perm_dispatch, REDIRECT_FIELD_NAME)
def dispatch_profile(request, id):
    user = User.objects.filter(is_staff = True, id=id)
    patients = User.objects.filter(is_superuser = False, is_staff = False)  
    context = {
        'user': user,
        'patients': patients,
        'id': id,
    }
    return render(request, 'accounts/dispacth_profile.html', context)


@user_passes_test(is_active, INACTIVE_REDIRECT_FIELD_NAME)
@user_passes_test(has_perm_user, REDIRECT_FIELD_NAME)
def user_profile(request, id):
    user = User.objects.filter(is_superuser = False, is_staff = False, id=id)
    context = {
        'user': user,
        'id': id,
    }
    return render(request, 'accounts/user_profile.html', context)


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


def change_pass(request):
    form = PasswordChangeForm(request.user)
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            print(form.errors)
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
    if user.is_active is True:
        user.is_active = False
        user.save()
        return HttpResponse('Account Deactivated')



def activate(request,id):
    user = User.objects.get(id = id)
    try:
        if request.user.is_superuser:
            if user.is_active is False:
                user.is_active = True
                user.save()
                return HttpResponse('Account Activated')
        else:
            return HttpResponse('Only admins can deactivate your account')
    except:
        return HttpResponse('Internal Server Error')
