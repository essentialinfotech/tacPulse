from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','password1','password2',
                    'username','contact','address', 'is_staff','profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),          
        }