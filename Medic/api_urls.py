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
]
