from django.db import models
from secondary.models import doctor_paciente
from django.contrib.auth.models import User

class cita(models.Model):
    id_doctor_paciente = models.ForeignKey(doctor_paciente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=False)
    hora = models.TimeField(default='00:00:00')
    detalle = models.TextField(max_length=300)
