from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from primary.models import persona, doctor
from secondary.models import paciente, doctor_paciente, const_vitales

@login_required
def dashboard(request):
    username = request.session.get('username', '')
    return render(request, 'dashboard.html',{'username': username})

@login_required
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
        antPerson = request.POST.get('antPerson')
        antFam = request.POST.get('antFam')
        
        correo_existente = persona.objects.filter(correo=correo).exists()
        if correo_existente:
            messages.error(request, 'El correo electrónico ingresado ya existe.', extra_tags='ojo')
            lista_pacientes = obtener_lista_pacientes()
            return render(request, 'patient.html', {'pacientes': lista_pacientes})
        
        dni_existente = persona.objects.filter(dni=dni).exists()
        if dni_existente:
            messages.error(request, 'El DNI ingresado ya está registrado.', extra_tags='ojo')
            lista_pacientes = obtener_lista_pacientes()
            return render(request, 'patient.html', {'pacientes': lista_pacientes})

        # Crear y guardar la instancia de Persona
        persona_instancia = persona(correo=correo, dni=dni, nombres=nombres, apellidos=apellidos, telefono=telefono, sexo=sexo)
        persona_instancia.save()

        # Crear la instancia de Paciente sin numero_ficha y guardar
        paciente_instancia = paciente(id_persona=persona_instancia, domicilio=domicilio, fecha_nacimiento=fecha_nacimiento, tipo_sangre=tipo_sangre, ant_personal = antPerson, ant_familiar = antFam)
        paciente_instancia.save()
        
        paciente_instancia.numero_ficha = str(paciente_instancia.id).zfill(5)
        paciente_instancia.save()
        
        paciente_instancia = doctor_paciente(id_doctor=doctor_obj, id_paciente=paciente_instancia)
        paciente_instancia.save()

        # Actualizar la lista de pacientes después de agregar uno nuevo
        lista_pacientes = obtener_lista_pacientes()
        messages.success(request, '¡Registro exitoso!', extra_tags ='correcto')
        return render(request, 'patient.html', {'pacientes': lista_pacientes})
    else:
        lista_pacientes = obtener_lista_pacientes()
        return render(request, 'patient.html', {'pacientes': lista_pacientes})
    
@login_required
def register_vitales(request):
    if request.method == 'POST':
        id_paciente = request.POST.get('idSeleccionado')
        paciente_fill = paciente.objects.get(id=id_paciente)

        fecha = request.POST.get('date')
        hora = request.POST.get('time')
        temperatura = request.POST.get('temp')
        presion_art = request.POST.get('arterial')
        pulse = request.POST.get('pulso')
        frec_respiratoria = request.POST.get('respiratoria')
        peso = request.POST.get('peso')
        talla = request.POST.get('talla')
        glucosa = request.POST.get('glucosa')

        # Crear y guardar la instancia de Persona
        constantes_vitales = const_vitales(id_paciente = paciente_fill, fecha = fecha, hora=hora, 
                                           temperatura=temperatura,presion_art=presion_art, pulse=pulse,
                                           frec_respiratoria=frec_respiratoria, peso=peso,talla = talla, glucosa=glucosa)
        constantes_vitales.save()
        
        messages.success(request, '¡Registro exitoso!', extra_tags ='correcto')

    return redirect(patient)

@login_required
def detail(request, id):
    spaciente = paciente.objects.get(id=id)
    #dpersona = persona.objects.get(id_paciente=spaciente)
    
    constantes = const_vitales.objects.filter(id_paciente=spaciente)
    constantes_lista = [constante for constante in constantes]
    
    # Corregido: Combina 'spaciente' y 'constantes_lista' en un solo diccionario
    context = {
        'datos': spaciente,
        'constantes': constantes_lista
    }

    return render(request, 'detail_patient.html', context)

def signout(request):
    logout(request)
    return redirect('home')

@login_required
def delete(request, id):
    try:
        spaciente = paciente.objects.get(id=id)
        spersona = persona.objects.get(id=spaciente.id_persona_id)
        spersona.delete()
        # Redirige a otra página, como la lista de pacientes, después de borrar
        return redirect(patient)
    except paciente.DoesNotExist:
        messages.success(request, 'Ha ocurrido un error', extra_tags ='error')
        return redirect(patient)
    
@login_required
def update_patient(request):
    if request.method == 'POST':

        did = request.POST.get('did')
        dni = request.POST.get('dni')
        nombres = request.POST.get('name')
        apellidos = request.POST.get('lastname')
        correo = request.POST.get('email')
        telefono = request.POST.get('phone')
        sexo = request.POST.get('sex')
        domicilio = request.POST.get('address')
        fecha_nacimiento = request.POST.get('birthdate')
        tipo_sangre = request.POST.get('blood')
        antPerson = request.POST.get('antPerson')
        antFam = request.POST.get('antFam')
        
        try:
            paciente_instancia = paciente.objects.get(id=did)
        except persona.DoesNotExist:
            messages.error(request, 'Paciente no encontrado.', extra_tags='error')
            return redirect(patient)
        
        # Obtener y actualizar datos de Paciente, asumiendo relación uno a uno
        paciente_instancia.domicilio = domicilio
        paciente_instancia.fecha_nacimiento = fecha_nacimiento
        paciente_instancia.tipo_sangre = tipo_sangre
        paciente_instancia.ant_personal = antPerson
        paciente_instancia.ant_familiar = antFam
        paciente_instancia.save()
        
        # Actualizar datos de Persona
        persona_instancia = persona.objects.get(id=paciente_instancia.id_persona_id)
        
        # if persona_instancia.correo == correo:
        #     messages.error(request, 'El correo electrónico ingresado ya existe.', extra_tags='ojo')
        #     return redirect(detail, id=paciente_instancia.id) 
        
        # if persona_instancia.dni == dni:
        #     messages.error(request, 'El DNI ingresado ya está registrado.', extra_tags='ojo')
        #     return redirect(detail, id=paciente_instancia.id) 
        
        persona_instancia.nombres = nombres
        persona_instancia.apellidos = apellidos
        persona_instancia.dni = dni
        persona_instancia.correo = correo
        persona_instancia.telefono = telefono
        persona_instancia.sexo = sexo
        persona_instancia.save()

        

        messages.success(request, 'Paciente actualizado correctamente.', extra_tags='correcto')
        return redirect(detail, id=paciente_instancia.id)  
    else:
        messages.error(request, 'Ha ocurrido un error.', extra_tags='error')
        return redirect(patient) 
    
@login_required
def update_vitales(request):
    if request.method == 'POST':

        id_const = request.POST.get('idSeleccionado')
        id_pac = request.POST.get('idpac')
        fecha = request.POST.get('date')
        hora = request.POST.get('time')
        temperatura = request.POST.get('temp')
        presion_art = request.POST.get('arterial')
        pulse = request.POST.get('pulso')
        frec_respiratoria = request.POST.get('respiratoria')
        peso = request.POST.get('peso')
        talla = request.POST.get('talla')
        glucosa = request.POST.get('glucosa')

        try:
            conts_instancia = const_vitales.objects.get(id=id_const)
        except persona.DoesNotExist:
            messages.error(request, 'Constante Vital no encontrado.', extra_tags='error')
            return redirect(patient)
        
        # Obtener y actualizar datos de Paciente, asumiendo relación uno a uno
        conts_instancia.fecha = fecha
        conts_instancia.hora = hora
        conts_instancia.temperatura = temperatura
        conts_instancia.presion_art = presion_art
        conts_instancia.pulse = pulse
        conts_instancia.frec_respiratoria = frec_respiratoria
        conts_instancia.peso = peso
        conts_instancia.talla = talla
        conts_instancia.glucosa = glucosa
        conts_instancia.save()
        

        messages.success(request, 'Constante Vital actualizada correctamente.', extra_tags='correcto')
        return redirect(detail, id=id_pac)  
    else:
        messages.error(request, 'Ha ocurrido un error.', extra_tags='error')
        return redirect(patient) 