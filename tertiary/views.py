from django.shortcuts import render
def perfil(request):
    return render(request, 'template/Perfil.html')
def citas(request):
    return render(request, 'template/Citas.html')
