from django import forms
from primary.models import persona, doctor
from tertiary.models import cita

class PersonaForm(forms.ModelForm):
    class Meta:
        model = persona
        fields = ['dni', 'nombres', 'apellidos', 'correo', 'telefono', 'sexo']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['rec_senecyt', 'especialidad', 'institucion']

class CitaForm(forms.ModelForm):
    class Meta:
        model = cita
        fields = ['fecha', 'hora', 'detalle']
