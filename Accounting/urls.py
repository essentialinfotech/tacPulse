from django.urls import path, register_converter
from .views import *
from Accounts.utils import HashIdConverter
register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('add/member/', add_member, name='add_member'),
    path('add/package/', add_package, name='add_package'),
    path('packages/', packages, name='packages'),
    path('get/membership/', getmembership, name='getmembership'),
    path('members/', members, name='members'),
    path('schedule/trip/', ScheduleTrip.as_view(), name='shcedule_trip'),
    path('scheduled/trips/', TripSchedules.as_view(), name='trip_schedules'),
    path('add/paystub/', add_paystub, name='add_paystub'),
    path('paystub/report', paystub_report, name='paystub_report'),
    path('add/package/', add_package, name = 'add_package'),
    path('edit/package/<hashid:id>/', edit_package, name='edit_package'),
    path('delete/package/<hashid:id>/', del_package, name = 'del_package'),
]
