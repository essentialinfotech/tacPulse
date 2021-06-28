from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/member/', add_member, name='add_member'),
    path('add/package/', add_package, name='add_package'),
    path('packages/', packages, name='packages'),
    path('get/membership/', getmembership, name='getmembership'),
    path('members/', members, name='members'),
    path('schedule/trip/', ScheduleTrip.as_view(), name='shcedule_trip'),
    path('scheduled/trips/', trip_schedules, name='trip_schedules'),
    path('add/paystub/', add_paystub, name='add_paystub'),
    path('paystub/report', paystub_report, name='paystub_report'),
]
