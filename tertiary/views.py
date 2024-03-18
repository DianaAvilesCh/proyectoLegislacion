from django.shortcuts import render, redirect, get_object_or_404
from primary.models import doctor
from secondary.models import doctor_paciente
from .models import cita
from django.contrib import messages
from .forms import CitaForm, DoctorForm, SeleccionPacienteForm
from primary.forms import PersonaForm
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
            messages.success(request, 'Datos editados con éxito.', extra_tags='correcto')
            return redirect('perfil_doctor')
        else:
            # Si el formulario no es válido, se mostrarán automáticamente los errores en el template.
            messages.error(request, 'Por favor, corrige los errores en el formulario.', extra_tags='error')

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
            messages.success(request, 'Cita actualizada con éxito.', extra_tags='correcto')

            return redirect('lista_citas')
        else:
            messages.error(request, 'Error al actualizar cita.', extra_tags='advertencia')
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
        messages.success(request, 'Cita eliminada con éxito.', extra_tags='correcto')
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
            messages.success(request, 'Cita registrada con éxito.', extra_tags='correcto')
            return redirect('lista_citas')
        else:
            messages.error(request, 'Error al registrar cita.', extra_tags='advertencia')
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


# REPORTE DE CITAS
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


def exportar_citas_pdf(request):
    # Obtener el doctor actual
    doctor_instance = doctor.objects.get(id_usuario=request.user)

    # Obtener la lista de pacientes del doctor
    doctor_paciente_list = doctor_paciente.objects.filter(id_doctor=doctor_instance)

    # Crear una lista para almacenar los datos de las citas por paciente
    datos_citas = []

    # Agregar encabezado a la lista de datos
    encabezado = ["Fecha", "Hora", "Detalle", "Nombre", "Apellido"]
    datos_citas.append(encabezado)

    for relacion in doctor_paciente_list:
        citas_paciente = cita.objects.filter(id_doctor_paciente=relacion)
        for c in citas_paciente:
            # Dividir el detalle en líneas
            detalle_lines = [c.detalle[i:i + 50] for i in range(0, len(c.detalle), 50)]  # Cambia 50 al ancho deseado
            for i, line in enumerate(detalle_lines):
                if i == 0:
                    datos_citas.append([c.fecha, c.hora, line, c.id_doctor_paciente.id_paciente.id_persona.nombres,
                                        c.id_doctor_paciente.id_paciente.id_persona.apellidos])
                else:
                    datos_citas.append(["", "", line, "", ""])

    # Crear un documento PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="citas_por_paciente.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Crear una tabla con los datos de las citas por paciente
    tabla = Table(datos_citas)
    tabla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Agregar encabezado al documento
    styles = getSampleStyleSheet()
    encabezado = Paragraph("<b>Institución " + doctor_instance.institucion + "</b>", styles['Title'])
    doctor_datos = Paragraph(
        "<b>Doctor: </b>" + doctor_instance.id_persona.nombres + "   " + doctor_instance.id_persona.apellidos + "",
        styles['Normal'])
    direccion = Paragraph("<b>Dirección:</b> 123 Calle Principal, Ciudad, País", styles['Normal'])
    especialidad = Paragraph("<b>Especialidad:</b> " + doctor_instance.especialidad + "", styles['Normal'])
    contacto = Paragraph(
        "<b>Teléfono: </b>" + doctor_instance.id_persona.telefono + "      <b> Correo electrónico:</b> " + doctor_instance.id_persona.correo + "",
        styles['Normal'])
    espacio = Spacer(1, 10)

    # Adjuntar encabezado y tabla al documento
    elementos = [encabezado, doctor_datos, direccion, especialidad, contacto, espacio, tabla]
    doc.build(elementos)

    return response

# mas reportes

# def seleccionar_paciente(request):
#     if request.method == 'POST':
#         form = SeleccionPacienteForm(request.POST)
#         if form.is_valid():
#             paciente_id = form.cleaned_data['paciente']
#             fecha_desde = form.cleaned_data['fecha_desde']
#             fecha_hasta = form.cleaned_data['fecha_hasta']
#             return redirect('generar_citas', paciente_id=paciente_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
#     else:
#         form = SeleccionPacienteForm()
#     pacientes = obtener_pacientes(request)
#     return render(request, 'template/quotes.html', {'form': form, 'pacientes': pacientes})
#
#
# def generar_pdf_citas(request, paciente_id, fecha_desde, fecha_hasta):
#     # Filtrar las citas por paciente y fecha
#     fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
#     fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
#     citas = cita.objects.filter(id_doctor_paciente__id_paciente=paciente_id, fecha__range=(fecha_desde, fecha_hasta))
#
#
#     # Crear un documento PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="citas_paciente.pdf"'
#     doc = SimpleDocTemplate(response, pagesize=letter)
#
#     # Crear una tabla con los datos de las citas del paciente
#     datos_citas = [["Fecha", "Hora", "Detalle"]]  # Encabezado de la tabla
#     for cita in citas:
#         datos_citas.append([cita.fecha, cita.hora, cita.detalle])
#
#     tabla = Table(datos_citas)
#
#     # Establecer estilos para la tabla
#     tabla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
#
#     # Adjuntar la tabla al documento PDF
#     elementos = [tabla]
#     doc.build(elementos)
#
#     return response
