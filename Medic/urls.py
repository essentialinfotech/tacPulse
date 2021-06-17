from django.urls import path
from .views import *

urlpatterns = [
    path('audit/form/', audit_form, name='audit_form'),
    path('assesment/form/', assetment_form, name='assetment_form'),
    path('rate/feedback/', rating, name='rating'),
    path('ambulance/request/', ambulance_request, name='ambulance_request'),
    path('ambulance/request/report/', ambulance_request_report,
         name='ambulance_request_report'),
    path('audit/form/', audit_form, name='audit_form'),
    path('audit/report/', audit_report, name='audit_report'),
    path('assesment/form/', assetment_form, name='assetment_form'),
    path('rate/feedback/', rating, name='rating'),
    path('dispatch/list/', dispatch_list, name='dispatch_list'),
    path('inspection/form/', inspection_form, name='inspection_form'),
    path('inspection/report/', inspaction_report, name='inspaction_report'),
    path('case/note/form/', case_note_form, name='case_note_form'),
    path('case/note/reports/', case_reports, name='case_reports'),
    path('stock/request/form/', stock_req_form, name='stock_req_form'),
    path('stock/request/report/', stock_req_reports, name='stock_req_reports'),
    path('property/form/', tools_form, name='tools_form'),
    path('hospital/transfer/report/', hospital_transfer_report,
         name='hospital_transfer_report'),
    path('hospital/transfer/request/',
         hospital_transfer, name='hospital_transfer'),

]
