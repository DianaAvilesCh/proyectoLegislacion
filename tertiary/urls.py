from django.urls import path
from . import views
urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('citas/', views.citas, name='citas')
]