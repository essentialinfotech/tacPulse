from django.urls import path
from .api_views import *

urlpatterns = [
    path('schedule/today/', ScheduleToday.as_view(), name='ScheduleToday'),
    path('schedule/week/', ScheduleWeek.as_view(), name='ScheduleWeek'),
    path('schedule/month/', ScheduleMonth.as_view(), name='ScheduleMonth'),

    path('task/today/', TaskToday.as_view(), name='TaskToday'),
    path('task/week/', TaskWeek.as_view(), name='TaskWeek'),
    path('task/month/', TaskMonth.as_view(), name='TaskMonth'),

    path('transferred/today/', TransferredToday.as_view(), name='TaskToday'),
    path('transferred/week/', TransferredWeek.as_view(), name='TaskWeek'),
    path('transferred/month/', TransferredMonth.as_view(), name='TaskMonth'),

    path('stock/request/today/', StockRequestToday.as_view(), name='StockRequestToday'),
    path('stock/request/week/', StockRequestWeek.as_view(), name='StockRequestWeek'),
    path('stock/request/month/', StockRequestMonth.as_view(), name='StockRequestMonth'),
    path('stock/requested/', StockRequested.as_view(), name='StockRequested'),
    path('stock/request/canceled/', StockRequestCanceled.as_view(), name='StockRequestCanceled'),
]
