from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Ciudadano, SolicitudRetiro, Material

class RegistroCiudadanoForm(forms.ModelForm):
    class Meta:
        model   = Ciudadano
        fields  = ['direccion', 'telefono']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle Numero, Comuna'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            })
        }

class SolicitudRetiroForm(forms.ModelForm):
    class Meta:
        model   = SolicitudRetiro
        fields  = ['material', 'cantidad', 'fecha_estimada']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'fecha_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos solo materiales activos si es necesario
        self.fields['material'].queryset = Material.objects.all() 