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
    return user.is_superuser is True

def has_perm_user(user):
    return user.is_superuser is False and user.is_staff is False

def has_perm_dispatch(user):
    return user.is_staff is True

def is_active(user):
    return user.is_active is True






