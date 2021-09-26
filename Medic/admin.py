from Medic.forms import PropertyForm
from django.contrib import admin
from django.forms.fields import FileField
from .models import *

# Register your models here.
admin.site.register(Panic)
admin.site.register(Rating)
admin.site.register(Occurrence)
admin.site.register(AmbulanceModel)
admin.site.register(PanicNoti)
admin.site.register(Feedback)
admin.site.register(PropertyTools)
admin.site.register(FAQ)
admin.site.register(CaseNote)
admin.site.register(HospitalTransferModel)
admin.site.register(Blog)
admin.site.register(AmbulanceNoti)
admin.site.register(HospitalTransferNoti)
admin.site.register(Senior)
admin.site.register(Scribe)
admin.site.register(Assist01)
admin.site.register(Assist02)
admin.site.register(Vehicles_count_with_info_for_ambulance_request)
admin.site.register(AmbulanceRequestModel)
