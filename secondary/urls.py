from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/', views.patient, name='patient'),
    path('register_vitales/', views.register_vitales, name='register_vitales'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('signout', views.signout, name='signout'),
    path('update_patient/', views.update_patient, name='update_patient'),
]