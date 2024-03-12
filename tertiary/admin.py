from django.contrib import admin
from .models import Persona, Doctor, Paciente, Cita, DoctorPaciente

admin.site.register(Persona)
admin.site.register(Doctor)
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(DoctorPaciente)
