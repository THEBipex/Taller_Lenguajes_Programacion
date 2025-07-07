"""
URL configuration for certamen2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ecoMuni import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Páginas principales
    path('', views.home, name='home'),
    path('metricas/', views.metricas_publicas, name='metricas'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Vistas de ciudadano
    path('perfil/', views.perfil_ciudadano, name='perfil_ciudadano'),
    path('nueva-solicitud/', views.nueva_solicitud, name='nueva_solicitud'),
    
    # Páginas estáticas 
    path('materiales/', views.materiales_aceptados, name='materiales'),
    path('puntos-limpios/', views.puntos_limpios, name='puntos_limpios'),
]
