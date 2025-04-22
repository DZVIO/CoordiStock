from rest_framework import serializers
from app.models import Terminal, Activo

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ['id', 'terminal', 'nombre', 'direccion']
    
class ActivoSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(source='id_marca.marca')
    class Meta:
        model = Activo
        fields = ['nombre_marca', 'activo', 'modelo', 'n_serie']