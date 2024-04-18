from rest_framework import serializers
from .models import nota_fiscal, nota_fiscal_produtos

class NotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = nota_fiscal
        exclude = ["id"]

class NotaFiscalProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = nota_fiscal_produtos
        exclude = ["id"]