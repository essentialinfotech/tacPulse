from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import *
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    return render(request,'accounts/admin_dashboard.html')


def register(request):
    return render(request,'registration/register.html')


def admin_profile(request):
    user = User.objects.all()
    return render(request,'accounts/admin_profile.html',{'user':user})

def dispatch_profile(request):
    user = User.objects.all()
    return render(request, 'accounts/dispacth_profile.html',{'user':user})

def user_profile(request):
    dispatch = User.objects.filter(is_superuser = False)
    return render(request, 'accounts/user_profile.html',{'dispatch':dispatch})


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
