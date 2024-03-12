from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tertiary_personas')
    dni = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    sexo = models.CharField(max_length=10)

class Doctor(models.Model):
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='tertiary_personas')
    rec_senecyt = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)

class Paciente(models.Model):
    id_persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    domicilio = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    numero_ficha = models.CharField(max_length=50)
    tipo_sangre = models.CharField(max_length=5)

class DoctorPaciente(models.Model):
    id_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class Cita(models.Model):
    id_doctor_paciente = models.ForeignKey(DoctorPaciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    detalle = models.TextField()
