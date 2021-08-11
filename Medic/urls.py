from django.urls import path, register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from Accounts.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('audit/form/', audit_form, name='audit_form'),
    path('rate/feedback/', rating, name='rating'),
    path('dispatch/list/', dispatch_list, name='dispatch_list'),
    path('inspection/form/', inspection_form, name='inspection_form'),
    path('case/note/add/<hashid:id>/', case_note_create, name='case_note_create'),
    path('property/form/', property_add, name='property_add'),
    path('property/<hashid:id>/', property_edit, name='property_edit'),
    path('create/occurrence/', occurrence_form, name='occurrence_form'),
    path('occurrence/report/', occurrence_report, name='occurrence_report'),
    path('panic/request/', panic_system, name='panic_system'),
    path('ambulance/request/', AmbulanceRequest.as_view(),
         name='ambulance_request'),
    path('ambulance/request/report/', AmbulanceRequestReport.as_view(),
         name='ambulance_request_report'),
    path('ambulance/request/detail/<hashid:pk>/',
         AmbulanceRequestDetail.as_view(), name='AmbulanceRequestDetail'),
    path('ambulance/track/<hashid:pk>/',
         AmbulanceTrackLocation.as_view(), name='AmbulanceTrackLocation'),
    path('ambulance/request/update/<int:pk>/',
         AmbulanceRequestUpdate.as_view(), name='AmbulanceRequestUpdate'),
    path('ambulance/request/delete/<hashid:pk>/',
         AmbulanceRequestDelete.as_view(), name='AmbulanceRequestDelete'),
    path('ambulance/task/complete/<hashid:pk>/',
         ambulance_task_complete, name='ambulance_task_complete'),

    path('audit/report/', audit_report, name='audit_report'),
    path('inspection/report/', inspaction_report, name='inspaction_report'),
    path('hospital/transfer/report/', hospital_transfer_report,
         name='hospital_transfer_report'),
    path('hospital/transfer/request/',
         hospital_transfer, name='hospital_transfer'),
    path('hospital/transfer/up/<hashid:pk>/',
         update_hospital_request, name='update_hospital_request'),
    path('hospital/transfer/details/<hashid:pk>/',
         details_hospital_request, name='details_hospital_request'),
    path('hospital/transfer/status/<hashid:pk>/',
         hospital_transfered, name='hospital_transfered'),
    path('hospital/transfer/delete/<hashid:pk>/',
         delete_hospital_request, name='delete_hospital_request'),
    path('panic/requests/', check_panic_requests, name='check_panic_requests'),
    path('individual/panic/location/<int:id>/',
         check_panic_requests_location, name='check_panic_requests_location'),
    path('panic/task/comlete/<hashid:pk>/',
         complete_panic_task, name='complete_panic_task'),
    path('delete/panic/request/<hashid:id>/', del_panic, name='del_panic'),
    path('property/report/', property_report, name='property_report'),
    path('delete/<hashid:id>/', common_delete, name='common_delete'),
    path('edit/occurrence/<hashid:id>/',
         edit_occurrence, name='edit_occurrence'),
    path('notification/panic/', panic_noti, name = 'panic_noti'),
    path('feedback/', feedback, name='feedback'),
    path('delete/property/<hashid:id>/', property_del, name='property_del'),
    path('invoice/<hashid:id>/', invoice_pdf_property,
         name='invoice_pdf_property'),
    path('FAQ/', faq, name='faq'),
    path('create/FAQ/', create_faq, name='create_faq'),
    path('edit/FAQ/<hashid:id>/', edit_faq, name='edit_faq'),
    path('delete/faq/<hashid:id>/', del_faq, name='del_faq'),
    path('showing/feedbacks/', feedbacks, name='feedbacks'),
    path('deleting/feedback/<hashid:id>/', del_feedback, name='del_feedback'),
    path('delete/case/<hashid:id>/', case_del, name='case_del'),
    path('case/notes/all/', case_notes, name='case_notes'),
    path('feedback/', feedback, name='feedback'),
    path('search/results/', search, name='search'),
    path('autosuggest/', autocomplete, name='autocomplete'),
    path('panic/notification/marking/as/read/<int:id>/', mark_seen_panic_noti, name ='mark_seen_panic_noti'),
    path('notification/length/', noti_length, name = 'noti_length'),
    path('paid/money/for/membership/chart/admin/dashboard/', membership_earnings_monthly_chart_dashboard, \
         name = 'membership_earnings_monthly_chart_dashboard'),
     path('delte/audit/<hashid:id>/', audit_delete, name = 'audit_delete'),
     path('editing/audit/<hashid:id>/', audit_edit, name = 'audit_edit'),
     path('individual/occurrence/details/<hashid:id>/', occurrence_details, name = 'occurrence_details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
