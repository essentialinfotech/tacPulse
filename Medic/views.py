from django.shortcuts import render

# Create your views here.
def audit_form(request):
    return render(request,'medic/audit_form.html')

def assetment_form(request):
    return render(request,'medic/assesment_form.html')
