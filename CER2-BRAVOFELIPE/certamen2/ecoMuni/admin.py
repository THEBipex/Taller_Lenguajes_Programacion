from django.contrib import admin
from .models import Material, Ciudadano, Operario, SolicitudRetiro

@admin .register(SolicitudRetiro)
class SolicitudRetiroAdmin(admin.ModelAdmin):
    list_display    = ('id', 'ciudadano', 'material', 'cantidad', 'fecha_estimada', 'estado', 'operario')
    list_filter     = ('estado', 'material')
    search_fields   = ('ciudadano__usuario__username', 'ciudadano__usuario__first_name', 'ciudadano__usuario__last_name')
    actions         = ['asignar_operario']

    def asignar_operario(self, request, queryset):
        operario_id = request.POST.get('operario')
        if operario_id:
            operario    = Operario.objects.get(id=operario_id)
            queryset.update(operario=operario, estado ='R')
            self.message_user(request, f"Solicitudes asignadas a {operario}")
    asignar_operario.short_description = "Asignar operario a solicitudes seleccionadas"

admin.site.register(Material)
admin.site.register(Ciudadano)
admin.site.register(Operario)
# Register your models here.
