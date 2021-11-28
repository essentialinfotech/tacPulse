from django.urls import path, include
from .api_views import *
urlpatterns = [
    path('ambulance/today/', AmbulanceRequestToday.as_view(), name='AmbulanceRequestToday'),
    path('ambulance/week/', AmbulanceRequestWeek.as_view(), name='AmbulanceRequestWeek'),
    path('ambulance/month/', AmbulanceRequestMonth.as_view(), name='AmbulanceRequestMonth'),

    #MOBILE API'S STARTS HERE . . .
    path('occurrence/reports/', OccurrenceReports.as_view(), name = 'occurrence_reports_api'),
    path('panic/notification/', Panic_Noti.as_view(), name = 'panic_noti_api'),
    path('ambulance/request/', AmbulanceRequest.as_view(), name = 'ambulance_req_api'),
    path('ambulance/requests/list/', AmbulanceRequestList.as_view(), name = 'AmbulanceRequestList_api'),
    path('panic/list/', PanicList.as_view() , name = 'panic_api_list'), 
    path('panic/crerate/', PanicCreate.as_view(), name = 'PanicCreate_api'),
    path('faq/', FAQLIST.as_view(), name = 'FAQLIST_api'),
    path('hospital/transfer/request/', HospitalTransferAPI.as_view(), name = 'HospitalTransferAPI_api'),
    path('hospital/transfer/request/list/', HospitalTransferList.as_view(), name = 'HospitalTransferList'),

    # dispatch incident
    path('assigned/paramedics/tasks/', AmbulanceModelList.as_view(), name = 'AmbulanceModelList_api'),
    path('paramedic/phases/update/', ParamedicsDifferentPhasesReportCreateApi.as_view(), name = 'ParamedicsDifferentPhasesReportCreateApi_api'),
    path('paramedic/reports/list/', ParamedicPhaseList.as_view(), name = 'ParamedicPhaseList_api'),
    path('photos/<int:id>/', DIspatchIncidentPhotosApi.as_view(), name = 'dispatch_incident_photo_api'),
    path('notes/<int:id>/', DIspatchIncidentServiceNotesApi.as_view(), name = 'service_notes'),
    path('scribes/', ScribeApi.as_view() , name = 'scribe_api'),

    # group chat api
    path('inbox/<int:id>/', GroupChatApi.as_view(), name = 'group_chat_api'),
]
