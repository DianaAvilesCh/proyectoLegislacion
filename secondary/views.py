from django.shortcuts import render
from primary.models import persona
def dashboard(request):
    return render(request, 'dashboard.html')
def patient(request):
    return render(request, 'patient.html')

