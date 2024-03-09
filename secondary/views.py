from django.shortcuts import render
def dashboard(request):
    return render(request, 'dashboard.html')
def patient(request):
    return render(request, 'patient.html')