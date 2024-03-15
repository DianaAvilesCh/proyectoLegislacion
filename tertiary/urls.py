from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.perfil_doctor, name='perfil_doctor'),
    path('quotes/', views.lista_citas, name='lista_citas'),
    path('quotes/editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('quotes/eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),

]