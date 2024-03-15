from django.contrib import admin
from primary.models import persona,doctor
from secondary.models import paciente
# Register your models here.
admin.site.register(persona)
admin.site.register(doctor)
admin.site.register(paciente)