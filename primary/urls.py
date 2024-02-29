from django.urls import path,include
from primary import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', views.register, name='Registro'),
    path('login_custom/', views.login_custom, name='login_custom'),
    path('profile/', views.profile, name='profile'),
]