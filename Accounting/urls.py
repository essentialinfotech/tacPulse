from django.urls import path, register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
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
    path('scheduled/detail/<hashid:pk>/', ScheduleDetails, name='schedule_details'),
    path('scheduled/update/<hashid:pk>/', UpdateSchedule.as_view(), name='schedule_update'),
    path('scheduled/delete/<hashid:pk>/', DeleteSchedule.as_view(), name='schedule_delete'),
    path('scheduled/complete/<hashid:pk>/', schedule_status_change, name='schedule_status_change'),
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
    path('task/detail/<hashid:pk>/', task_detail, name='task_detail'),
    path('transfer/task/<hashid:pk>/', TransferTask.as_view(), name='transfer_task'),
    path('transferred/tasks/', TransferredTasks.as_view(), name='transferred_task'),
    path('request/stock/', stock_request, name='stock_request'),
    path('cancel/stock/request/', cancel_stock_request,
         name='cancel_stock_request'),
    path('stock/requests/', StockRequest.as_view(), name='stock_requests'),
    path('stock/request/delete/<hashid:pk>/',
         DeleteStock.as_view(), name='DeleteStock'),
    path('stock/request/detail/<hashid:pk>/', StockRequestDetail.as_view(), name='stock_detail'),
    path('add/package/', add_package, name='add_package'),
    path('edit/package/<hashid:id>/', edit_package, name='edit_package'),
    path('delete/package/<hashid:id>/', del_package, name='del_package'),
    path('create/inspection/', create_inspection, name = 'create_inspection'),
    path('inspection/reports/', inpection_reports, name = 'inpection_reports'),
    path('delete/inspection/<hashid:id>/', del_inspection, name = 'del_inspection'),
    path('update/inspection/<hashid:id>/', edit_inspection, name = 'edit_inspection'),


    path('payment/<hashid:id>/', payment, name = 'payment'),
    path('payment/backend/', payment_backend, name = 'payment_backend'),
    path('purchased/', package_purchased, name = 'package_purchased'),
    path('membership/notificattions/', membership_noti, name = 'membership_noti'),
    path('membership/details/individual/<int:id>/', viewing_membership_details_individual, name = 'viewing_membership_details_individual'),
    path('mark/as/read/membership/notification/<int:id>/', membership_noti_mark_as_seen, name = 'membership_noti_mark_as_seen'),
    path('renewal/membership/', user_membership_renewal_noti, name = 'user_membership_renewal_noti'),
    path('mark/as/seen/membership/renewal/notification/<int:id>/', mark_as_seen_membership_renewal_noti, name = 'mark_as_seen_membership_renewal_noti'),
    path('employee/leave/request/', employee_leave, name = 'employee_leave'),
    path('my/leaves/<hashid:id>/', my_leaves, name = 'my_leaves'),
    path('employee/leave/reports/', employee_leaves, name = 'employee_leaves'),
    path('delete/leave/report/<hashid:id>/', delete_leaves, name = 'delete_leaves'),
    path('reports/payroll/deductions/', payrol_deduction_reports, name = 'payrol_deduction_reports'),
    path('payroll/deductions/', payroll_deduction_form, name = 'payroll_deduction_form'),
    path('payroll/deduction/individual/report/view/<hashid:id>/', payroll_deduction_individual_report, name = 'payroll_deduction_individual_report'),
    path('delete/payrolldeductionreport/<hashid:id>/', payroll_deduction_delete, name = 'payroll_deduction_delete'),
    path('has_membership_or_not/', has_membership_or_not, name = 'has_membership_or_not'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)