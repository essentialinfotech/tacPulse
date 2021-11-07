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
    path('emergency/medical/dispatch/incident/report/', ambulance_request,
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
    path('hospital/transfer/details/<int:pk>/',
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
     path('create/blog/post/', create_blog, name = 'create_blog'),
     path('our/blogs/', blog_list, name = 'blog_list'),
     path('blog/detail/<int:id>/', single_blog, name = 'single_blog'),
     path('ambulance/requests/notifications/', Ambulance_request_noti_for_admin_dispatch, name = 'Ambulance_request_noti_for_admin_dispatch'),
     path('hospital/transfer/notifications/', hospital_transfer_noti_for_admin_dispatch, name = 'hospital_transfer_noti_for_admin_dispatch'),
     path('hospital_transfer_noti_mark_seen/<int:id>/', h_transfer_noti_mark_seen, name = 'h_transfer_noti_mark_seen'),
     path('crew_and_vehicle/details/<int:id>', dispatch_incident_crew_and_vehicle, name = 'dispatch_incident_crew_and_vehicle'),
     path('add/another/crew_and_vehicle/<int:id>/', add_another_dispatch_incident_crew_and_vehicle, name = 'add_another_dispatch_incident_crew_and_vehicle'),
     path('dispatch/incident/travel/details/<int:id>/', dispatch_incident_travel_details, name = 'dispatch_incident_travel_details'),
     path('dispatch/incident/service/notes/<int:id>/', dispatch_incident_service_notes, name = 'dispatch_incident_service_notes'),
     path('add/another/dispatch/incident/service/note/<int:id>/', add_another_dispatch_incident_service_notes, name = 'add_another_dispatch_incident_service_notes'),
     path('dispatch/incident/location/details/<int:id>/', dispatch_incident_location_details, name = 'dispatch_incident_location_details'),
     path('add/another/dispatch/incident/location/details/<int:id>/', add_another_dispatch_incident_location_details, name = 'add_another_dispatch_incident_location_details'),
     path('dispatch/incident/patient/information/<int:id>/', dispatch_incident_patient_info, name = 'dispatch_incident_patient_info'),
     path('add/another/dispatch/incident/patient/information/<int:id>/', add_another_dispatch_incident_patient_info, name = 'add_another_dispatch_incident_patient_info'),
     path('add/dispatch/incident/photos/and/other/<int:id>/', dispatch_incident_photos_and_others, name = 'dispatch_incident_photos_and_others'),
     path('add/another/photo/other/document/dispatch/incident/<int:id>/', add_another_dispatch_incident_photos_and_others, name = 'add_another_dispatch_incident_photos_and_others'),
     path('dispatch/incident/dispatcher/certification/<int:id>/', dispatch_incident_dispatcher_certification, name = 'dispatch_incident_dispatcher_certification'),
     path('dispatch/incident/review/submission/<int:id>/', dispatch_incident_submission_review, name = 'dispatch_incident_submission_review'),
     path('dispatch/incident/submissions/', dispatch_incident_submission_review_all, name = 'dispatch_incident_submission_review_all'),
     path('add/another/service/note/for/dispacth/incident/<int:id>/', add_another_dispatch_incident_service_notes, name = 'add_another_dispatch_incident_service_notes'),
     path('dispatch/incident/report/pdf/<int:id>/', dispatch_incident_report_pdf, name = 'dispatch_incident_report_pdf'),

     path('form/builder/', form_save, name='form_builder'),
     path('form/list/', FormList.as_view(), name="form_list"),
     path('form/list/delete/', FormListDelete.as_view(), name="form_list_delete"),
     path('form/<int:pk>/', Form.as_view(), name="form"),
     path('save/form/', save_form, name="save_form"),
     path('form/data/<int:pk>/', FormDatatable.as_view(), name="form_data"),
     path('form/data/pdf/<int:pk>/', GenerateFormBuilderDataPdf.as_view(), name="form_data_pdf"),
     path('form/data/delete/', FormDataDelete.as_view(), name="form_data_delete"),
     path('form/data/edit/<int:pk>/',FormDataEdit.as_view(), name="edit_form_data"),

     path('add/call/sign/', AddCallSign.as_view(),name="add_call_sign"),
     path('edit/call/sign/<int:pk>/', EditCallSign.as_view(),name="edit_call_sign"),
     path('call/sign/', CallSignList.as_view(), name="call_sign"),
     path('vehicle/information/', VehicleInformation.as_view(), name="vehicle_information"),
     path('get/vehicle/information/', GetVehicleInformation.as_view(), name="get_vehicle_information"),
     path('photograph/<int:pk>/',VehiclePhotograph.as_view(), name='vehicle_photograph'),
     path('vehicle/category/<int:pk>/',VehicleCategory.as_view(), name="vehicle_category"),
     path('vehicle/profile/report/', VehicleProfileReport.as_view(), name="vehicle_profile_report"),
     path('vehicle/profile/delete/', VehicleProfileDelete.as_view(), name="vehicle_profile_delete"),
     path('categories & pictures/<int:pk>/', categories_pictures, name='categories_pictures'),
     path('edit/vehicle/information/<int:pk>/', EditVehicleInformation.as_view(), name='edit_vehicle_information'),

     path('daily preventive inspection/', DailyPreventiveInsperctions.as_view(), name="daily_preventive_insperctions"),
     path('vehicle/information/<int:pk>/', VehicleInformations.as_view(), name="vehicle_information"),
     path('pre inspection/selections/<int:pk>/', PreinspectionSelections.as_view(), name="pre_inspection_selection"),
     path('battery/main/<int:pk>/', BatteryMain.as_view(),name="battery_main"),
     path('edit/battery/<int:pk>/', EditBattery.as_view(), name="edit_battery"),
     path('inverter/main/<int:pk>/', InverterMain.as_view(),name="inverter_main"),
     path('edit/inverter/<int:pk>/', EditInverter.as_view(), name="edit_inverter"),
     path('body&branding/<int:pk>/', BodyBrandings.as_view(),name="bodybranding"),
     path('edit/body/branding/<int:pk>/', EditBodyBranding.as_view(), name="edit_body_branding"),
     path('fluid/inspection/<int:pk>/', FluidInspections.as_view(),name="fluid_inspection"),
     path('edit/fluid/inspection/<int:pk>/', EditFluidInspections.as_view(), name="edit_fluid_inspections"),
     path('internal/systems/<int:pk>/', InternalSystems.as_view(),name="internal_systems"),
     path('edit/internal/system/<int:pk>/', EditInternalSystems.as_view(), name="edit_internal_systems"),
     path('lights/<int:pk>/', Lights.as_view(),name="lights"),
     path('edit/light/<int:pk>/', EditLights.as_view(), name="edit_lights"),
     path('fleet/management/technician/<int:pk>/', FleetTechnicianConfirmations.as_view(),name="technician"),
     path('fleet/preventive/management/report/', FleetPreventiveManagementReport.as_view(), name="fleet_preventive_management_report"),
     path('vehicle/fleetmanagement/other/data/<int:pk>/',FleetManagementOtherData.as_view(),name="vehicle_fleetmanagement_other_data"),
     path('edit/fleet/management/<int:pk>/', EditFleetManagement.as_view(), name="edit_fleet_management"),
     path('fleet/management/delete/', FleetManagementDelete.as_view(), name="fleet_management_delete"),

     # not done pdf
     path('electronic/cash/invoice/<int:id>/', electronic_cash_pdf, name = 'electronic_cash_pdf'),
     path('order/pdf/<int:id>/', purchaseOrder_pdf, name = 'purchaseOrder_pdf'),
     path('quotation/emergency/operations/pdf/<int:id>/', quotation_emergency_operations_pdf, name = 'quotation_emergency_operations_pdf'),
     path('quotation/sports/events/pdf/<int:id>/', quotation_events_sports_pdf, name = 'quotation_events_sports_pdf'),

     path('delete/electronic/cash/receipt/<int:id>/', delete_electronic_cash_receipt, name = 'delete_electronic_cash_receipt'),
     path('delete/dispatch/emergency/incident/report/<int:id>/', delete_emergency_dispatch_incident_report, name = 'delete_emergency_dispatch_incident_report'),
     path('delete/expense/reimbursement/record/report/<int:id>/', delete_expense_reimbursement_record_report, name = 'delete_expense_reimbursement_record_report'),
     path('delete/purchased/order/report/<int:id>/', delete_purchase_order_report, name = 'delete_purchase_order_report'),
     path('delete/quotation/emergency/operation/<int:id>/', delete_quotation_emergency_operation_report, name = 'delete_quotation_emergency_operation_report'),
     path('delete/quotation/event-sport=true/<int:id>/', delete_quotation_event_sport_report, name = 'delete_quotation_event_sport_report'),

     path('ambulance/request/procedure/', ambulance_request_real, name = 'ambulance_request_real'),

     path('blog/comment/for/', blog_comment, name = 'blog_comment'),
     path('update/call_intake_phase/<int:id>/', edit_emergency_dispatch_incident_report_call_intake_phase, name = 'edit_emergency_dispatch_incident_report_call_intake_phase'),
     path('update/crew_and_vehicle_detail/<int:id>/', edit_dispatch_incident_crew_and_vehicle, name = 'edit_dispatch_incident_crew_and_vehicle'),
     path('assigning/paramedics/to/units/', assign_paramedics_to_units, name = 'assign_paramedics_to_units'),
     path('list/units/', paramedics_with_assigned_unit_list, name = 'paramedics_with_assigned_unit_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
