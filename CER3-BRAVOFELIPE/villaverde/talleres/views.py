from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views import View
from .serializers import TallerSerializer, PropuestaTallerSerializer
from .models import Taller, Categoria
from .forms import ProponerTallerForm
from datetime import date
import requests


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ProponerTallerView(View):
    def get(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return redirect('home')
        
        form = ProponerTallerForm()
        return render(request, 'talleres/proponer_taller.html', {'form': form})
    
    def post(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return redirect('home')
        
        form = ProponerTallerForm(request.POST)
        if form.is_valid():
            # Llamar a la API interna
            data    = form.cleaned_data
            token   = request.session.get('token', None)

            response = requests.post(
                request.build_absolute_uri('/api/proponer-taller/'),
                data=data,
                cookies=request.COOKIES # pasa sesion autenticada
            )

            if response.status_code in [200, 201]:
                return redirect('home')
        
        return render(request, 'talleres/proponer_taller.html', {'form': form, 'error': True})
    
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

class ProponerTallerAPI(generics.CreateAPIView):
    serializer_class    = PropuestaTallerSerializer
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = Taller.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "Este endpoint es solo para enviar propuesta de taller via POST."})
    
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