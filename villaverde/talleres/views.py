from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Taller, Categoria
from .serializers import TallerSerializer
from datetime import date

# Create your views here.

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