from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/', views.patient, name='patient'),
    path('register_vitales/', views.register_vitales, name='register_vitales'),
]