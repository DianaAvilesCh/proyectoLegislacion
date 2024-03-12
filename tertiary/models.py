from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personas')
    dni = models.CharField(max_length=10, unique=True)  # Asumiendo que DNI debe ser único
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)  # La longitud máxima por defecto es adecuada y has hecho bien en hacerlo único
    telefono = models.CharField(max_length=15)  # Considera la longitud adecuada para los números internacionales si es necesario
    sexo = models.CharField(max_length=10)  # Considera usar choices si tienes un conjunto fijo de opciones

    def __str__(self):
        return self.dni

class Doctor(models.Model):
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='doctores')
    rec_senecyt = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_persona.dni}"  # Esto asume que quieres mostrar el DNI de la Persona asociada
