from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Taller, Categoria
from .serializers import TallerSerializer
from datetime import date
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'talleres/login.html'

    def get_success_url(self):
        user = self.request.user
        next_url = self.request.GET.get('next')
        
        # Junta de Vecinos: is_staff=FALSE, is_superuser=False
        if not user.is_staff and not user.is_superuser:
            return next_url or self.request.META.get('') or '/'

        # Funcionarios o administradores: acceso al pandel de gestion
        return '/admin'

class TallerViewSet(viewsets.ModelViewSet):
    queryset            = Taller.objects.all()
    serializer_class    = TallerSerializer
    permission_classes  = [permissions.IsAuthenticated]
    
def talleres_disponibles(request):
    talleres        = Taller.objects.filter(estado='aceptado', fecha__gt=date.today())
    categorias      = Categoria.objects.all()
    categoria_id    = request.GET.get('categoria')

    if categoria_id:
        talleres = talleres.filter(categoria_id=categoria_id)

    return render(request, 'talleres/lista_talleres.html', {
        'talleres':     talleres,
        'categorias':   categorias,
    })

def home(request):
    return render(request, 'talleres/home.html')