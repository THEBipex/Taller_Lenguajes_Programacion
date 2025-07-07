from rest_framework import serializers
from .models import Taller, Profesor, Lugar, Categoria

        
class PropuestaTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Taller
        fields  = ['titulo', 'fecha', 'duracion_horas', 'profesor', 'lugar', 'categoria']

    def create(self, validated_data):
        user = self.context['request'].user
        return Taller.objects.create(propuesto_por=user, **validated_data)
        
class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Profesor
        fields  = ['id', 'nombre']

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ['id', 'nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class TallerSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer()
    lugar = LugarSerializer()
    categoria = CategoriaSerializer()

    class Meta:
        model = Taller
        fields = [
            'id', 'titulo', 'fecha', 'duracion_horas', 'estado',
            'profesor', 'lugar', 'categoria', 'observacion'
        ]