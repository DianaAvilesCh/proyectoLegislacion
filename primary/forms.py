# En forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import persona, doctor
import re

class PersonaForm(forms.ModelForm):
    class Meta:
        model = persona
        fields = ['dni', 'nombres', 'apellidos', 'correo', 'telefono', 'sexo']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['rec_senecyt', 'especialidad', 'institucion']

class CustomUserCreationForm(UserCreationForm):
    dni = forms.CharField(max_length=10)
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    correo = forms.EmailField(max_length=100)
    telefono = forms.CharField(max_length=10)
    sexo = forms.CharField(max_length=10)
    rec_senecyt = forms.CharField(max_length=15)
    especialidad = forms.CharField(max_length=100)
    institucion = forms.CharField(max_length=100)
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['password1', 'password2', 'dni', 'nombres', 'apellidos', 'correo', 'telefono', 'sexo', 'rec_senecyt', 'especialidad', 'institucion']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo Electrónico'
        self.fields['username'].help_text = 'Ingrese un correo electrónico válido.'
        self.fields['password2'].help_text = 'Repite la contraseña'

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['username'] = cleaned_data.get('correo', '')
    
    def clean_correo(self):
            correo = self.cleaned_data['correo']
            if User.objects.filter(persona__correo=correo).exists():
                raise forms.ValidationError('Este correo electrónico ya está en uso.')
            return correo
    def clean_dni(self):
            dni = self.cleaned_data['dni']
            if User.objects.filter(persona__dni=dni).exists():
                raise forms.ValidationError('La cédula ya existe. Por favor, ingrese otra')
            return dni
    def clean_rec_senecyt(self):
            rec_senecyt = self.cleaned_data['rec_senecyt']
            if User.objects.filter(doctor__rec_senecyt=rec_senecyt).exists():
                raise forms.ValidationError('El Reg. Senecyt ya existe. Por favor, ingrese otra')
            return rec_senecyt

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        errors = []
        # Verificar si la contraseña cumple con los requisitos
        if password1 and password2 and password1 != password2:
            errors.append("Las contraseñas no coinciden.")

        # Verificar si la contraseña tiene al menos 8 caracteres
        if password2 and len(password2) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r'[A-Z]', password2) or not re.search(r'[a-z]', password2) or not re.search(r'\d', password2) or not re.search(r'[+-/¡!@#$%^&*(),.?":{}|<>]', password2):
            errors.append("La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.")

        if errors:
            raise forms.ValidationError(errors)

        return password2
    
    def clean_rec_senecyt(self):
        rec_senecyt = self.cleaned_data.get('rec_senecyt')
        if len(rec_senecyt) > 15:
            raise forms.ValidationError('El Registro SENECYT debe tener como máximo 10 caracteres.')
        return rec_senecyt

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
