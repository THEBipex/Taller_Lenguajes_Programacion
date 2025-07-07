from django import forms
from .models import Taller

class ProponerTallerForm(forms.ModelForm):
    class Meta:
        model   = Taller
        fields  = ['titulo', 'fecha', 'duracion_horas', 'profesor', 'lugar', 'categoria']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }