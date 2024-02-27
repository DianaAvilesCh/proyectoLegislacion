from django import forms
from .models import persona,doctor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    rec_senecyt = forms.CharField(max_length=10)
    especialidad = forms.CharField(max_length=100)
    institucion = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'dni', 'nombres', 'apellidos', 'correo', 'telefono', 'sexo', 'rec_senecyt', 'especialidad', 'institucion']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Actualizar el campo username para usar el correo electrónico
        self.fields['username'].label = 'Correo Electrónico'
        self.fields['username'].help_text = 'Ingrese un correo electrónico válido.'
        self.fields['password2'].help_text = 'Repite la contraseña'

    def clean_username(self):
        # Validar que el correo no esté en uso
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        print(password1,password2)
        errors = []
        # Verificar si la contraseña cumple con los requisitos
        if password1 and password2 and password1 != password2:
            errors.append("Las contraseñas no coinciden.")

        # Verificar si la contraseña tiene al menos 8 caracteres
        if password2 and len(password2) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r'[A-Z]', password2) or not re.search(r'[a-z]', password2) or not re.search(r'\d', password2) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password2):
            errors.append("La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.")

        if errors:
            raise forms.ValidationError(errors)

        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user