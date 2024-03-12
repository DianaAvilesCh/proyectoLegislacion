from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PersonaForm, DoctorForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    return render(request, 'sections.html')

def register(request):
    contexto = {}
    form = CustomUserCreationForm()
    persona_form = PersonaForm()
    doctor_form = DoctorForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        persona_form = PersonaForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if form.is_valid() and persona_form.is_valid() and doctor_form.is_valid():
            try:
                # Registro de usuario
                user = form.save(commit=False)
                user.username = form.cleaned_data['correo']
                user.save()
                login(request, user)

                # Registro de persona
                nueva_persona = persona_form.save(commit=False)                
                nueva_persona.save()

                # Registro de doctor asociado a la persona
                nuevo_doctor = doctor_form.save(commit=False)
                nuevo_doctor.id_persona = nueva_persona
                nuevo_doctor.id_usuario = user
                nuevo_doctor.save()

                contexto['persona_form'] = persona_form
                contexto['doctor_form'] = doctor_form

                return JsonResponse({'redirect_url': 'login_custom'})
            except ValidationError as e:
                for field, messages in e.error_dict.items():
                    for message in messages:
                        form.add_error(field, message)
                        print(f"Error en el campo '{field}': {message}")
        else:
            response = render(request, 'register.html', {'form': form, 'persona_form': persona_form, 'doctor_form': doctor_form})
            return response

    contexto = {'form': form, 'persona_form': persona_form, 'doctor_form': doctor_form}
    return render(request, 'register.html', contexto)

      
def login_custom(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse({'redirect_url': 'profile'})
    else:
        form = AuthenticationForm()

    return render(request, 'login_custom.html', {'form': form})



def profile(request):
    return render(request, 'profile.html')