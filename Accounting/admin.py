from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ScheduleModel)
admin.site.register(TaskModel)
admin.site.register(TaskTransferModel)
admin.site.register(StockRequestModel)
admin.site.register(Package)
