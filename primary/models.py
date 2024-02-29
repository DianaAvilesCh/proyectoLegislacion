from django.db import models
from django.contrib.auth.models import User
# Create your models here.
   
class persona(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=10)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=10)
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return self.dni
    
class doctor(models.Model):
    id_persona = models.ForeignKey(persona,on_delete=models.CASCADE)
    rec_senecyt = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)

    def __str__(self):
         return f"{self.id_persona}"
    
class paciente(models.Model):
    id_persona = models.ForeignKey(persona,on_delete=models.CASCADE)
    domicilio = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(auto_now_add=False)
    numero_ficha = models.CharField(max_length=10)
    tipo_sangre = models.CharField(max_length=10)

    def __str__(self):
            return f"{self.id_persona}"
    
class doctor_paciente(models.Model):
    id_doctor = models.ForeignKey(doctor,on_delete=models.CASCADE)
    id_paciente = models.ForeignKey(paciente,on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.id_doctor}"