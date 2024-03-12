from django.db import models
from secondary.models import doctor_paciente
from django.contrib.auth.models import User

class cita(models.Model):
    id_doctor_paciente = models.ForeignKey(doctor_paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    detalle = models.TextField()
