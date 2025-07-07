from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class Material(models.Model):
    codigo      = models.CharField(max_length=5, primary_key=True)
    nombre      = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Ciudadano(models.Model):

    usuario         = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre          = models.CharField(max_length=50)
    apellido        = models.CharField(max_length=70)
    direccion       = models.CharField(max_length=200)
    telefono        = models.CharField(max_length=15)
    fecha_registro  = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Operario(models.Model):
    usuario     = models.OneToOneField(User, on_delete=models.CASCADE)
    capacidad   = models.PositiveBigIntegerField(default=5)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

class SolicitudRetiro(models.Model):
    ESTADOS = {
        ('P','Pendiente'),
        ('R','En ruta'),
        ('C','Completada'),
    }

    ciudadano   = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)
    material    = models.ForeignKey(Material, on_delete=models.PROTECT)
    cantidad    = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_estimada  = models.DateField()
    estado      = models.CharField(max_length=1, choices=ESTADOS, default='P')
    fecha_completada = models.DateTimeField(null=True, blank=True)  # <-- Añade este campo
    operario    = models.ForeignKey(Operario, on_delete=models.SET_NULL, null=True, blank=True)
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return f"Solicitud #{self.id} - {self.ciudadano}" 