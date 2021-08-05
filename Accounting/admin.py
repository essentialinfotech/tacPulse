from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ScheduleModel)
admin.site.register(TaskModel)
admin.site.register(TaskTransferModel)
admin.site.register(StockRequestModel)
admin.site.register(Package)
admin.site.register(PaystubModel)
admin.site.register(InspectionModel)
admin.site.register(MembershipModel)
admin.site.register(MembershipNoti)
admin.site.register(MembershipRenewalNoti)
admin.site.register(Audit)
admin.site.register(Leaves)
admin.site.register(PayrolDeduction)
