from django.shortcuts import render, redirect, get_object_or_404
from primary.models import doctor, persona
from secondary.models import doctor_paciente, paciente
from tertiary.models import cita
from django.contrib import messages
from .forms import DoctorForm, CitaForm, PersonaForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
    citas_paciente = []

    for relacion in doctor_paciente_list:
        citas_paciente.extend(cita.objects.filter(id_doctor_paciente=relacion))

    return render(request, 'template/quotes.html', {'citas': citas_paciente})


@login_required
def editar_cita(request, pk):
    cita_instancia = get_object_or_404(cita, pk=pk)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita_instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada con éxito.')
            return redirect('lista_citas')
        else:
            messages.error(request, 'Por favor corrija los errores abajo.')
            # Aquí podrías optar por devolver el usuario a una vista detallada de la cita con el formulario abierto
            # Pero necesitarías cambiar la lógica para mantener la página y abrir el modal.
    else:
        form = CitaForm(instance=cita_instancia)
    # Si no es POST o si el formulario no es válido, simplemente redirige para mantener la simplicidad.
    return redirect('lista_citas', {'form': form})


@login_required
def eliminar_cita(request, pk):
    cita_instancia = get_object_or_404(cita, pk=pk)

    if request.method == 'POST':
        cita_instancia.delete()
        messages.success(request, 'Cita eliminada con éxito.')
        return redirect('lista_citas')

    return render(request, 'template/quotes.html', {'cita': cita_instancia})


@login_required
def agregar_cita(request):
    doctor_instance = doctor.objects.get(id_usuario=request.user)
    doctor_paciente_list = doctor_paciente.objects.filter(id_doctor=doctor_instance)
    print(doctor_paciente_list)
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita_instancia = form.save(commit=False)
            id_doctor_paciente = request.POST.get('doctor_paciente')  # Asigna el primer doctor_paciente de la lista
            print("Valor de doctor_paciente:", id_doctor_paciente)
            doctor_paciente_instancia = get_object_or_404(doctor_paciente, id=id_doctor_paciente)
            cita_instancia.id_doctor_paciente = doctor_paciente_instancia
            cita_instancia.save()
            messages.success(request, 'Cita agregada con éxito.')
            return redirect('lista_citas')
        else:
            messages.error(request, 'Por favor corrija los errores abajo.')
    else:
        form = CitaForm()

    return render(request, 'template/quotes.html', {'form': form, 'doctor_paciente_list': doctor_paciente_list})


def obtener_pacientes(request):
    doctor_instance = doctor.objects.get(id_usuario=request.user)
    doctor_paciente_list = doctor_paciente.objects.filter(id_doctor=doctor_instance)
    pacientes = [
        {
            'id': relacion.id_paciente.id,
            'id_persona': {
                'nombres': relacion.id_paciente.id_persona.nombres,
                'apellidos': relacion.id_paciente.id_persona.apellidos
            }
        }
        for relacion in doctor_paciente_list
    ]
    return JsonResponse(pacientes, safe=False)


def quotes(request):
    return render(request, 'template/quotes.html')
