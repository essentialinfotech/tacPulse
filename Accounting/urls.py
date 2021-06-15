from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/member/', add_member, name='add_member'),
]
