from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from .utils import obtener_tipo_feriado

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    nombre_completo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_completo
    
class Taller(models.Model):
    ESTADO_CHOICES = [
            ('pendiente', 'Pendiente'),
            ('aceptado', 'Aceptado'),
            ('rechazado', 'Rechazado'),
    ]

    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    duracion_horas = models.FloatField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    observacion = models.TextField(null=True, blank=True)

    profesor = models.CharField(max_length=100)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    propuesto_por = models.ForeignKey('talleres.Usuario', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        tipo_feriado = obtener_tipo_feriado(self.fecha)

        if tipo_feriado == 'irrenunciable':
            self.estado = 'rechazado'
            self.observacion = "No se programan talleres en fereias irrenunciables."

        elif tipo_feriado == 'normal' and self.categoria.nombre != 'Aire Libre':
            self.estado = 'rechazado'
            self.observacion = "Solo se pograman takkeres al aire libre en feriados"
    def __str__(self):
        return self.titulo

class Usuario(AbstractUser):
    pass
