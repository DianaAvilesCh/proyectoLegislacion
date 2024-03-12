from .forms import DoctorForm,PersonaForm
from .models import Persona,Doctor,User
from django.shortcuts import render, redirect


def profile(request):
    if not request.user.is_authenticated:
        usuario = User.objects.get(id=1)  # Asegúrate de que este ID de usuario exista en tu base de datos
    else:
        usuario = request.user

    persona, created = Persona.objects.get_or_create(id_usuario=usuario)  # Asegura que la Persona exista
    doctor, created = Doctor.objects.get_or_create(id_persona=persona)  # Asegura que el Doctor exista

    if request.method == 'POST':
        persona_form = PersonaForm(request.POST, instance=persona)
        doctor_form = DoctorForm(request.POST, instance=doctor)
        if persona_form.is_valid() and doctor_form.is_valid():
            persona_form.save()
            doctor_form.save()
            return redirect('perfil_doctor')  # Redirige a la vista donde el doctor puede ver su perfil
    else:
        persona_form = PersonaForm(instance=persona)
        doctor_form = DoctorForm(instance=doctor)

    context = {
        'persona_form': persona_form,
        'doctor_form': doctor_form
    }
    return render(request, 'template/profile.html', context)


def quotes(request):
    return render(request, 'template/quotes.html')
