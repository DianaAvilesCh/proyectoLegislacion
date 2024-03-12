from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.perfil_doctor, name='perfil_doctor'),
    path('quotes/', views.lista_citas, name='lista_citas'),
##  path('quotes/nueva/', views.nueva_cita, name='nueva_cita'),
]