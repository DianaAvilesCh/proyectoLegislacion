from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.perfil_doctor, name='perfil_doctor'),
    path('quotes/', views.lista_citas, name='lista_citas'),
    path('agregar/', views.agregar_cita, name='agregar_cita'),
    path('buscar/', views.obtener_pacientes, name='obtener_pacientes'),
    path('editar/<int:pk>/', views.editar_cita, name='editar_cita'),
    path('eliminar/<int:pk>/', views.eliminar_cita, name='eliminar_cita'),
    path('exportar-citas-pdf/', views.exportar_citas_pdf, name='exportar_citas_pdf'),
   # path('generar-citas/<int:paciente_id>/<str:fecha_desde>/<str:fecha_hasta>/', views.generar_pdf_citas,name='generar_citas')
]
