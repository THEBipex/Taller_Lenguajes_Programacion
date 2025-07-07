from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ciudadano, SolicitudRetiro, Material, User

class CreacionUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
class RegistroCiudadanoForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        })
    )
    apellido = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        })
    )
    direccion = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle Numero, Comuna'
        })
    )
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56912345678'
        })
    )

    class Meta:
        model = Ciudadano
        fields = ['nombre', 'apellido', 'direccion', 'telefono']
        
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