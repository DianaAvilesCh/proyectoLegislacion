from django.contrib import admin
from primary.models import persona, doctor
from secondary.models import paciente, doctor_paciente

admin.site.register(persona)
admin.site.register(doctor)
admin.site.register(paciente)
admin.site.register(doctor_paciente)
