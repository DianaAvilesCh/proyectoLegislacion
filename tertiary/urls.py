from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.perfil_doctor, name='perfil_doctor'),
    path('quotes/', views.lista_citas, name='lista_citas'),
    path('agregar/', views.agregar_cita, name='agregar_cita'),
    path('buscar/', views.obtener_pacientes, name='obtener_pacientes'),
    path('editar/<int:pk>/', views.editar_cita, name='editar_cita'),
    path('eliminar/<int:pk>/', views.eliminar_cita, name='eliminar_cita'),

]
