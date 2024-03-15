from django.shortcuts import render, redirect, get_object_or_404
from primary.models import doctor, persona
from secondary.models import doctor_paciente, paciente
from tertiary.models import cita

from .forms import DoctorForm, CitaForm, PersonaForm
from django.contrib.auth.decorators import login_required


@login_required
def perfil_doctor(request):
    usuario = request.user
    # Obtenemos o creamos el objeto doctor relacionado con el usuario.
    # La relación entre doctor y persona se maneja internamente en los modelos.
    doctor_instance, created = doctor.objects.get_or_create(id_usuario=usuario)

    # Obtenemos la persona relacionada con este doctor.
    # Asumimos que ya existe una relación entre doctor y persona.
    persona_instance = doctor_instance.id_persona

    # Inicialmente, el formulario no está en modo de edición.
    editing = "editar" in request.GET

    if request.method == 'POST':
        persona_form = PersonaForm(request.POST, instance=persona_instance)
        doctor_form = DoctorForm(request.POST, instance=doctor_instance)
        if persona_form.is_valid() and doctor_form.is_valid():
            persona_form.save()
            doctor_form.save()
            # Redirige a la vista sin el modo de edición activado.
            return redirect('perfil_doctor')
    else:
        persona_form = PersonaForm(instance=persona_instance)
        doctor_form = DoctorForm(instance=doctor_instance)

    context = {
        'persona_form': persona_form,
        'doctor_form': doctor_form,
        'editing': editing  # Envía el estado de edición al template.
    }
    return render(request, 'template/profile.html', context)

@login_required
def lista_citas(request):
    doctor_instance = doctor.objects.get(id_usuario=request.user)

    doctor_paciente_list = doctor_paciente.objects.filter(id_doctor=doctor_instance)

    citas = cita.objects.filter(id_doctor_paciente__in=doctor_paciente_list).order_by('fecha', 'hora','detalle')

    context = {
        'citas': citas
    }

    return render(request, 'template/quotes.html', context)


@login_required
def editar_cita(request, cita_id):
    cita_instancia = get_object_or_404(cita, id=cita_id)

    if request.method == 'POST':
       form = CitaForm(request.POST, instance=cita_instancia)
       if form.is_valid():
            form.save()
            return redirect('editar_cita', cita_id=cita_id)

    else:
        form = CitaForm(instance=cita_instancia)
    return render(request, 'template/quotes.html',  {'form': form})


@login_required
def eliminar_cita(request, cita_id):
    cita_instancia = get_object_or_404(cita, id=cita_id)

    if request.method == 'POST':
        # Elimina la cita
        cita_instancia.delete()
        return redirect('lista_citas')

    context = {
        'cita': cita_instancia
    }
    return render(request, 'template/quotes.html', context)