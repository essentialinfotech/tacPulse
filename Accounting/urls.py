from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/member/', add_member, name='add_member'),
    path('add/package/', add_package, name='add_package'),
    path('packages/', packages, name='packages'),
    path('get/membership/', getmembership, name='getmembership'),
    path('members/', members, name='members'),
    path('schedule/trip/', ScheduleTrip.as_view(), name='shcedule_trip'),
    path('scheduled/trips/', TripSchedules.as_view(), name='trip_schedules'),
    path('scheduled/detail/<int:pk>/', ScheduleDetails.as_view(), name='schedule_details'),
    path('scheduled/update/<int:pk>/', UpdateSchedule.as_view(), name='schedule_update'),
    path('scheduled/delete/<int:pk>/', DeleteSchedule.as_view(), name='schedule_delete'),
    path('track/schedule/<int:pk>/', TrackSchedule.as_view(), name='track_schedule'),
    path('add/paystub/', add_paystub, name='add_paystub'),
    path('paystub/report', paystub_report, name='paystub_report'),
    path('create/task/', task_create, name='task_create'),
    path('task/report/', TasksList.as_view(), name='task_list'),
    path('task/update/<int:pk>/', UpdateTask.as_view(), name='update_task'),
    path('task/delete/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
    path('transfer/task/<int:pk>/', TransferTask.as_view(), name='transfer_task'),
    path('transferred/tasks/', TransferredTasks.as_view(), name='transferred_task'),
    path('request/stock/', stock_request, name='stock_request'),
    path('cancel/stock/request/', cancel_stock_request, name='cancel_stock_request'),
    path('stock/requests/', StockRequest.as_view(), name='stock_requests'),
    path('stock/request/delete/<int:pk>/', DeleteStock.as_view(), name='DeleteStock'),
    path('stock/request/detail/<int:pk>/', StockRequestDetail.as_view(), name='stock_detail'),
]
