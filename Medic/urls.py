from django.urls import path
from .views import *

urlpatterns = [
    path('audit/form/', audit_form, name = 'audit_form'),
    path('assesment/form/', assetment_form, name = 'assetment_form'),
    path('rate/feedback/', rating, name = 'rating'),
    path('dispatch/list/', dispatch_list , name = 'dispatch_list'),
    path('inspection/form/', inspection_form, name = 'inspection_form'),
    path('case/note/form/', case_note_form, name = 'case_note_form'),
    path('stock/request/form/', stock_req_form, name = 'stock_req_form'),
    path('property/form/', tools_form, name = 'tools_form'),
    path('occurrence/form/', occurrence_form, name = 'occurrence_form'),
    path('panic/request/', panic_system, name = 'panic_system'),
    path('draggable/form/', dragable_form, name = 'dragable_form'),
]
