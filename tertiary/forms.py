from django import forms
from .models import Persona, Doctor, Cita

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['dni', 'nombres', 'apellidos', 'correo', 'telefono', 'sexo']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['rec_senecyt', 'especialidad', 'institucion']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'detalle']
