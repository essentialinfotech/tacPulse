from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import *

# Create your views here.
def dashboard(request):
    return render(request,'accounts/admin_dashboard.html')


def register(request):
    return render(request,'registration/register.html')


def my_profile(request):
    pass


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
