from django.db import models
from django.contrib.auth.models import User
# Create your models here.
   
class persona(models.Model):
    
    dni = models.CharField(max_length=10)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=10)
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}"
    
class doctor(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_persona = models.ForeignKey(persona,on_delete=models.CASCADE)
    rec_senecyt = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)

    def __str__(self):
         return f"{self.id_persona}"
    
