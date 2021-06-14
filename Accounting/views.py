from django.shortcuts import render

# Create your views here.
def add_member(request):
    return render(request, 'base.html')