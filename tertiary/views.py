from django.shortcuts import render, redirect
from .models import Doctor, Cita,Persona, DoctorPaciente
from .forms import DoctorForm, CitaForm,PersonaForm
from django.contrib.auth.decorators import login_required
@login_required
def perfil_doctor(request):
    usuario = request.user
    persona, created = Persona.objects.get_or_create(id_usuario=usuario)
    doctor, created = Doctor.objects.get_or_create(id_persona=persona)

    # Inicialmente, el formulario no está en modo de edición.
    editing = "editar" in request.GET

    if request.method == 'POST':
        persona_form = PersonaForm(request.POST, instance=persona)
        doctor_form = DoctorForm(request.POST, instance=doctor)
        if persona_form.is_valid() and doctor_form.is_valid():
            persona_form.save()
            doctor_form.save()
            # Redirige a la vista sin el modo de edición activado.
            return redirect('perfil_doctor')
    else:
        persona_form = PersonaForm(instance=persona)
        doctor_form = DoctorForm(instance=doctor)

    context = {
        'persona_form': persona_form,
        'doctor_form': doctor_form,
        'editing': editing  # Envía el estado de edición al template.
    }
    return render(request, 'template/profile.html', context)
@login_required
def lista_citas(request):
    usuario = request.user
    doctor = usuario.persona.doctor
    citas = Cita.objects.filter(id_doctor_paciente__id_doctor=doctor)
    return render(request, 'template/quotes.html', {'citas': citas})

def profile(request):
    return
##