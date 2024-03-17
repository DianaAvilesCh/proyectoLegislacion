from django.db import models
from primary.models import persona,doctor
# Create your models here.
class paciente(models.Model):
    id_persona = models.ForeignKey(persona,on_delete=models.CASCADE)
    domicilio = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(auto_now_add=False)
    numero_ficha = models.CharField(max_length=10)
    tipo_sangre = models.CharField(max_length=10)
    ant_personal = models.CharField(max_length=100, default='Ninguno')
    ant_familiar = models.CharField(max_length=100, default='Ninguno')

    def __str__(self):
            return f"{self.id_persona}"
    
class doctor_paciente(models.Model):
    id_doctor = models.ForeignKey(doctor,on_delete=models.CASCADE)
    id_paciente = models.ForeignKey(paciente,on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.id_doctor}"
        
class const_vitales(models.Model):
    id_paciente = models.ForeignKey(paciente,on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=False)
    hora = models.TimeField(default='00:00:00')
    temperatura = models.FloatField(null=True)
    presion_art = models.FloatField(null=True)
    pulse = models.FloatField(null=True)
    frec_respiratoria = models.FloatField(null=True)
    peso = models.FloatField(null=True)
    talla = models.FloatField(null=True)
    glucosa = models.FloatField(null=True)

    def __str__(self):
            return f"{self.id_paciente}"