from django.shortcuts import render, get_object_or_404
from primary.models import persona, doctor
from secondary.models import paciente, doctor_paciente

def dashboard(request):
    username = request.session.get('username', '')
    return render(request, 'dashboard.html',{'username': username})

def patient(request):
    username = request.session.get('username', '')
    print(username)
    persona_doctor = persona.objects.get(correo=username)
    doctor_obj = doctor.objects.get(id_persona=persona_doctor)
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
        
        return render(request, 'patient.html')
    else:
        relaciones_doctor_paciente = doctor_paciente.objects.filter(id_doctor=doctor_obj)
        lista_pacientes = []
        
        for relacion in relaciones_doctor_paciente:
            paciente_obj = paciente.objects.get(id=relacion.id_paciente_id)
            lista_pacientes.append(paciente_obj)
        print(lista_pacientes)
            
        return render(request, 'patient.html',{'pacientes': lista_pacientes})
