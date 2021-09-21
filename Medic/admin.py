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
admin.site.register(FAQ),
admin.site.register(CaseNote)
admin.site.register(HospitalTransferModel)
admin.site.register(Blog)
admin.site.register(AmbulanceNoti)
admin.site.register(HospitalTransferNoti)
