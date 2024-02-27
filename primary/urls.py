from django.urls import path,include
from primary import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', views.register, name='Registro'),
    path('login/', views.login, name='Login'),
    path('profile/', views.profile, name='perfil'),
]