from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Taller, Profesor, Lugar, Categoria, Usuario

# Register your models here.

class CustomUsuarioAdmin(UserAdmin):
    model = Usuario
    list_display    = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields   = ('username', 'email')
    ordering        = ('username',)

admin.site.register(Usuario, CustomUsuarioAdmin)
admin.site.register(Taller)
admin.site.register(Profesor)
admin.site.register(Lugar)
admin.site.register(Categoria)