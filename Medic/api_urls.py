from django.urls import path, include
from .api_views import *
urlpatterns = [
    path('ambulance/today/', AmbulanceRequestToday.as_view(), name='AmbulanceRequestToday'),
    path('ambulance/week/', AmbulanceRequestWeek.as_view(), name='AmbulanceRequestWeek'),
    path('ambulance/month/', AmbulanceRequestMonth.as_view(), name='AmbulanceRequestMonth'),

]
