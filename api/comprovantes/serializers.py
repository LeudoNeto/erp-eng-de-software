from rest_framework import serializers
from .models import comprovante, comprovante_produtos

class ComprovanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = comprovante
        exclude = ["id"]

class ComprovanteProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = comprovante_produtos
        exclude = ["id"]