from django.shortcuts import render
def dashboard(request):
    return render(request, 'template/dashboard.html')
def patient(request):
    return render(request, 'template/patient.html')