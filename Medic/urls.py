from django.urls import path,register_converter
from .views import *
from Accounts.utils import HashIdConverter
register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('audit/form/', audit_form, name = 'audit_form'),
    path('assesment/form/', assetment_form, name = 'assetment_form'),
    path('rate/feedback/', rating, name = 'rating'),
    path('dispatch/list/', dispatch_list , name = 'dispatch_list'),
    path('inspection/form/', inspection_form, name = 'inspection_form'),
    path('case/note/form/', case_note_form, name = 'case_note_form'),
    path('stock/request/form/', stock_req_form, name = 'stock_req_form'),
    path('property/form/', tools_form, name = 'tools_form'),
    path('occurrence/form/', occurrence_form, name = 'occurrence_form'),
    path('occurrence/report/', occurrence_report, name = 'occurrence_report'),
    path('panic/request/', panic_system, name = 'panic_system'),
    path('draggable/form/', dragable_form, name = 'dragable_form'),
    path('ambulance/request/', AmbulanceRequest.as_view(), name='ambulance_request'),
    path('ambulance/request/report/', AmbulanceRequestReport.as_view(),
         name='ambulance_request_report'),
    path('ambulance/request/detail/<int:pk>/', AmbulanceRequestDetail.as_view(),name='AmbulanceRequestDetail'),
    path('ambulance/track/<int:pk>/', AmbulanceTrackLocation.as_view(), name='AmbulanceTrackLocation'),

    path('audit/report/', audit_report, name='audit_report'),
    path('inspection/report/', inspaction_report, name='inspaction_report'),
    path('case/note/reports/', case_reports, name='case_reports'),
    path('stock/request/report/', stock_req_reports, name='stock_req_reports'),
    path('hospital/transfer/report/', hospital_transfer_report,
         name='hospital_transfer_report'),
    path('hospital/transfer/request/',
         hospital_transfer, name='hospital_transfer'),
     path('panic/requests/', check_panic_requests, name = 'check_panic_requests'),
      path('transfer/task/', task_transfer_req, name = 'task_transfer_req'),
     path('find/route/', get_route, name = 'get_route'),
     path('individual/panic/location/<hashid:id>/', check_panic_requests_location, name = 'check_panic_requests_location'),
     path('delete/panic/request/<hashid:id>/', del_panic, name = 'del_panic'),
     path('tools/report/', tools_report, name = 'tools_report'),
     path('schedule/report/', schedule_report, name = 'schedule_report'),
     path('delete/<hashid:id>/', common_delete, name = 'common_delete'),
     path('edit/occurrence/<hashid:id>/', edit_occurrence, name = 'edit_occurrence'),
]
