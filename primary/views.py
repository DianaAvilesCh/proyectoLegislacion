from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PersonaForm, DoctorForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import persona, doctor
from django.contrib.auth.decorators import login_required

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

        if form.is_valid() and persona_form.is_valid():
            try:
                # Registro de usuario
                user = form.save()
                login(request, user)

                # Registro de persona asociada al usuario
                nueva_persona = persona_form.save(commit=False)
                nueva_persona.id_usuario = user
                nueva_persona.save()

                # Registro de doctor asociado a la persona
                nuevo_doctor = doctor_form.save(commit=False)
                nuevo_doctor.id_persona = nueva_persona
                nuevo_doctor.save()

                contexto['persona_form'] = persona_form
                contexto['doctor_form'] = doctor_form

                return redirect('login')
            except ValidationError as e:
                for field, messages in e.error_dict.items():
                    for message in messages:
                        form.add_error(field, message)
                        print(f"Error en el campo '{field}': {message}")
        else:
            contexto = {'form': form, 'persona_form': persona_form, 'doctor_form': doctor_form}
            return render(request, 'register.html', contexto)

    return render(request, 'register.html', contexto)


      
def login(request):
    return render(request, 'login.html')

@login_required
def profile(request):
    return render(request, 'profile.html')