from rest_framework import serializers
from .models import CategoriaPermissao, Permissao, Cargo

class CategoriaPermissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaPermissao
        exclude = ["id"]

class PermissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissao
        exclude = ["id"]
    
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        exclude = ["id"]
