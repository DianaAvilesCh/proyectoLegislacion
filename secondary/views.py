from django.shortcuts import render, redirect
from django.contrib import messages
from primary.models import persona, doctor
from secondary.models import paciente, doctor_paciente, const_vitales

def dashboard(request):
    username = request.session.get('username', '')
    return render(request, 'dashboard.html',{'username': username})

def patient(request):
    username = request.session.get('username', '')
    print(username)
    persona_doctor = persona.objects.get(correo=username)
    doctor_obj = doctor.objects.get(id_persona=persona_doctor)

    # Función o bloque para obtener la lista de pacientes
    def obtener_lista_pacientes():
        relaciones_doctor_paciente = doctor_paciente.objects.filter(id_doctor=doctor_obj)
        lista_pacientes = []
        for relacion in relaciones_doctor_paciente:
            paciente_obj = paciente.objects.get(id=relacion.id_paciente_id)
            lista_pacientes.append(paciente_obj)
        return lista_pacientes

    if request.method == 'POST':
        dni = request.POST.get('dni')
        nombres = request.POST.get('name')
        apellidos = request.POST.get('lastname')
        correo = request.POST.get('email')
        telefono = request.POST.get('phone')
        sexo = request.POST.get('sex')

        domicilio = request.POST.get('address')
        fecha_nacimiento = request.POST.get('birthdate')
        tipo_sangre = request.POST.get('blood')

        # Crear y guardar la instancia de Persona
        persona_instancia = persona(correo=correo, dni=dni, nombres=nombres, apellidos=apellidos, telefono=telefono, sexo=sexo)
        persona_instancia.save()

        # Crear la instancia de Paciente sin numero_ficha y guardar
        paciente_instancia = paciente(id_persona=persona_instancia, domicilio=domicilio, fecha_nacimiento=fecha_nacimiento, tipo_sangre=tipo_sangre)
        paciente_instancia.save()
        
        paciente_instancia.numero_ficha = str(paciente_instancia.id).zfill(5)
        paciente_instancia.save()
        
        paciente_instancia = doctor_paciente(id_doctor=doctor_obj, id_paciente=paciente_instancia)
        paciente_instancia.save()

        # Actualizar la lista de pacientes después de agregar uno nuevo
        lista_pacientes = obtener_lista_pacientes()
        return render(request, 'patient.html', {'pacientes': lista_pacientes})
    else:
        lista_pacientes = obtener_lista_pacientes()
        return render(request, 'patient.html', {'pacientes': lista_pacientes})
    

def register_vitales(request):
    if request.method == 'POST':
        id_paciente = request.POST.get('idSeleccionado')
        paciente_fill = paciente.objects.get(id=id_paciente)

        fecha = request.POST.get('date')
        hora = request.POST.get('time')
        temperatura = request.POST.get('temp')
        presion_art = request.POST.get('arterial')
        pulse = request.POST.get('pulso')
        frec_cardiaca = request.POST.get('cardiaca')
        peso = request.POST.get('peso')
        glucosa = request.POST.get('glucosa')

        # Crear y guardar la instancia de Persona
        constantes_vitales = const_vitales(id_paciente = paciente_fill, fecha = fecha, hora=hora, 
                                           temperatura=temperatura,presion_art=presion_art, pulse=pulse,
                                           frec_cardiaca=frec_cardiaca, peso=peso, glucosa=glucosa)
        constantes_vitales.save()
        
        messages.success(request, '¡Registro exitoso!', extra_tags ='correcto')

    return redirect(patient)