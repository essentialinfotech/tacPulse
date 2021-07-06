from django.urls import path
from .api_views import *

urlpatterns = [
    path('dispatch/location/', DispatchesLocationAPI.as_view(), name='DispatchesLocationAPI')
]