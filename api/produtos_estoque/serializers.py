from rest_framework import serializers
from .models import produto_estoque

class ProdutoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = produto_estoque
        exclude = ["id"]