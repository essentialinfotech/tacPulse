from django.urls import path
from .views import *

urlpatterns = [
    path('audit/form/', audit_form, name = 'audit_form'),
    path('assesment/form/', assetment_form, name = 'assetment_form'),
]
