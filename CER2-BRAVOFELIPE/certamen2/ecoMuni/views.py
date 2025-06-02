from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Count, Avg, F
from datetime import timedelta
from django.utils import timezone
from .forms import RegistroCiudadanoForm, SolicitudRetiroForm
from .models import Material, SolicitudRetiro,Ciudadano

def home (request):
    materiales = Material.objects.all()
    return render(request, 'home.html', {'materiales': materiales})

@login_required
def perfil_ciudadano(request):
    solicitudes = SolicitudRetiro.objects.filter(ciudadano=request.user.ciudadano)
    return render(request, 'perfil_ciudadano.html', {'solicitudes': solicitudes})

def registro(request):
    if request.method == 'POST':
        user_form       = UserCreationForm(request.POST)
        ciudadano_form  = RegistroCiudadanoForm(request.POST)

        if user_form.is_valid() and ciudadano_form.is_valid():
            user = user_form.save()
            ciudadano = ciudadano_form.save(commit=False)
            ciudadano.usuario = user
            ciudadano.save()
            return redirect('login.html')
    else:
        user_form       = UserCreationForm()
        ciudadano_form  = RegistroCiudadanoForm()
    
    return render(request, 'registro.html', {
        'user_form': user_form,
        'ciudadano_form': ciudadano_form
    })

@login_required
def nueva_solicitud(request):
    if request.method == 'POST':
        form = SolicitudRetiroForm(request.POST)
        if form.is_valid():
            solicitud           = form.save(commit=False)
            solicitud.ciudadano = request.user.ciudadano
            solicitud.save()
            return redirect('perfil_ciudadano')
    else:
        form = SolicitudRetiroForm()

    return render(request, 'nueva_solicitud.html', {'form': form})

def metricas_publicas(request):
    """Vista para mostrar las métricas públicas del sistema"""
    # Fecha actual y hace 30 días
    hoy = timezone.now()
    hace_30_dias = hoy - timedelta(days=30)
    
    # 1. Cantidad de solicitudes por mes
    solicitudes_mes = SolicitudRetiro.objects.filter(
        fecha_solicitud__gte=hace_30_dias
    ).count()
    
    # 2. Materiales más reciclados (top 3)
    materiales_populares = Material.objects.annotate(
        total_solicitudes=Count('solicitudretiro')
    ).order_by('-total_solicitudes')[:3]
    
    # Calcular porcentaje para cada material
    total_solicitudes = sum(m.total_solicitudes for m in materiales_populares)
    for material in materiales_populares:
        if total_solicitudes > 0:
            material.porcentaje = round((material.total_solicitudes / total_solicitudes) * 100)
        else:
            material.porcentaje = 0

    # Filtrar solo solicitudes completadas con fecha_completada no nula
    solicitudes_completadas = SolicitudRetiro.objects.filter(
        estado='C',
        fecha_completada__isnull=False
    )
    # 3. Tiempo promedio de retiro (en días)
    tiempo_promedio = solicitudes_completadas.aggregate(
        promedio=Avg(F('fecha_completada') - F('fecha_solicitud'))
    )

    avg_dias = tiempo_promedio['promedio'].days if tiempo_promedio['promedio'] else 0

    # 4. Últimas solicitudes completadas
    ultimas_solicitudes = SolicitudRetiro.objects.filter(
        estado='C'
    ).order_by('-fecha_completada')[:10]
    
    # Calcular días de retiro para cada solicitud
    for solicitud in ultimas_solicitudes:
        solicitud.tiempo_retiro = (solicitud.fecha_completada - solicitud.fecha_solicitud).days
    
    context = {
        'solicitudes_mes': solicitudes_mes,
        'materiales_populares': materiales_populares,
        'tiempo_promedio': avg_dias,
        'total_materiales': total_solicitudes,
        'ultimas_solicitudes': ultimas_solicitudes,
    }
    return render(request, 'metricas.html', context)

def materiales_aceptados(request):
    """Vista para mostrar todos los materiales aceptados"""
    materiales = Material.objects.all()
    return render(request, 'materiales.html', {'materiales': materiales})

def puntos_limpios(request):
    """Vista para mostrar información de puntos limpios"""
    # Datos estáticos - puedes convertir esto en un modelo después
    puntos = [
        {
            'nombre': 'Centro de Reciclaje Municipal',
            'direccion': 'Av. Principal 1234, Comuna Central',
            'horario': 'Lunes a Viernes 8:00 - 18:00 hrs'
        },
        {
            'nombre': 'Punto Limpio Norte',
            'direccion': 'Calle Secundaria 567, Sector Norte',
            'horario': 'Martes a Sábado 9:00 - 17:00 hrs'
        }
    ]
    return render(request, 'puntos_limpios.html', {'puntos': puntos})

def custom_login(request):
    """Vista personalizada para el login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    """Vista personalizada para logout"""
    logout(request)
    return redirect('home')
