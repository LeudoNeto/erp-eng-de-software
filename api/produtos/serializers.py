from rest_framework import serializers
from .models import produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = produto
        exclude = ["id"]