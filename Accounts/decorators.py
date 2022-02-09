from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import user_passes_test

#redirect url
def forbidden(request):
    return render(request,'accounts/forbidden.html')
REDIRECT_FIELD_NAME = 'forbidden'

def inactive(request):
    return HttpResponse('User is Not Active')

INACTIVE_REDIRECT_FIELD_NAME = 'inactive'

#permissions
def has_perm_admin(user):
    return user.is_superuser

def has_perm_user(user):
    return not user.is_staff and not user.medic

def has_perm_user_admin(user):
    return not user.medic

def has_perm_dispatch(user):
    return user.is_staff  and not user.is_superuser 

def is_active(user):
    return user.is_active

def has_perm_admin_dispatch(user):
    return user.is_staff






