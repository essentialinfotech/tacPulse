from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import user_passes_test

#redirect url
def forbidden(request):
    return render(request,'user/forbidden.html')
REDIRECT_FIELD_NAME = 'forbidden'

#permissions
def has_perm_admin(user):
    return user.is_superuser

def has_perm_user(user):
    return not user.is_user

def has_perm_dispatch(user):
    return  user.is_dispatch






