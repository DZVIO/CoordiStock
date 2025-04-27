from rest_framework import serializers
from app.models import Terminal, Activo, Agente, Area

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ['id', 'terminal', 'nombre', 'direccion']
    
class ActivoSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(source='id_marca.marca')
    class Meta:
        model = Activo
        fields = ['id','nombre_marca', 'activo', 'modelo', 'n_serie', 'renting']
    
class AgenteSerializer(serializers.ModelSerializer):
    nombre_area = serializers.CharField(source='id_area.area')
    nombre_terminal = serializers.CharField(source='id_terminal.terminal')
    class Meta:
        model = Agente
        fields = ['id','nombre', 'codigo', 'email', 'nombre_area', 'nombre_terminal']

class AreaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Area
        fields = ['id','area']