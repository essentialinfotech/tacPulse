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
    path('scheduled/detail/<hashid:pk>/',
         ScheduleDetails.as_view(), name='schedule_details'),
    path('scheduled/update/<hashid:pk>/',
         UpdateSchedule.as_view(), name='schedule_update'),
    path('scheduled/delete/<hashid:pk>/',
         DeleteSchedule.as_view(), name='schedule_delete'),
    path('track/schedule/<hashid:pk>/',
         TrackSchedule.as_view(), name='track_schedule'),

    path('complete/schedule/', CompletedSchedule.as_view(), name='complete_schedule'),
    path('accepted/schedule/', AcceptedSchedule.as_view(), name='accepted_schedule'),

    path('add/paystub/', add_paystub, name='add_paystub'),
    path('paystub/report', paystub_report, name='paystub_report'),
    path('paystub/update/<hashid:pk>/', update_paystub_report, name='update_paystub_report'),
    path('paystub/delete/<hashid:pk>/', delete_paystub, name='delete_paystub'),
    path('create/task/', task_create, name='task_create'),
    path('task/report/', TasksList.as_view(), name='task_list'),
    path('task/update/<hashid:pk>/', UpdateTask.as_view(), name='update_task'),
    path('task/delete/<hashid:pk>/', DeleteTask.as_view(), name='delete_task'),
    path('transfer/task/<hashid:pk>/', TransferTask.as_view(), name='transfer_task'),
    path('transferred/tasks/', TransferredTasks.as_view(), name='transferred_task'),
    path('request/stock/', stock_request, name='stock_request'),
    path('cancel/stock/request/', cancel_stock_request,
         name='cancel_stock_request'),
    path('stock/requests/', StockRequest.as_view(), name='stock_requests'),
    path('stock/request/delete/<int:pk>/',
         DeleteStock.as_view(), name='DeleteStock'),
    path('stock/request/detail/<int:pk>/', StockRequestDetail.as_view(), name='stock_detail'),
    path('add/package/', add_package, name='add_package'),
    path('edit/package/<hashid:id>/', edit_package, name='edit_package'),
    path('delete/package/<hashid:id>/', del_package, name='del_package'),
]
