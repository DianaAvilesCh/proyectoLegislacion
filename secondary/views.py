from django.shortcuts import render
from primary.models import persona
def dashboard(request):
    username = request.session.get('username', '')
    return render(request, 'dashboard.html',{'username': username})
def patient(request):
    username = request.session.get('username', '')
    return render(request, 'patient.html',{'username': username})

def listar_datos(request):
    datos = persona.objects.all()
    return render(request, 'mi_app/listado.html', {'datos': datos})